#!/usr/bin/env python3
# scripts/ai_cli.py
# AI_Prompt 缁熶竴 CLI 宸ュ叿 鈥?宸ヤ綔鍖虹姸鎬佹煡璇笌鐭ヨ瘑搴撴悳绱?#
# 鐢ㄦ硶锛?#   python scripts/ai_cli.py status             鏄剧ず鎵€鏈夐樁娈电姸鎬?#   python scripts/ai_cli.py review             鍒楀嚭寰呭鐞嗗鏌ユ潯鐩?#   python scripts/ai_cli.py bugs               鍒楀嚭寰呭鐞?Bug
#   python scripts/ai_cli.py log                鏄剧ず鏈€杩戞棩蹇楁憳瑕?#   python scripts/ai_cli.py kb search <query>  鎼滅储鐭ヨ瘑搴?
import argparse
import os
import re
import sys
from pathlib import Path
from datetime import datetime


# 鈹€鈹€ 椤圭洰鏍圭洰褰曟娴?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def _find_project_root() -> Path:
    """鍚戜笂鏌ユ壘椤圭洰鏍圭洰褰曪紙鍖呭惈 .ai/ 鐨勭洰褰曪級銆?""
    current = Path(__file__).resolve().parent.parent
    while current != current.parent:
        if (current / ".ai").is_dir() and (current / "AGENTS.md").is_file():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent


PROJECT_ROOT = _find_project_root()
AI_DIR = PROJECT_ROOT / ".ai"
PLAN_DIR = AI_DIR / "plan"
LOG_DIR = AI_DIR / "log"
KB_DIR = AI_DIR / "kb"
USERS_DIR = AI_DIR / "users"


# 鈹€鈹€ 鍛戒护琛岃В鏋?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def build_parser():
    parser = argparse.ArgumentParser(
        prog="ai",
        description="AI_Prompt 缁熶竴 CLI 鈥?宸ヤ綔鍖虹姸鎬佹煡璇笌鐭ヨ瘑搴撴悳绱?,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
浣跨敤绀轰緥锛?  ai status                  鏄剧ず鎵€鏈夐樁娈电姸鎬?  ai review                  鍒楀嚭寰呭鐞嗗鏌ユ潯鐩?  ai bugs                    鍒楀嚭寰呭鐞?Bug
  ai log                     鏄剧ず鏈€杩戞棩蹇楁憳瑕?  ai kb search <鍏抽敭璇?       鎼滅储鐭ヨ瘑搴?  ai kb list                 鍒楀嚭鐭ヨ瘑搴撴枃浠?        """,
    )

    sub = parser.add_subparsers(dest="command", help="瀛愬懡浠?)

    # status
    sub.add_parser("status", help="鏄剧ず鎵€鏈夐樁娈电姸鎬?)

    # review
    sub.add_parser("review", help="鍒楀嚭寰呭鐞嗗鏌ユ潯鐩?)

    # bugs
    sub.add_parser("bugs", help="鍒楀嚭寰呭鐞?Bug")

    # log
    sub.add_parser("log", help="鏄剧ず鏈€杩戞棩蹇楁憳瑕?)

    # kb
    kb_parser = sub.add_parser("kb", help="鐭ヨ瘑搴撴搷浣?)
    kb_sub = kb_parser.add_subparsers(dest="kb_command", help="鐭ヨ瘑搴撳瓙鍛戒护")

    kb_search = kb_sub.add_parser("search", help="鎼滅储鐭ヨ瘑搴?)
    kb_search.add_argument("query", help="鎼滅储鍏抽敭璇?)

    kb_sub.add_parser("list", help="鍒楀嚭鐭ヨ瘑搴撴枃浠?)

    return parser


# 鈹€鈹€ 杈呭姪鍑芥暟 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def _read_status_md(filepath: Path) -> dict:
    """璇诲彇 status.md 骞舵彁鍙栫粨鏋勫寲瀛楁銆?""
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding="utf-8")
    info = {}
    patterns = {
        "鎵ц妯″紡": r"-\s+\*\*鎵ц妯″紡\*\*[锛?]\s*(.+)",
        "鑷姩鎺ㄨ繘": r"-\s+\*\*鑷姩鎺ㄨ繘\*\*[锛?]\s*(.+)",
        "鐘舵€?: r"-\s+\*\*鐘舵€乗*\*[锛?]\s*(.+)",
        "褰撳墠璐ｄ换 Agent": r"-\s+\*\*褰撳墠璐ｄ换 Agent\*\*[锛?]\s*(.+)",
        "涓婁竴璐ｄ换 Agent": r"-\s+\*\*涓婁竴璐ｄ换 Agent\*\*[锛?]\s*(.+)",
        "鏇存柊鏃堕棿": r"-\s+\*\*鏇存柊鏃堕棿\*\*[锛?]\s*(.+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, content)
        if m:
            info[key] = m.group(1).strip()
    return info


def _find_stage_status_files() -> list:
    """鏌ユ壘鎵€鏈?stage-*/status.md 鏂囦欢銆?""
    result = []
    if not PLAN_DIR.is_dir():
        return result
    for stage_dir in sorted(PLAN_DIR.iterdir()):
        if not stage_dir.is_dir():
            continue
        if not stage_dir.name.startswith("stage-"):
            continue
        status_path = stage_dir / "status.md"
        if status_path.exists():
            result.append((stage_dir.name, status_path))
    return result


def _find_review_files() -> dict:
    """鏌ユ壘绉佸煙瀹℃煡鏂囦欢锛岃繑鍥?{闃舵: {pending: [], fixing: [], resolved: []}}銆?""
    reviews = {}
    if not USERS_DIR.is_dir():
        return reviews
    for user_dir in USERS_DIR.iterdir():
        if not user_dir.is_dir():
            continue
        cr_dir = user_dir / "code_review"
        if not cr_dir.is_dir():
            continue
        for rev_file in cr_dir.glob("REV-*.md"):
            content = rev_file.read_text(encoding="utf-8")
            stage = rev_file.stem.replace("REV-", "").rsplit("-", 1)[0] if "-" in rev_file.stem[4:] else "unknown"
            # 妫€鏌ョ姸鎬佹爣璁?            status_match = re.search(r"-\s*\*\*鐘舵€乗*\*[锛?]\s*(pending|fixing|resolved|closed)", content)
            if not status_match:
                continue
            status = status_match.group(1)
            if status == "closed":
                continue
            # 璇诲彇鏍囬
            title_match = re.search(r"##\s+REV-\d+[锛?]\s*(.+)", content)
            title = title_match.group(1).strip() if title_match else rev_file.stem
            if stage not in reviews:
                reviews[stage] = []
            reviews[stage].append({"file": rev_file, "title": title, "status": status})
    return reviews


def _find_bug_files() -> dict:
    """鏌ユ壘绉佸煙 Bug 鏂囦欢锛岃繑鍥?{妯″潡: [{file, title, status}]}銆?""
    bugs = {}
    if not USERS_DIR.is_dir():
        return bugs
    for user_dir in USERS_DIR.iterdir():
        if not user_dir.is_dir():
            continue
        bugs_dir = user_dir / "bugs"
        if not bugs_dir.is_dir():
            continue
        for module_dir in bugs_dir.iterdir():
            if not module_dir.is_dir():
                continue
            for bug_file in module_dir.glob("BUG-*.md"):
                content = bug_file.read_text(encoding="utf-8")
                status_match = re.search(r"-\s*\*\*鐘舵€乗*\*[锛?]\s*(open|fixing|resolved|closed)", content)
                if not status_match:
                    continue
                status = status_match.group(1)
                if status == "closed":
                    continue
                title_match = re.search(r"##\s+BUG-\d+[锛?]\s*(.+)", content)
                title = title_match.group(1).strip() if title_match else bug_file.stem
                module = module_dir.name
                if module not in bugs:
                    bugs[module] = []
                bugs[module].append({"file": bug_file, "title": title, "status": status})
    return bugs


def _read_recent_logs(limit: int = 30) -> list:
    """璇诲彇鍏叡鏃ュ織鏈€杩戞潯鐩€?""
    entries = []
    if not LOG_DIR.is_dir():
        return entries
    log_index = LOG_DIR / "log.md"
    if log_index.exists():
        content = log_index.read_text(encoding="utf-8")
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- [") or stripped.startswith("- "):
                entries.append(stripped.lstrip("- "))
            if len(entries) >= limit:
                break
    return entries


def _search_kb(query: str) -> list:
    """鎼滅储鐭ヨ瘑搴撴枃浠讹紙绾枃鏈尮閰嶏紝涓嶄緷璧栧悜閲忕储寮曪級銆?""
    results = []
    if not KB_DIR.is_dir():
        return results
    query_lower = query.lower()
    for kb_file in sorted(KB_DIR.glob("*.md")):
        if kb_file.name == "index.md":
            continue
        try:
            content = kb_file.read_text(encoding="utf-8")
        except Exception:
            continue
        lines = content.splitlines()
        title = ""
        for line in lines:
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break
        # 鍦ㄥ唴瀹逛腑鎼滅储
        matches = []
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                matches.append((i + 1, line.strip()))
        if matches:
            results.append({
                "file": kb_file,
                "title": title or kb_file.stem,
                "matches": matches[:5],  # 鏈€澶氭樉绀?5 鏉″尮閰?                "total_matches": len(matches),
            })
    return results


# 鈹€鈹€ 鍛戒护澶勭悊鍑芥暟 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def cmd_status():
    """鏄剧ず鎵€鏈夐樁娈电姸鎬併€?""
    stages = _find_stage_status_files()
    if not stages:
        print("鏈壘鍒伴樁娈电姸鎬佹枃浠讹紙.ai/plan/stage-*/status.md锛?)
        return

    status_order = {
        "planned": 0, "ready_for_code": 1, "auto_running": 2, "coding": 3,
        "ready_for_review": 4, "review_failed": 5, "review_passed": 6,
        "ready_for_test": 7, "test_writing": 8, "testing": 9,
        "bug_found": 10, "bug_fixing": 11, "done": 12, "paused": 13,
    }

    print("AI_Prompt 闃舵鐘舵€佹瑙?)
    print("=" * 72)
    print(f"{'闃舵':<12} {'鐘舵€?:<18} {'璐ｄ换 Agent':<14} {'鏇存柊鏃堕棿':<16}")
    print("-" * 72)

    done_count = 0
    active_count = 0
    for stage_name, status_path in stages:
        info = _read_status_md(status_path)
        if info is None:
            print(f"{stage_name:<12} {'鏃犳硶璇诲彇':<18}")
            continue
        status = info.get("鐘舵€?, "?")
        agent = info.get("褰撳墠璐ｄ换 Agent", "?")
        updated = info.get("鏇存柊鏃堕棿", "?")
        status_display = {
            "done": "鉁?done",
            "review_passed": "鉁?review_passed",
            "review_failed": "鉂?review_failed",
            "paused": "鈴革笍 paused",
            "ready_for_code": "馃搵 ready_for_code",
            "ready_for_review": "馃搵 ready_for_review",
            "coding": "馃敡 coding",
            "review": "馃攳 review",
        }.get(status, f"  {status}")

        status_padding = 18 - len(status.replace("鉁?", "").replace("鉂?", "").replace("鈴革笍 ", "").replace("馃搵 ", "").replace("馃敡 ", "").replace("馃攳 ", ""))
        print(f"{stage_name:<12} {status_display:<24} {agent:<14} {updated:<16}")
        if status in ("done", "review_passed"):
            done_count += 1
        else:
            active_count += 1

    print("-" * 72)
    total = len(stages)
    print(f"鍏?{total} 涓樁娈碉細{done_count} 宸插畬鎴愶紝{active_count} 杩涜涓?寰呭鐞?)
    print()


def cmd_review():
    """鍒楀嚭寰呭鐞嗗鏌ユ潯鐩€?""
    reviews = _find_review_files()
    if not reviews:
        print("鏈壘鍒板緟澶勭悊瀹℃煡鏉＄洰")
        return

    total = 0
    print("寰呭鐞嗗鏌ユ潯鐩?)
    print("=" * 60)
    for stage, items in sorted(reviews.items()):
        print(f"\n[{stage}]")
        for item in items:
            tag = {"pending": "鈴?, "fixing": "馃敡", "resolved": "鉁?}.get(item["status"], "?")
            print(f"  {tag} [{item['status']}] {item['title']}")
            total += 1

    print(f"\n鍏?{total} 鏉″緟澶勭悊瀹℃煡")


def cmd_bugs():
    """鍒楀嚭寰呭鐞?Bug銆?""
    bugs = _find_bug_files()
    if not bugs:
        print("鏈壘鍒板緟澶勭悊 Bug")
        return

    total = 0
    print("寰呭鐞?Bug")
    print("=" * 60)
    for module, items in sorted(bugs.items()):
        print(f"\n[{module}]")
        for item in items:
            tag = {"open": "馃悰", "fixing": "馃敡", "resolved": "鉁?}.get(item["status"], "?")
            print(f"  {tag} [{item['status']}] {item['title']}")
            total += 1

    print(f"\n鍏?{total} 鏉″緟澶勭悊 Bug")


def cmd_log():
    """鏄剧ず鏈€杩戞棩蹇楁憳瑕併€?""
    entries = _read_recent_logs()
    if not entries:
        print("鏈壘鍒版棩蹇楁潯鐩?)
        return

    print("鏈€杩戞棩蹇楁憳瑕?)
    print("=" * 60)
    for entry in entries[:20]:
        print(f"  {entry}")
    print()


def cmd_kb_search(query):
    """鎼滅储鐭ヨ瘑搴撱€?""
    print(f"鎼滅储鐭ヨ瘑搴擄細\"{query}\"")
    print("=" * 60)

    # 棣栧厛灏濊瘯鍚戦噺鎼滅储锛堝鏋滃彲鐢級锛屽惁鍒欏洖閫€鍒版枃鏈尮閰?    vector_search_available = False
    try:
        import numpy
        vector_search_available = True
    except ImportError:
        pass

    if not vector_search_available:
        print("[鎻愮ず] 鍚戦噺绱㈠紩鏈惎鐢紝浣跨敤绾枃鏈尮閰嶆ā寮忋€?)
        print("  瀹夎 numpy + sentence-transformers 鍙惎鐢ㄨ涔夋悳绱€俓n")

    results = _search_kb(query)

    if not results:
        print("鏈壘鍒板尮閰嶇粨鏋溿€?)
        print(f"鐭ヨ瘑搴撶洰褰曪細{KB_DIR}")
        kb_files = [f.name for f in KB_DIR.glob("*.md") if f.name != "index.md"]
        if kb_files:
            print(f"鍙敤鏂囦欢锛歿', '.join(kb_files)}")
        return

    for r in results:
        print(f"\n馃搫 {r['title']}")
        print(f"   鏂囦欢锛歿r['file'].relative_to(PROJECT_ROOT)}")
        print(f"   鍖归厤 {r['total_matches']} 澶勶細")
        for lineno, line in r["matches"]:
            # 鎴柇杩囬暱琛?            display = line[:100] + "..." if len(line) > 100 else line
            print(f"   L{lineno:>3}: {display}")
    print()


def cmd_kb_list():
    """鍒楀嚭鐭ヨ瘑搴撴枃浠躲€?""
    if not KB_DIR.is_dir():
        print("鐭ヨ瘑搴撶洰褰曚笉瀛樺湪")
        return

    files = sorted(KB_DIR.glob("*.md"))
    if not files:
        print("鐭ヨ瘑搴撲负绌?)
        return

    print("鐭ヨ瘑搴撴枃浠?)
    print("=" * 60)
    for f in files:
        if f.name == "index.md":
            continue
        content = f.read_text(encoding="utf-8")
        title = ""
        for line in content.splitlines():
            if line.startswith("# "):
                title = line.lstrip("# ").strip()
                break
        size = len(content.splitlines())
        print(f"  馃搫 {title or f.stem}  ({size} 琛?  [{f.name}]")
    print()


# 鈹€鈹€ 涓诲嚱鏁?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return
    if args.command == "status":
        cmd_status()
    elif args.command == "review":
        cmd_review()
    elif args.command == "bugs":
        cmd_bugs()
    elif args.command == "log":
        cmd_log()
    elif args.command == "kb":
        if args.kb_command is None:
            print("璇锋寚瀹?kb 瀛愬懡浠わ細search 鎴?list")
            print("  ai kb search <鍏抽敭璇?")
            print("  ai kb list")
            return
        if args.kb_command == "search":
            cmd_kb_search(args.query)
        elif args.kb_command == "list":
            cmd_kb_list()


if __name__ == "__main__":
    main()
