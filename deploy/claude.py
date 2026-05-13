# deploy/claude.py
# AI_Prompt 部署脚本 — Claude Code 适配器

from pathlib import Path
from .common import report, copy_files

CLAUDE_FILES = {
    "adapters/claude-code/CLAUDE.md": "CLAUDE.md",
}

CLAUDE_DIRS = []


def deploy_claude(source: Path, target: Path) -> list[str]:
    """部署 Claude Code。CLAUDE.md 补充 AGENTS.md 通用约束。"""
    lines = []
    lines.append("\n[Claude Code]")
    c_lines, cc, cs, cm = copy_files(source, target, CLAUDE_FILES)
    lines.extend(c_lines)
    lines.append(report("info", f"适配器: 复制 {cc}, 跳过 {cs}" + (f", 缺失 {cm}" if cm else "")))
    return lines
