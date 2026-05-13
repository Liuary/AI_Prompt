# deploy/claude.py
# AI_Prompt 部署脚本 — Claude Code 适配器

from pathlib import Path
from .common import report, copy_files, deploy_resources

CLAUDE_FILES = {
    "adapters/claude-code/CLAUDE.md": ".claude/CLAUDE.md",
}

CLAUDE_DIRS = [
    ".claude/rules",
    ".claude/skills",
]


def deploy_claude(source: Path, target: Path) -> list[str]:
    """部署 Claude Code。全部放在 .claude/ 下，不污染根目录。"""
    lines = []
    lines.append("\n[Claude Code]")

    lines.append("  [.claude/CLAUDE.md]")
    c_lines, cc, cs, cm = copy_files(source, target, CLAUDE_FILES)
    lines.extend(c_lines)

    # instructions → .claude/rules/（Claude 自动加载）
    res_lines, rc, rs = deploy_resources(source, target, ".claude", rules_dir="rules")
    lines.extend(res_lines)
    lines.append(report("info", f"总计: 复制 {cc + rc}, 跳过 {cs + rs}" + (f", 缺失 {cm}" if cm else "")))
    return lines
