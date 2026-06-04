#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""閻儴鐦戞惔鎾磋穿閸氬牊顥呯槐銏ｅ壖閺堫兙鈧?
鐎圭偟骞囩拠顓濈疅閻╅晲鎶€鎼?+ 閺傚洣娆㈤崥?閺嶅洭顣界划鍓р€橀崠褰掑帳 + 閺冨爼妫跨悰鏉垮櫤閾诲秴鎮庨幍鎾冲瀻閿?娴?.ai/tmp/vectors/index.json 閸旂姾娴囩槐銏犵穿閿涘本鏁幐浣告嚒娴犮倛顢戦弻銉嚄閵?
娓氭繆绂嗛敍姝眎p install sentence-transformers
"""

import json
import math
import os
import re
import sys
import time
from pathlib import Path


# 閳光偓閳光偓 鐠侯垰绶炵敮鎼佸櫤 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

VECTORS_DIR = Path(__file__).resolve().parent.parent / ".ai" / "tmp" / "vectors"
INDEX_FILE = VECTORS_DIR / "index.json"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"

# HuggingFace 闂€婊冨剼缁旑垳鍋ｉ敍鍫濇禇閸愬懐缍夌紒婊呭箚婢у啫褰茬拋鍙ヨ礋 https://hf-mirror.com閿?HF_ENDPOINT = os.environ.get("HF_ENDPOINT", "https://huggingface.co")

# 濞ｅ嘲鎮庡Λ鈧槐銏℃綀闁?WEIGHT_SEMANTIC = 0.6     # 鐠囶厺绠熼惄闀愭妧鎼达附娼堥柌?WEIGHT_EXACT = 0.3        # 缁墽鈥橀崠褰掑帳閺夊啴鍣?WEIGHT_TIME = 0.1         # 閺冨爼妫跨悰鏉垮櫤閺夊啴鍣?TIME_HALF_LIFE_DAYS = 30  # 閺冨爼妫跨悰鏉垮櫤閸楀﹨鈥滈張鐕傜礄婢垛晪绱?

# 閳光偓閳光偓 缁便垹绱╅崝鐘烘祰 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

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

# 閳光偓閳光偓 鐠囧嫬鍨庨崙鑺ユ殶 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """鐠侊紕鐣绘稉銈勯嚋瀹告彃缍婃稉鈧崠鏍ф倻闁插繒娈戞担娆忛浮閻╅晲鎶€鎼达讣绱欑粵澶夌幆娴滃海鍋ｇ粔顖ょ礆閵?""
    if len(vec_a) != len(vec_b):
        return 0.0
    return sum(a * b for a, b in zip(vec_a, vec_b))


