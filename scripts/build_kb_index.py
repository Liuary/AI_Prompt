#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scripts/build_kb_index.py
# 知识库索引构建工具：向量索引 + 图谱索引
#
# 功能：
#   - 默认模式：读取 .ai/kb/*.md 中的 [+] 条目，生成向量索引（BGE-small-zh-v1.5）
#   - --graph 模式：解析 [[wikilink]] 链接，构建有向图谱，输出 .ai/tmp/graph.json
#
# 依赖：pip install sentence-transformers

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path


# ── 路径常量 ────────────────────────────────────────────────────

KB_DIR = Path(__file__).resolve().parent.parent / ".ai" / "kb"
VECTORS_DIR = Path(__file__).resolve().parent.parent / ".ai" / "tmp" / "vectors"
INDEX_FILE = VECTORS_DIR / "index.json"
HASHES_FILE = VECTORS_DIR / "file_hashes.json"
GRAPH_FILE = Path(__file__).resolve().parent.parent / ".ai" / "tmp" / "graph.json"

MODEL_NAME = "BAAI/bge-small-zh-v1.5"

HF_ENDPOINT = os.environ.get("HF_ENDPOINT", "https://huggingface.co")


# ── 条目提取 ────────────────────────────────────────────────────

def extract_entries(file_path: Path) -> list[dict]:
    """从单个 kb 文件提取所有 [+] 条目。
    返回列表，每项含 file、category、title、content、full_text 字段。
    """
    raw = file_path.read_text(encoding="utf-8")
    category = file_path.stem  # architecture / patterns / troubleshooting / setup

    pattern = re.compile(r'^##\s*\[\+\]\s*(.+?)$\n(.*?)(?=^##\s|\Z)', re.MULTILINE | re.DOTALL)
    entries = []
    for match in pattern.finditer(raw):
        title = match.group(1).strip()
        content = match.group(2).strip()
        if not content:
            continue
        entries.append({
            "file": file_path.name,
            "category": category,
            "title": title,
            "content": content,
            "full_text": f"{title}\n{content}",
        })
    return entries


def compute_file_hash(file_path: Path) -> str:
    """计算文件 SHA-256 哈希值。"""
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def load_hashes() -> dict:
    """加载文件哈希记录。"""
    if HASHES_FILE.exists():
        return json.loads(HASHES_FILE.read_text(encoding="utf-8"))
    return {}


