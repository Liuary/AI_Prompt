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
    """部署 GitHub Copilot 适配器。"""
    lines = []
    lines.append("\n[GitHub Copilot 适配器]")
    p_lines, pc, ps, pm = copy_files(source, target, COPILOT_FILES)
    lines.extend(p_lines)
    lines.append(report("info", f"Copilot 文件: 复制 {pc}, 跳过 {ps}" + (f", 缺失 {pm}" if pm else "")))
    return lines
