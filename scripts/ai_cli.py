#!/usr/bin/env python3
# scripts/ai_cli.py
# AI_Prompt unified CLI tool — workspace status query and knowledge base search
# Usage:
#   python scripts/ai_cli.py status             Show all stage statuses
#   python scripts/ai_cli.py review             List pending review items
#   python scripts/ai_cli.py bugs               List pending bugs
#   python scripts/ai_cli.py log                Show recent log summary
#   python scripts/ai_cli.py kb search <query>  Search knowledge base
import argparse
import os
import re
import sys
from pathlib import Path
from datetime import datetime


# ─── Project Root Detection ───

def _find_project_root() -> Path:
    """Walk up to find the project root (directory containing .ai/)."""
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


# ─── CLI Argument Parsing ───

def build_parser():
    parser = argparse.ArgumentParser(
        prog="ai",
        description="AI_Prompt unified CLI — workspace status and knowledge base search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ai status                  Show all stage statuses
  ai review                  List pending review items
  ai bugs                    List pending bugs
  ai log                     Show recent log summary
  ai kb search <keyword>     Search knowledge base
  ai kb list                 List knowledge base files
        """,
    )

    sub = parser.add_subparsers(dest="command", help="subcommand")

    # status
    sub.add_parser("status", help="Show all stage statuses")

    # review
    sub.add_parser("review", help="List pending review items")

    # bugs
    sub.add_parser("bugs", help="List pending bugs")

    # log
    sub.add_parser("log", help="Show recent log summary")

    # kb
    kb_parser = sub.add_parser("kb", help="Knowledge base operations")
    kb_sub = kb_parser.add_subparsers(dest="kb_command", help="Knowledge base subcommand")

    kb_search = kb_sub.add_parser("search", help="Search knowledge base")
    kb_search.add_argument("query", help="search query")

    kb_sub.add_parser("list", help="List knowledge base files")

    return parser


# ─── Helper Functions ───

def _read_status_md(filepath: Path) -> dict:
    """Read status.md and extract structured fields."""
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding="utf-8")
    info = {}
    patterns = {
        "execution_mode": r"-\s+\*\*执行模式\*\*[：:]\s*(.+)",
        "auto_advance": r"-\s+\*\*自动推进\*\*[：:]\s*(.+)",
        "status": r"-\s+\*\*状态\*\*[：:]\s*(.+)",
        "current_agent": r"-\s+\*\*当前责任 Agent\*\*[：:]\s*(.+)",
        "previous_agent": r"-\s+\*\*上一责任 Agent\*\*[：:]\s*(.+)",
        "update_time": r"-\s+\*\*更新时间\*\*[：:]\s*(.+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, content)
        if m:
            info[key] = m.group(1).strip()
    return info


def _find_stage_status_files() -> list:
    """Find all stage-*/status.md files."""
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
    """Find private review files, return {stage: [{file, title, status}]}."""
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
            # check status label
            status_match = re.search(r"-\s+\*\*状态\*\*[：:]\s*(pending|fixing|resolved|closed)", content)
            if not status_match:
                continue
            status = status_match.group(1)
            if status == "closed":
                continue
            # read title
            title_match = re.search(r"##\s+REV-\d+[：:]\s*(.+)", content)
            title = title_match.group(1).strip() if title_match else rev_file.stem
            if stage not in reviews:
                reviews[stage] = []
            reviews[stage].append({"file": rev_file, "title": title, "status": status})
    return reviews


def _find_bug_files() -> dict:
    """Find private bug files, return {module: [{file, title, status}]}."""
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
                status_match = re.search(r"-\s+\*\*状态\*\*[：:]\s*(open|fixing|resolved|closed)", content)
                if not status_match:
                    continue
                status = status_match.group(1)
                if status == "closed":
                    continue
                title_match = re.search(r"##\s+BUG-\d+[：:]\s*(.+)", content)
                title = title_match.group(1).strip() if title_match else bug_file.stem
                module = module_dir.name
                if module not in bugs:
                    bugs[module] = []
                bugs[module].append({"file": bug_file, "title": title, "status": status})
    return bugs


def _read_recent_logs(limit: int = 30) -> list:
    """Read recent public log entries."""
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
    """Search knowledge base files (plain text match, no vector index dependency)."""
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
        # search in content
        matches = []
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                matches.append((i + 1, line.strip()))
        if matches:
            results.append({
                "file": kb_file,
                "title": title or kb_file.stem,
                "matches": matches[:5],  # show at most 5 matches
                "total_matches": len(matches),
            })
    return results


# ─── Command Handlers ───

def cmd_status():
    """Show all stage statuses."""
    stages = _find_stage_status_files()
    if not stages:
        print("No stage status files found (.ai/plan/stage-*/status.md)")
        return

    status_order = {
        "planned": 0, "ready_for_code": 1, "auto_running": 2, "coding": 3,
        "ready_for_review": 4, "review_failed": 5, "review_passed": 6,
        "ready_for_test": 7, "test_writing": 8, "testing": 9,
        "bug_found": 10, "bug_fixing": 11, "done": 12, "paused": 13,
    }

    print("AI_Prompt Stage Status Overview")
    print("=" * 72)
    print(f"{'Stage':<12} {'Status':<18} {'Agent':<14} {'Updated':<16}")
    print("-" * 72)

    done_count = 0
    active_count = 0
    for stage_name, status_path in stages:
        info = _read_status_md(status_path)
        if info is None:
            print(f"{stage_name:<12} {'unreadable':<18}")
            continue
        status = info.get("status", "?")
        agent = info.get("current_agent", "?")
        updated = info.get("update_time", "?")
        status_display = {
            "done": "✅ done",
            "review_passed": "✅ review_passed",
            "review_failed": "❌ review_failed",
            "paused": "⏸️ paused",
            "ready_for_code": "📋 ready_for_code",
            "ready_for_review": "📋 ready_for_review",
            "coding": "🔨 coding",
            "review": "🔍 review",
        }.get(status, f"  {status}")

        status_padding = 18 - len(status.replace("✅", "").replace("❌", "").replace("⏸️ ", "").replace("📋 ", "").replace("🔨 ", "").replace("🔍 ", ""))
        print(f"{stage_name:<12} {status_display:<24} {agent:<14} {updated:<16}")
        if status in ("done", "review_passed"):
            done_count += 1
        else:
            active_count += 1

    print("-" * 72)
    total = len(stages)
    print(f"Total {total} stages: {done_count} done, {active_count} active/pending")
    print()


def cmd_review():
    """List pending review items."""
    reviews = _find_review_files()
    if not reviews:
        print("No pending review items found")
        return

    total = 0
    print("Pending Review Items")
    print("=" * 60)
    for stage, items in sorted(reviews.items()):
        print(f"\n[{stage}]")
        for item in items:
            tag = {"pending": "⏸", "fixing": "🔨", "resolved": "✅"}.get(item["status"], "?")
            print(f"  {tag} [{item['status']}] {item['title']}")
            total += 1

    print(f"\nTotal {total} pending review items")


def cmd_bugs():
    """List pending bugs."""
    bugs = _find_bug_files()
    if not bugs:
        print("No pending bugs found")
        return

    total = 0
    print("Pending Bugs")
    print("=" * 60)
    for module, items in sorted(bugs.items()):
        print(f"\n[{module}]")
        for item in items:
            tag = {"open": "🐛", "fixing": "🔨", "resolved": "✅"}.get(item["status"], "?")
            print(f"  {tag} [{item['status']}] {item['title']}")
            total += 1

    print(f"\nTotal {total} pending bugs")


def cmd_log():
    """Show recent log summary."""
    entries = _read_recent_logs()
    if not entries:
        print("No log entries found")
        return

    print("Recent Log Summary")
    print("=" * 60)
    for entry in entries[:20]:
        print(f"  {entry}")
    print()


def cmd_kb_search(query):
    """Search knowledge base."""
    print(f'Searching knowledge base: "{query}"')
    print("=" * 60)

    # First try vector search (if available), otherwise fall back to text match
    vector_search_available = False
    try:
        import numpy
        vector_search_available = True
    except ImportError:
        pass

    if not vector_search_available:
        print("[Notice] Vector index not enabled, using plain text match mode.")
        print("  Install numpy + sentence-transformers to enable semantic search.\n")

    results = _search_kb(query)

    if not results:
        print("No matching results found.")
        print(f"Knowledge base directory: {KB_DIR}")
        kb_files = [f.name for f in KB_DIR.glob("*.md") if f.name != "index.md"]
        if kb_files:
            print(f"Available files: {', '.join(kb_files)}")
        return

    for r in results:
        print(f"\n📄 {r['title']}")
        print(f"   File: {r['file'].relative_to(PROJECT_ROOT)}")
        print(f"   {r['total_matches']} matches:")
        for lineno, line in r["matches"]:
            # truncate long lines
            display = line[:100] + "..." if len(line) > 100 else line
            print(f"   L{lineno:>3}: {display}")
    print()


def cmd_kb_list():
    """List knowledge base files."""
    if not KB_DIR.is_dir():
        print("Knowledge base directory does not exist")
        return

    files = sorted(KB_DIR.glob("*.md"))
    if not files:
        print("Knowledge base is empty")
        return

    print("Knowledge Base Files")
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
        print(f"  📄 {title or f.stem}  ({size} lines)  [{f.name}]")
    print()


# ─── Main ───

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
            print("Please specify kb subcommand: search or list")
            print("  ai kb search <query>")
            print("  ai kb list")
            return
        if args.kb_command == "search":
            cmd_kb_search(args.query)
        elif args.kb_command == "list":
            cmd_kb_list()


if __name__ == "__main__":
    main()
