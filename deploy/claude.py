# deploy/claude.py
# AI_Prompt 部署脚本 — Claude Code 适配器

from pathlib import Path
from .common import report, copy_files, deploy_resources

CLAUDE_FILES = {
    "adapters/claude-code/CLAUDE.md": ".claude/CLAUDE.md",
}

CLAUDE_AGENT_FILES = {
    "adapters/claude-code/agents/architect.json": ".claude/agents/architect.json",
    "adapters/claude-code/agents/code.json": ".claude/agents/code.json",
    "adapters/claude-code/agents/debug.json": ".claude/agents/debug.json",
    "adapters/claude-code/agents/tester.json": ".claude/agents/tester.json",
}

CLAUDE_DIRS = [
    ".claude/rules",
    ".claude/skills",
    ".claude/agents",
]


def deploy_claude(source: Path, target: Path) -> list[str]:
    """部署 Claude Code。全部放在 .claude/ 下。"""
    lines = []
    lines.append("\n[Claude Code]")

    lines.append("  [.claude/CLAUDE.md]")
    c_lines, cc, cs, cm = copy_files(source, target, CLAUDE_FILES)
    lines.extend(c_lines)

    res_lines, rc, rs = deploy_resources(source, target, ".claude", rules_dir="rules")
    lines.extend(res_lines)

    lines.append("  [.claude/agents/]")
    a_lines, ac, a_skip, am = copy_files(source, target, CLAUDE_AGENT_FILES)
    lines.extend(a_lines)
    lines.append(report("info", f"Agent: 复制 {ac}, 跳过 {a_skip}" + (f", 缺失 {am}" if am else "")))

    total = cc + rc + ac
    skipped = cs + rs + a_skip
    lines.append(report("info", f"总计: 复制 {total}, 跳过 {skipped}" + (f", 缺失 {cm + am}" if cm or am else "")))
    return lines
