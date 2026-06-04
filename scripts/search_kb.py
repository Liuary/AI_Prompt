#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scripts/search_kb.py
# 知识库语义搜索工具：向量相似度 + 精确匹配 + 时间衰减融合检索
#
# 从 .ai/tmp/vectors/index.json 加载向量索引，使用 BGE-small-zh-v1.5 编码查询并检索
#
# 依赖：pip install sentence-transformers

import json
import math
import os
import re
import sys
import time
from pathlib import Path


# ── 路径常量 ────────────────────────────────────────────────────

VECTORS_DIR = Path(__file__).resolve().parent.parent / ".ai" / "tmp" / "vectors"
INDEX_FILE = VECTORS_DIR / "index.json"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"

HF_ENDPOINT = os.environ.get("HF_ENDPOINT", "https://huggingface.co")

# 融合权重
WEIGHT_SEMANTIC = 0.6     # 语义相似度权重
WEIGHT_EXACT = 0.3        # 精确匹配权重
WEIGHT_TIME = 0.1         # 时间衰减权重
TIME_HALF_LIFE_DAYS = 30  # 时间衰减半衰期（天）


# ── 索引加载 ────────────────────────────────────────────────────

def load_index() -> dict:
    """加载向量索引文件。"""
    if not INDEX_FILE.exists():
        print(f"提示: 向量索引不存在: {INDEX_FILE}")
        print("请先运行: python scripts/build_kb_index.py 构建索引")
        return {"entries": []}

    try:
        data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        return data
    except json.JSONDecodeError:
        print(f"警告: 索引文件已损坏: {INDEX_FILE}")
        print("请重新运行: python scripts/build_kb_index.py")
        return {"entries": []}


# ── 分数计算 ────────────────────────────────────────────────────

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """计算两个归一化向量的余弦相似度。"""
    if len(vec_a) != len(vec_b):
        return 0.0
    return sum(a * b for a, b in zip(vec_a, vec_b))


def compute_semantic_score(query_embedding: list[float], entry_embedding: list[float]) -> float:
    """计算语义相似度分数 [0, 1]。"""
    sim = cosine_similarity(query_embedding, entry_embedding)
    return max(0.0, min(1.0, sim))


def compute_exact_score(query: str, entry: dict) -> float:
    """计算精确匹配分数 [0, 1]。
    考虑文件名、标题、分类三个维度的关键词匹配。
    """
    query_lower = query.lower()
    score = 0.0
    max_possible = 3.0

    # 文件名匹配
    file_stem = entry["file"].replace(".md", "").lower()
    if file_stem in query_lower or any(w in file_stem for w in query_lower.split()):
        score += 1.0

    # 标题匹配
    title_lower = entry["title"].lower()
    query_words = query_lower.split()
    matches = sum(1 for w in query_words if w in title_lower)
    if query_words:
        score += matches / len(query_words)

    # 分类匹配
    category_lower = entry["category"].lower()
    if any(w in category_lower for w in query_words):
        score += 0.5

    return score / max_possible


def compute_time_decay(updated_at: str, half_life_days: int = TIME_HALF_LIFE_DAYS) -> float:
    """计算时间衰减系数 [0, 1]。
    越新的条目权重越高，衰减以半衰期为基准。
    """
    try:
        updated_time = time.mktime(time.strptime(updated_at, "%Y-%m-%d %H:%M:%S"))
    except (ValueError, TypeError):
        return 0.5
    now = time.time()
    age_days = (now - updated_time) / 86400.0
    if age_days <= 0:
        return 1.0

    decay = math.pow(0.5, float(age_days) / float(half_life_days))
    return max(0.1, decay)


# ── 融合搜索 ────────────────────────────────────────────────────

def search(query: str, top_k: int = 10, min_score: float = 0.1) -> list[dict]:
    """执行融合搜索。
    参数：
        query: 查询文本
        top_k: 返回结果数量
        min_score: 最低分数阈值，低于此值的结果被过滤
    返回：
        排序后的结果列表，每项含 file、category、title、content、score、scores_detail 字段
    """
    index = load_index()
    entries = index.get("entries", [])
    metadata = index.get("metadata", {})
    updated_at = metadata.get("updated_at", "")

    if not entries:
        return []

    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    except ImportError:
        print("错误: 未安装 sentence-transformers")
        print("请执行: pip install sentence-transformers")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 无法加载模型: {e}")
        if HF_ENDPOINT == "https://huggingface.co":
            print(f"提示: 可通过环境变量 HF_ENDPOINT=https://hf-mirror.com 使用镜像加速下载")
        sys.exit(1)

    query_embedding = model.encode([query], normalize_embeddings=True)[0]

    results = []
    for entry in entries:
        if "embedding" not in entry:
            continue

        entry_embedding = entry["embedding"]

        semantic = compute_semantic_score(query_embedding.tolist(), entry_embedding)
        exact = compute_exact_score(query, entry)
        time_factor = compute_time_decay(updated_at)

        final_score = (
            WEIGHT_SEMANTIC * semantic +
            WEIGHT_EXACT * exact +
            WEIGHT_TIME * time_factor
        )

        if final_score < min_score:
            continue

        results.append({
            "file": entry["file"],
            "category": entry["category"],
            "title": entry["title"],
            "content": entry["content"],
            "score": round(final_score, 4),
            "scores_detail": {
                "semantic": round(semantic, 4),
                "exact_match": round(exact, 4),
                "time_decay": round(time_factor, 4),
            },
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ── 输出格式化 ──────────────────────────────────────────────────

def format_output(results: list[dict], verbose: bool = False) -> None:
    """格式化输出检索结果。"""
    if not results:
        print("未找到与查询相关的知识条目。")
        print("  请尝试：使用更宽泛的查询词、确认知识库中已包含相关内容（运行 build_kb_index.py 重建索引后重试）")
        return

    print(f"找到 {len(results)} 条相关条目\n")
    for i, r in enumerate(results, 1):
        print(f"{'─' * 60}")
        print(f"  #{i} [{r['category']}] {r['title']}")
        print(f"  文件: {r['file']}")
        print(f"  得分: {r['score']}")
        if verbose:
            print(f"    ├─ 语义相似度: {r['scores_detail']['semantic']}")
            print(f"    ├─ 精确匹配:   {r['scores_detail']['exact_match']}")
            print(f"    └─ 时间衰减:   {r['scores_detail']['time_decay']}")
        content_preview = r["content"][:200]
        if len(r["content"]) > 200:
            content_preview += "..."
        print(f"  内容: {content_preview}")
    print(f"{'─' * 60}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="知识库语义搜索工具")
    parser.add_argument(
        "query",
        nargs="?",
        help="查询文本",
    )
    parser.add_argument(
        "-k", "--top-k",
        type=int,
        default=10,
        help="返回结果数量（默认: 10）",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.1,
        help="最低分数阈值（默认: 0.1）",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细分数构成",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="交互式搜索模式",
    )
    args = parser.parse_args()

    if args.interactive:
        print("知识库语义搜索 — 交互模式")
        print("输入查询文本开始搜索，输入 /exit 退出")
        while True:
            try:
                q = input("查询: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not q:
                continue
            if q == "/exit":
                break
            results = search(q, top_k=args.top_k, min_score=args.min_score)
            format_output(results, verbose=args.verbose)
        return

    if not args.query:
        parser.print_help()
        sys.exit(0)

    results = search(args.query, top_k=args.top_k, min_score=args.min_score)
    format_output(results, verbose=args.verbose)


if __name__ == "__main__":
    main()