def compute_semantic_score(query_embedding: list[float], entry_embedding: list[float]) -> float:
    """鐠侊紕鐣荤拠顓濈疅閻╅晲鎶€鎼达箑鍨庨弫?[0, 1]閵?""
    sim = cosine_similarity(query_embedding, entry_embedding)
    return max(0.0, min(1.0, sim))


def compute_exact_score(query: str, entry: dict) -> float:
    """鐠侊紕鐣荤划鍓р€橀崠褰掑帳閸掑棙鏆?[0, 1]閵?
    閸栧綊鍘ょ紒鏉戝閿涙碍鏋冩禒璺烘倳閵嗕焦鐖ｆ０妯糕偓浣稿瀻缁鎮曟稉顓犳畱閸忔娊鏁拠宥呮嚒娑擃厹鈧?    """
    query_lower = query.lower()
    score = 0.0
    max_possible = 3.0

    # 閺傚洣娆㈤崥宥呭爱闁板稄绱欐俊?architecture.md 閳劏鍟?architecture閿?    file_stem = entry["file"].replace(".md", "").lower()
    if file_stem in query_lower or any(w in file_stem for w in query_lower.split()):
        score += 1.0

    # 閺嶅洭顣介崠褰掑帳
    title_lower = entry["title"].lower()
    query_words = query_lower.split()
    matches = sum(1 for w in query_words if w in title_lower)
    if query_words:
        score += matches / len(query_words)

    # 閸掑棛琚崥宥呭爱闁?    category_lower = entry["category"].lower()
    if any(w in category_lower for w in query_words):
        score += 0.5

    return score / max_possible


def compute_time_decay(updated_at: str, half_life_days: int = TIME_HALF_LIFE_DAYS) -> float:
    """鐠侊紕鐣婚弮鍫曟？鐞涙澘鍣洪崶鐘茬摍 [0, 1]閵?
    閺堚偓鏉╂垶娲块弬鎵畱閺夛紕娲板妤€鍨庨弴鎾彯閿涘苯宕愮悰鐗堟埂閸氬孩娼堥柌宥呭櫤閸楀鈧?    """
    try:
        updated_time = time.mktime(time.strptime(updated_at, "%Y-%m-%d %H:%M:%S"))
    except (ValueError, TypeError):
        return 0.5  # 閺冪姵纭剁憴锝嗙€介弮鍫曟？閺冨墎绮版稉顓熲偓褍鈧?
    now = time.time()
    age_days = (now - updated_time) / 86400.0
    if age_days <= 0:
        return 1.0

    decay = math.pow(0.5, float(age_days) / float(half_life_days))
    return max(0.1, decay)  # 娣囨繂绨?0.1閿涘矂浼╅崗宥呭坊閸欏弶娼惄顔肩暚閸忋劍鐭囨惔?

# 閳光偓閳光偓 濞ｅ嘲鎮庡Λ鈧槐?閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

def search(query: str, top_k: int = 10, min_score: float = 0.1) -> list[dict]:
    """閹笛嗩攽濞ｅ嘲鎮庡Λ鈧槐顫偓?
    閸欏倹鏆?
        query: 閺屻儴顕楅弬鍥ㄦ拱
        top_k: 鏉╂柨娲栫紒鎾寸亯閺佷即鍣?        min_score: 閺堚偓娴ｅ骸鍨庨弫浼存閸婄》绱濇担搴濈艾濮濄倕鈧偐娈戠紒鎾寸亯鐞氼偉绻冨?
    鏉╂柨娲?
        閹烘帒绨崥搴ｆ畱缂佹挻鐏夐崚妤勩€冮敍灞剧槨妞ょ懓瀵橀崥?file閵嗕恭ategory閵嗕辜itle閵嗕恭ontent閵嗕够cores閿涘牆鎯堥崥鍕€嶉崚鍡樻殶閿?    """
    index = load_index()
    entries = index.get("entries", [])
    metadata = index.get("metadata", {})
    updated_at = metadata.get("updated_at", "")

    if not entries:
        return []

    # 閸旂姾娴囧Ο鈥崇€烽獮鍓佺椽閻焦鐓＄拠?    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    except ImportError:
        print("闁挎瑨顕? 闂団偓鐟曚礁鐣ㄧ憗?sentence-transformers")
        print("鏉╂劘顢? pip install sentence-transformers")
        sys.exit(1)
    except Exception as e:
        print(f"闁挎瑨顕? 閸旂姾娴囧Ο鈥崇€锋径杈Е: {e}")
        if HF_ENDPOINT == "https://huggingface.co":
            print(f"閹绘劗銇? 閸ヨ棄鍞寸純鎴犵捕閸欘垵顔曠純顔惧箚婢у啫褰夐柌?HF_ENDPOINT=https://hf-mirror.com 娴ｈ法鏁ら梹婊冨剼")
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

        # 閾诲秴鎮庨崝鐘虫綀濮瑰倸鎷?        final_score = (
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


# 閳光偓閳光偓 閸涙垝鎶ょ悰灞藉弳閸?閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

def format_output(results: list[dict], verbose: bool = False) -> None:
    """閺嶇厧绱￠崠鏍翻閸戠儤顥呯槐銏㈢波閺嬫嚎鈧?""
    if not results:
        print("閺堫亝澹橀崚鏉垮爱闁板秶娈戦惌銉ㄧ槕鎼存挻娼惄顔衡偓?)
        print("  瀵ら缚顔呴敍姘毦鐠囨洘娲跨€硅姤纭鹃惃鍕叀鐠囥垼鐦濋敍灞惧灗鏉╂劘顢?build_kb_index.py 绾喕绻氱槐銏犵穿娑撶儤娓堕弬鑸偓?)
        return

    print(f"閹垫儳鍩?{len(results)} 閺夛紕娴夐崗铏蒋閻?\n")
    for i, r in enumerate(results, 1):
        print(f"{'閳光偓' * 60}")
        print(f"  #{i} [{r['category']}] {r['title']}")
        print(f"  閺傚洣娆? {r['file']}")
        print(f"  瀵版鍨? {r['score']}")
        if verbose:
            print(f"    閳光偓 鐠囶厺绠熼惄闀愭妧鎼? {r['scores_detail']['semantic']}")
            print(f"    閳光偓 缁墽鈥橀崠褰掑帳:   {r['scores_detail']['exact_match']}")
            print(f"    閳光偓 閺冨爼妫跨悰鏉垮櫤:   {r['scores_detail']['time_decay']}")
        content_preview = r["content"][:200]
        if len(r["content"]) > 200:
            content_preview += "閳?
        print(f"  閸愬懎顔? {content_preview}")
    print(f"{'閳光偓' * 60}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="閻儴鐦戞惔鎾诡嚔娑斿顥呯槐?)
    parser.add_argument(
        "query",
        nargs="?",
        help="閺屻儴顕楅弬鍥ㄦ拱",
    )
    parser.add_argument(
        "-k", "--top-k",
        type=int,
        default=10,
        help="鏉╂柨娲栫紒鎾寸亯閺佷即鍣洪敍鍫ョ帛鐠? 10閿?,
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.1,
        help="閺堚偓娴ｅ骸鍨庨弫浼存閸婄》绱欐妯款吇: 0.1閿?,
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="閺勫墽銇氱拠锔剧矎鐠囧嫬鍨庢穱鈩冧紖",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="娴溿倓绨板Ο鈥崇础閿涘牊瀵旂紒顓＄翻閸忋儲鐓＄拠顫礆",
    )
    args = parser.parse_args()

    if args.interactive:
        print("閻儴鐦戞惔鎾诡嚔娑斿顥呯槐顫礄娴溿倓绨板Ο鈥崇础閿?)
        print("鏉堟挸鍙嗛弻銉嚄閺傚洦婀伴敍宀冪翻閸?/exit 闁偓閸戠n")
        while True:
            try:
                q = input("閺屻儴顕? ").strip()
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