def save_hashes(hashes: dict) -> None:
    """保存文件哈希记录。"""
    VECTORS_DIR.mkdir(parents=True, exist_ok=True)
    HASHES_FILE.write_text(json.dumps(hashes, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 向量索引 ────────────────────────────────────────────────────

def load_model():
    """延迟加载 sentence-transformers 模型。"""
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    except ImportError:
        print("错误: 未安装 sentence-transformers 库")
        print("请执行: pip install sentence-transformers")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 无法加载模型 {MODEL_NAME}: {e}")
        if HF_ENDPOINT == "https://huggingface.co":
            print(f"提示: 可通过环境变量 HF_ENDPOINT=https://hf-mirror.com 使用镜像加速下载")
        sys.exit(1)


def build_index(incremental: bool = True, kb_dir_override: Path = None) -> dict:
    """构建向量索引。

    参数：
        incremental: True 时仅增量更新已变化的文件
        kb_dir_override: 可选的自定义知识库目录

    返回：
        {"total": 条目总数, "changed": 变更数, "skipped": 跳过数, "removed_files": [...]}
    """
    src_dir = kb_dir_override if kb_dir_override else KB_DIR

    if not src_dir.exists():
        print(f"错误: 知识库目录不存在: {src_dir}")
        sys.exit(1)

    old_hashes = load_hashes() if incremental else {}
    new_hashes = {}

    existing = []
    if incremental and INDEX_FILE.exists():
        try:
            data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {"entries": []}
        existing = data.get("entries", [])

    model = None
    entries = []
    changed_count = 0
    skipped_count = 0
    total_count = 0

    md_files = sorted([f for f in src_dir.glob("*.md") if f.name != "index.md"])
    for fp in md_files:
        file_hash = compute_file_hash(fp)
        new_hashes[fp.name] = file_hash

        if incremental and fp.name in old_hashes and old_hashes[fp.name] == file_hash:
            reused = [e for e in existing if e["file"] == fp.name]
            entries.extend(reused)
            skipped_count += len(reused)
            total_count += len(reused)
            continue

        file_entries = extract_entries(fp)
        if not file_entries:
            continue

        if model is None:
            model = load_model()

        texts = [e["full_text"] for e in file_entries]
        embeddings = model.encode(texts, normalize_embeddings=True)

        for i, entry in enumerate(file_entries):
            entry["embedding"] = embeddings[i].tolist()
            entries.append(entry)
            changed_count += 1
            total_count += 1

    removed_files = set(old_hashes.keys()) - set(new_hashes.keys())
    if removed_files:
        entries = [e for e in entries if e["file"] not in removed_files]

    save_hashes(new_hashes)

    index_data = {
        "entries": entries,
        "metadata": {
            "model": MODEL_NAME,
            "total": len(entries),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "incremental": incremental,
        },
    }

    VECTORS_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "total": len(entries),
        "changed": changed_count,
        "skipped": skipped_count,
        "removed_files": list(removed_files),
    }


# ── 图谱构建 ────────────────────────────────────────────────────

def canonical_title(title: str) -> str:
    """去除标题末尾的日期后缀，返回规范标题名。
    例如 "OAuth2 登录流程 (2026-05-20)" → "OAuth2 登录流程"
    """
    return re.sub(r'\s*\(\d{4}-\d{2}-\d{2}\)\s*$', '', title).strip()


def load_register(index_path: Path) -> dict:
    """从 kb/index.md 加载条目标题注册表。
    返回 {规范标题名: {"file": "xx.md", "category": "xx", "title": "完整标题"}}。

    注册表同时支持完整标题和规范标题两种查找方式。
    """
    if not index_path.exists():
        print(f"警告: kb/index.md 不存在: {index_path}")
        return {}

    register = {}

    for fp in sorted((index_path.parent).glob("*.md")):
        if fp.name == "index.md":
            continue
        category = fp.stem
        entries = extract_entries(fp)
        for e in entries:
            full_title = e["title"].strip()
            cid = canonical_title(full_title)
            if cid not in register:
                register[cid] = {
                    "file": fp.name,
                    "category": category,
                    "title": full_title,
                }

    return register


def parse_wikilinks(text: str) -> list[str]:
    """从文本中提取所有 [[wikilink]] 引用。
    返回目标条目名列表（不含锚点部分），已去重。
    """
    pattern = re.compile(r'(?<!\\)\[\[([^\]|#]+)(?:#[^\]]+)?(?:\|[^\]]+)?\]\]')
    results = []
    seen = set()
    for match in pattern.finditer(text):
        target = match.group(1).strip()
        if target and target not in seen:
            seen.add(target)
            results.append(target)
    return results


def build_graph(kb_dir_override: Path = None) -> dict:
    """解析所有 kb 文件中的 [[wikilink]] 链接，构建有向图谱。

    返回：
        {"nodes": [...], "edges": [{from, to}, ...]}
    """
    src_dir = kb_dir_override if kb_dir_override else KB_DIR

    if not src_dir.exists():
        print(f"错误: 知识库目录不存在: {src_dir}")
        sys.exit(1)

    index_path = src_dir / "index.md"
    register = load_register(index_path)

    if not register:
        print("警告: 知识库注册表为空，图谱无节点")
        return {"nodes": [], "edges": []}

    nodes = []
    nodes_set = set()
    for title, info in register.items():
        if title not in nodes_set:
            nodes.append({
                "id": title,
                "file": info["file"],
                "title": info.get("title", title),
                "category": info.get("category", ""),
            })
            nodes_set.add(title)

    edges = []
    edges_set = set()
    for fp in sorted([f for f in src_dir.glob("*.md") if f.name != "index.md"]):
        raw = fp.read_text(encoding="utf-8")
        links = parse_wikilinks(raw)

        file_entries = extract_entries(fp)
        source_cids = set(canonical_title(e["title"].strip()) for e in file_entries)

        for source_cid in source_cids:
            if source_cid not in register:
                continue
            for target in links:
                target_cid = canonical_title(target)
                if target_cid not in register:
                    continue
                if source_cid == target_cid:
                    continue
                edge_key = (source_cid, target_cid)
                if edge_key not in edges_set:
                    edges.append({"from": source_cid, "to": target_cid})
                    edges_set.add(edge_key)

    return {"nodes": nodes, "edges": edges}


def save_graph(graph: dict, output_path: Path = None) -> Path:
    """保存图谱到 JSON 文件。"""
    dest = output_path if output_path else GRAPH_FILE
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def compute_graph_stats(graph: dict) -> dict:
    """计算图谱统计信息。"""
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    out_degree = {}
    in_degree = {}
    for n in nodes:
        nid = n["id"]
        out_degree[nid] = 0
        in_degree[nid] = 0

    for edge in edges:
        f = edge["from"]
        t = edge["to"]
        out_degree[f] = out_degree.get(f, 0) + 1
        in_degree[t] = in_degree.get(t, 0) + 1

    isolated = [nid for nid in out_degree if out_degree[nid] == 0 and in_degree.get(nid, 0) == 0]

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "isolated_count": len(isolated),
        "isolated_nodes": isolated,
        "max_out_degree": max(out_degree.values()) if out_degree else 0,
        "max_in_degree": max(in_degree.values()) if in_degree else 0,
    }


