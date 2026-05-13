# deploy/claude.py
# AI_Prompt 部署脚本 — Claude Code 适配器

from pathlib import Path
from .common import report, copy_files

CLAUDE_FILES = {
    "adapters/claude-code/CLAUDE.md": "CLAUDE.md",
    ".claude/commands/rule-compile.md": ".claude/commands/rule-compile.md",
    ".claude/commands/rule-validate.md": ".claude/commands/rule-validate.md",
}

CLAUDE_DIRS = [
    ".claude/commands",
]


def deploy_claude(source: Path, target: Path) -> list[str]:
    """部署 Claude Code 适配器。"""
    lines = []
    lines.append("\n[Claude Code 适配器]")
    c_lines, cc, cs, cm = copy_files(source, target, CLAUDE_FILES)
    lines.extend(c_lines)
    lines.append(report("info", f"Claude Code 文件: 复制 {cc}, 跳过 {cs}" + (f", 缺失 {cm}" if cm else "")))
    return lines
