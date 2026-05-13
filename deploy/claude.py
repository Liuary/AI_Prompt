# deploy/claude.py
# AI_Prompt 部署脚本 — Claude Code 适配器

from pathlib import Path
from .common import report, copy_files, deploy_resources

CLAUDE_FILES = {
    "adapters/claude-code/CLAUDE.md": "CLAUDE.md",
    ".claude/commands/rule-compile.md": ".claude/commands/rule-compile.md",
    ".claude/commands/rule-validate.md": ".claude/commands/rule-validate.md",
}

CLAUDE_DIRS = [
    ".claude/commands",
    ".claude/instructions",
    ".claude/skills",
]


def deploy_claude(source: Path, target: Path) -> list[str]:
    """部署 Claude：通用资源 → .claude/ 下，适配器文件 → 项目根"""
    lines = []
    lines.append("\n[Claude Code]")
    lines.append("  [通用资源 → .claude/]")

    res_lines, rc, rs = deploy_resources(source, target, ".claude")
    lines.extend(res_lines)
    lines.append(report("info", f"资源: 复制 {rc}, 跳过 {rs}"))

    lines.append("  [Claude 适配器]")
    c_lines, cc, cs, cm = copy_files(source, target, CLAUDE_FILES)
    lines.extend(c_lines)
    lines.append(report("info", f"适配器: 复制 {cc}, 跳过 {cs}" + (f", 缺失 {cm}" if cm else "")))
    return lines