# ── 命令行入口 ──────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="知识库索引构建工具：向量索引 + 图谱索引",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python scripts/build_kb_index.py                  # 构建/更新向量索引（增量）
  python scripts/build_kb_index.py --full           # 全量重建向量索引
  python scripts/build_kb_index.py --graph          # 构建知识图谱
  python scripts/build_kb_index.py --graph --stats  # 构建图谱并输出统计
  python scripts/build_kb_index.py --dry-run        # 预览文件变更
        """,
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="全量重建索引（默认：增量更新）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览变更，不实际写入",
    )
    parser.add_argument(
        "--kb-dir",
        default=None,
        help=f"自定义知识库目录（默认: {KB_DIR}）",
    )
    parser.add_argument(
        "--graph",
        action="store_true",
        help="构建知识图谱（解析 [[wikilink]] 链接），输出到 .ai/tmp/graph.json",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="与 --graph 配合使用，输出图谱统计信息",
    )
    parser.add_argument(
        "--graph-output",
        default=None,
        help="自定义图谱输出路径（默认: .ai/tmp/graph.json）",
    )
    args = parser.parse_args()

    kb_dir = Path(args.kb_dir).resolve() if args.kb_dir else KB_DIR

    if args.dry_run:
        old_hashes = load_hashes()
        md_files = sorted([f for f in kb_dir.glob("*.md") if f.name != "index.md"])
        changed = []
        unchanged = []
        new_files = []
        for fp in md_files:
            h = compute_file_hash(fp)
            if fp.name not in old_hashes:
                new_files.append(fp.name)
            elif old_hashes[fp.name] != h:
                changed.append(fp.name)
            else:
                unchanged.append(fp.name)

        removed = set(old_hashes.keys()) - {f.name for f in md_files}
        print(f"知识库目录: {kb_dir}")
        print(f"Markdown 文件: {len(md_files)} 个")
        if new_files:
            print(f"新增文件: {', '.join(new_files)}")
        if changed:
            print(f"已修改文件: {', '.join(changed)}")
        if unchanged:
            print(f"未变化文件: {', '.join(unchanged)}")
        if removed:
            print(f"已删除文件: {', '.join(removed)}")
        if not new_files and not changed and not removed:
            print("所有文件均为最新，无需重建索引")
        return

    if args.graph:
        graph = build_graph(kb_dir_override=kb_dir)
        output_path = Path(args.graph_output).resolve() if args.graph_output else None
        dest = save_graph(graph, output_path)

        print(f"图谱文件: {dest}")
        print(f"  节点: {len(graph['nodes'])}")
        print(f"  边: {len(graph['edges'])}")

        if args.stats:
            stats = compute_graph_stats(graph)
            print(f"  孤立节点: {stats['isolated_count']}")
            if stats['isolated_nodes']:
                print(f"    无链接条目: {', '.join(stats['isolated_nodes'])}")
            print(f"  最大出度: {stats['max_out_degree']}")
            print(f"  最大入度: {stats['max_in_degree']}")
        return

    incremental = not args.full
    result = build_index(incremental=incremental, kb_dir_override=kb_dir)

    print(f"索引文件: {INDEX_FILE}")
    print(f"  模型: {MODEL_NAME}")
    print(f"  总条目: {result['total']}")
    print(f"  新增/更新: {result['changed']} 条")
    if result["skipped"]:
        print(f"  跳过（未变化）: {result['skipped']} 条")
    if result["removed_files"]:
        print(f"  已删除文件: {', '.join(result['removed_files'])}")
    print(f"  更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
