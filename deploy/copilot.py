# deploy/copilot.py
# AI_Prompt 部署脚本 — GitHub Copilot 适配器

from pathlib import Path
from .common import report, copy_files, deploy_resources

COPILOT_FILES = {
    "adapters/copilot/copilot-instructions.md": ".github/copilot-instructions.md",
}

COPILOT_DIRS = [
    ".github",
    ".github/instructions",
    ".github/skills",
]


def deploy_copilot(source: Path, target: Path) -> list[str]:
    """部署 Copilot：通用资源 → .github/ 下，适配器文件 → .github/"""
    lines = []
    lines.append("\n[GitHub Copilot]")
    lines.append("  [通用资源 → .github/]")

    res_lines, rc, rs = deploy_resources(source, target, ".github")
    lines.extend(res_lines)
    lines.append(report("info", f"资源: 复制 {rc}, 跳过 {rs}"))

    lines.append("  [Copilot 适配器]")
    c_lines, cc, cs, cm = copy_files(source, target, COPILOT_FILES)
    lines.extend(c_lines)
    lines.append(report("info", f"适配器: 复制 {cc}, 跳过 {cs}" + (f", 缺失 {cm}" if cm else "")))
    return lines
