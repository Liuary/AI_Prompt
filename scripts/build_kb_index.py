#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""閻儴鐦戞惔鎾虫倻闁插繒鍌ㄥ鏇熺€楦垮壖閺堫兙鈧?
鐠囪褰?.ai/kb/*.md 娑擃厽澧嶉張?[+] 閺夛紕娲伴敍灞煎▏閻?bge-small-zh-v1.5 閻㈢喐鍨氶崥鎴﹀櫤缁便垹绱╅敍?鐎涙ê鍋嶉崚?.ai/tmp/vectors/閵嗗倿鈧俺绻冮弬鍥︽閸愬懎顔愰崫鍫濈瑖閸嬫艾顤冮柌蹇旀纯閺傚府绱濈捄瀹犵箖閺堫亜褰夐崠鏍ㄦ瀮娴犺翰鈧?
娓氭繆绂嗛敍姝眎p install sentence-transformers
"""

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path


# 閳光偓閳光偓 鐠侯垰绶炵敮鎼佸櫤 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

KB_DIR = Path(__file__).resolve().parent.parent / ".ai" / "kb"
VECTORS_DIR = Path(__file__).resolve().parent.parent / ".ai" / "tmp" / "vectors"
INDEX_FILE = VECTORS_DIR / "index.json"
HASHES_FILE = VECTORS_DIR / "file_hashes.json"

# BGE-small 娑擃厽鏋冨Ο鈥崇€烽敍灞灸侀崹瀣毈閿涘瀫100MB閿涘鈧浇宸濋柌蹇撱偨閿涘矂鈧倸鎮庨張顒€婀存潪濠氬櫤鐠囶厺绠熷Λ鈧槐?MODEL_NAME = "BAAI/bge-small-zh-v1.5"

# HuggingFace 闂€婊冨剼缁旑垳鍋ｉ敍鍫濇禇閸愬懐缍夌紒婊呭箚婢у啫褰茬拋鍙ヨ礋 https://hf-mirror.com閿?HF_ENDPOINT = os.environ.get("HF_ENDPOINT", "https://huggingface.co")


# 閳光偓閳光偓 閺夛紕娲扮憴锝嗙€?閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

def extract_entries(file_path: Path) -> list[dict]:
    """娴犲骸宕熸稉?kb 閺傚洣娆㈡稉顓熷絹閸欐牗澧嶉張?[+] 閺夛紕娲伴妴?
    閺夛紕娲伴弽鐓庣础閿?        ## [+] 閺夛紕娲伴弽鍥暯
        閸愬懎顔愬▓浣冩儰閿涘牆褰茬捄銊ヮ樋鐞涘矉绱濋惄鏉戝煂娑撳绔存稉?## 閹存牗鏋冩禒鍓佺波閺夌噦绱?
    鏉╂柨娲栭弶锛勬窗閸掓銆冮敍灞剧槨妞ょ懓瀵橀崥?title閵嗕恭ontent閵嗕公ile閵嗕恭ategory閵?    """
    raw = file_path.read_text(encoding="utf-8")
    category = file_path.stem  # architecture / patterns / troubleshooting / setup

    # 閸栧綊鍘?## [+] 瀵偓婢跺娈戦弽鍥暯閸欏﹤鍙鹃崘鍛啇
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
    """鐠侊紕鐣婚弬鍥︽閸愬懎顔愰惃?SHA-256 閸濆牆绗囬妴?""
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def load_hashes() -> dict:
    """閸旂姾娴囨稉濠冾偧閺嬪嫬缂撻弮鏈电箽鐎涙娈戦弬鍥︽閸濆牆绗囩悰銊ｂ偓?""
    if HASHES_FILE.exists():
        return json.loads(HASHES_FILE.read_text(encoding="utf-8"))
    return {}


def save_hashes(hashes: dict) -> None:
    """娣囨繂鐡ㄨぐ鎾冲閺傚洣娆㈤崫鍫濈瑖鐞涖劊鈧?""
    VECTORS_DIR.mkdir(parents=True, exist_ok=True)
    HASHES_FILE.write_text(json.dumps(hashes, ensure_ascii=False, indent=2), encoding="utf-8")


# 閳光偓閳光偓 閸氭垿鍣洪崠?閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

def load_model():
    """瀵ゆ儼绻滈崝鐘烘祰 sentence-transformers 濡€崇€烽妴?""
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    except ImportError:
        print("闁挎瑨顕? 闂団偓鐟曚礁鐣ㄧ憗?sentence-transformers 娓氭繆绂?)
        print("鏉╂劘顢? pip install sentence-transformers")
        sys.exit(1)
    except Exception as e:
        print(f"闁挎瑨顕? 閸旂姾娴囧Ο鈥崇€?{MODEL_NAME} 婢惰精瑙? {e}")
        print("妫ｆ牗顐兼担璺ㄦ暏闂団偓娑撳娴囧Ο鈥崇€烽敍宀冾嚞濡偓閺屻儳缍夌紒婊嗙箾閹恒儱鑻熺粙宥呮倵闁插秷鐦?)
        if HF_ENDPOINT == "https://huggingface.co":
            print(f"閹绘劗銇? 閸ヨ棄鍞寸純鎴犵捕閸欘垵顔曠純顔惧箚婢у啫褰夐柌?HF_ENDPOINT=https://hf-mirror.com 娴ｈ法鏁ら梹婊冨剼")
        sys.exit(1)


def build_index(incremental: bool = True, kb_dir_override: Path = None) -> dict:
    """閺嬪嫬缂撻崥鎴﹀櫤缁便垹绱╅妴?
    閸欏倹鏆?
        incremental: True 閺冭泛顕В鏃€鏋冩禒璺烘惐鐢矉绱濈捄瀹犵箖閺堫亜褰夐崠鏍ㄦ瀮娴?        kb_dir_override: 鐟曞棛娲婃妯款吇閻儴鐦戞惔鎾舵窗瑜版洜娈戠捄顖氱窞

    鏉╂柨娲栫槐銏犵穿鐎涙鍚€閿?        {
            "entries": [ { file, category, title, content, full_text, embedding }, ... ],
            "metadata": { model, total, updated_at, incremental }
        }
    """
    src_dir = kb_dir_override if kb_dir_override else KB_DIR

    if not src_dir.exists():
        print(f"闁挎瑨顕? 閻儴鐦戞惔鎾舵窗瑜版洑绗夌€涙ê婀? {src_dir}")
        sys.exit(1)

    old_hashes = load_hashes() if incremental else {}
    new_hashes = {}

    # 閸旂姾娴囧鍙夋箒缁便垹绱╅敍鍫濐杻闁插繑膩瀵繑妞傞敍?    existing = []
    if incremental and INDEX_FILE.exists():
        try:
            data = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"警告: 索引文件已损坏，将重建: {INDEX_FILE}")
            data = {"entries": []}
        existing = data.get("entries", [])
        # 娴?(file, title) 娑撴椽鏁铏圭彌閺屻儲澹樼悰?
    model = None  # 瀵ゆ儼绻滈崝鐘烘祰
    entries = []
    changed_count = 0
    skipped_count = 0
    total_count = 0

    md_files = sorted(src_dir.glob("*.md"))
    for fp in md_files:
        file_hash = compute_file_hash(fp)
        new_hashes[fp.name] = file_hash

        if incremental and fp.name in old_hashes and old_hashes[fp.name] == file_hash:
            # 閺傚洣娆㈤張顏勫綁閸栨牭绱濇径宥囨暏瀹稿弶婀侀弶锛勬窗
            reused = [e for e in existing if e["file"] == fp.name]
            entries.extend(reused)
            skipped_count += len(reused)
            total_count += len(reused)
            continue

        # 閺傚洣娆㈤張澶婂綁閸栨牗鍨ㄦ＃鏍偧閺嬪嫬缂撻敍灞惧絹閸欐牗娼惄?        file_entries = extract_entries(fp)
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

    # 缁夊娅庡鎻掑灩闂勩倖鏋冩禒鍓佹畱閺夛紕娲伴敍鍫熸＋閸濆牆绗囨稉顓熸箒娴ｅ棙鏌婇崫鍫濈瑖娑擃厽妫ら惃鍕瀮娴犺绱?    removed_files = set(old_hashes.keys()) - set(new_hashes.keys())
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


# 閳光偓閳光偓 閸涙垝鎶ょ悰灞藉弳閸?閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

def main():
    import argparse

    parser = argparse.ArgumentParser(description="閺嬪嫬缂撻惌銉ㄧ槕鎼存挸鎮滈柌蹇曞偍瀵?)
    parser.add_argument(
        "--full",
        action="store_true",
        help="閸忋劑鍣洪柌宥呯紦缁便垹绱╅敍鍫濇嫹閻ｃ儱顤冮柌蹇撴惐鐢本顥呴弻銉礆",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="娴犲懏顥呴弻銉ユ憿娴滄稒鏋冩禒鍫曟付鐟曚焦娲块弬甯礉娑撳秴鐤勯梽鍛€铏瑰偍瀵?,
    )
    parser.add_argument(
        "--kb-dir",
        default=None,
        help=f"閻儴鐦戞惔鎾舵窗瑜版洝鐭惧鍕剁礄姒涙顓? {KB_DIR}閿?,
    )
    args = parser.parse_args()

    kb_dir = Path(args.kb_dir).resolve() if args.kb_dir else KB_DIR

    if args.dry_run:
        old_hashes = load_hashes()
        md_files = sorted(kb_dir.glob("*.md"))
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
        print(f"閻儴鐦戞惔鎾舵窗瑜? {kb_dir}")
        print(f"Markdown 閺傚洣娆? {len(md_files)} 娑?)
        if new_files:
            print(f"閺傛澘顤冮弬鍥︽: {', '.join(new_files)}")
        if changed:
            print(f"閸欐ɑ娲块弬鍥︽: {', '.join(changed)}")
        if unchanged:
            print(f"閺堫亜褰夐崠鏍ㄦ瀮娴? {', '.join(unchanged)}")
        if removed:
            print(f"瀹告彃鍨归梽銈嗘瀮娴? {', '.join(removed)}")
        if not new_files and not changed and not removed:
            print("閹碘偓閺堝鏋冩禒璺烘綆娑撶儤娓堕弬甯礉閺冪娀娓堕柌宥呯紦缁便垹绱?)
        return

    incremental = not args.full
    result = build_index(incremental=incremental, kb_dir_override=kb_dir)

    print(f"缁便垹绱╅弸鍕紦鐎瑰本鍨? {INDEX_FILE}")
    print(f"  濡€崇€? {MODEL_NAME}")
    print(f"  閹粯娼惄? {result['total']}")
    print(f"  閺傛壆绱惍? {result['changed']} 閺?)
    if result["skipped"]:
        print(f"  鐠哄疇绻?閺堫亜褰夐崠?: {result['skipped']} 閺?)
    if result["removed_files"]:
        print(f"  缁夊娅庨弬鍥︽: {', '.join(result['removed_files'])}")
    print(f"  閺囧瓨鏌婇弮鍫曟？: {time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
