# deploy/copilot.py
# AI_Prompt 部署脚本 — GitHub Copilot 适配器

from pathlib import Path
from .common import report, copy_files

COPILOT_FILES = {
    "adapters/copilot/copilot-instructions.md": ".github/copilot-instructions.md",
}

COPILOT_DIRS = [
    ".github",
]


def deploy_copilot(source: Path, target: Path) -> list[str]:
    """部署 GitHub Copilot。仅在 AGENTS.md 之上补充 copilot-instructions.md。"""
    lines = []
    lines.append("\n[GitHub Copilot]")
    c_lines, cc, cs, cm = copy_files(source, target, COPILOT_FILES)
    lines.extend(c_lines)
    lines.append(report("info", f"适配器: 复制 {cc}, 跳过 {cs}" + (f", 缺失 {cm}" if cm else "")))
    return lines
