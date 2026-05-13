# deploy/deepcode.py
# AI_Prompt 部署脚本 — Deep Code CLI 适配器

import shutil
from pathlib import Path
from .common import report, copy_files

DEEPCODE_FILES = {
    "adapters/deepcode/skills/check-kb/SKILL.md": ".agents/skills/check-kb/SKILL.md",
    "adapters/deepcode/skills/get-bugs/SKILL.md": ".agents/skills/get-bugs/SKILL.md",
    "adapters/deepcode/skills/bug-acceptance/SKILL.md": ".agents/skills/bug-acceptance/SKILL.md",
    "adapters/deepcode/skills/get-stage-status/SKILL.md": ".agents/skills/get-stage-status/SKILL.md",
    "adapters/deepcode/skills/update-stage-status/SKILL.md": ".agents/skills/update-stage-status/SKILL.md",
}

DEEPCODE_DIRS = [
    ".agents/skills/check-kb",
    ".agents/skills/get-bugs",
    ".agents/skills/bug-acceptance",
    ".agents/skills/get-stage-status",
    ".agents/skills/update-stage-status",
    ".deepcode",
]


def configure_deepcode_agents_md(source: Path, target: Path) -> list[str]:
    """部署 AGENTS.md 到 .deepcode/。"""
    lines = []
    src_path = source / "adapters" / "deepcode" / "AGENTS.md"
    dst_path = target / ".deepcode" / "AGENTS.md"

    if not src_path.exists():
        lines.append(report("warning", ".deepcode/AGENTS.md", "源文件不存在"))
        return lines

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if dst_path.exists():
        lines.append(report("skipped", ".deepcode/AGENTS.md", "已存在"))
    else:
        shutil.copy2(src_path, dst_path)
        lines.append(report("created", ".deepcode/AGENTS.md"))
    return lines


def deploy_deepcode(source: Path, target: Path) -> list[str]:
    """部署 Deep Code CLI 适配器。"""
    lines = []
    lines.append("\n[Deep Code CLI 适配器]")
    d_lines, dc, ds, dm = copy_files(source, target, DEEPCODE_FILES)
    lines.extend(d_lines)
    lines.append(report("info", f"DeepCode 文件: 复制 {dc}, 跳过 {ds}" + (f", 缺失 {dm}" if dm else "")))

    lines.append("\n[DeepCode .deepcode/]")
    lines.extend(configure_deepcode_agents_md(source, target))
    return lines
