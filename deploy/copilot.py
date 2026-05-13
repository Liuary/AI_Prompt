# deploy/copilot.py
# AI_Prompt 部署脚本 — GitHub Copilot 适配器

from pathlib import Path
from .common import report, copy_files

COPILOT_FILES = {
    "adapters/copilot/copilot-instructions.md": ".github/copilot-instructions.md",
}

COPILOT_INSTRUCTIONS = {
    "adapters/copilot/instructions/workspace.instructions.md": ".github/instructions/workspace.instructions.md",
}

COPILOT_SKILLS = {
    "adapters/copilot/skills/get-bugs/SKILL.md": ".github/skills/get-bugs/SKILL.md",
    "adapters/copilot/skills/check-kb/SKILL.md": ".github/skills/check-kb/SKILL.md",
    "adapters/copilot/skills/bug-acceptance/SKILL.md": ".github/skills/bug-acceptance/SKILL.md",
    "adapters/copilot/skills/sync-status/SKILL.md": ".github/skills/sync-status/SKILL.md",
}

COPILOT_AGENTS = {
    "adapters/copilot/agents/architect.agent.md": ".github/agents/architect.agent.md",
    "adapters/copilot/agents/code.agent.md": ".github/agents/code.agent.md",
    "adapters/copilot/agents/reviewer.agent.md": ".github/agents/reviewer.agent.md",
}

COPILOT_DIRS = [
    ".github",
    ".github/instructions",
    ".github/skills/get-bugs",
    ".github/skills/check-kb",
    ".github/skills/bug-acceptance",
    ".github/skills/sync-status",
    ".github/agents",
]


def deploy_copilot(source: Path, target: Path) -> list[str]:
    """部署 GitHub Copilot：适配层 + Instructions + Skills + Agents。"""
    lines = []
    lines.append("\n[GitHub Copilot]")

    lines.append("  [全局适配层]")
    c_lines, cc, cs, cm = copy_files(source, target, COPILOT_FILES)
    lines.extend(c_lines)

    lines.append("  [文件级 Instructions]")
    i_lines, ic, iskip, im = copy_files(source, target, COPILOT_INSTRUCTIONS)
    lines.extend(i_lines)
    lines.append(report("info", f"Instructions: 复制 {ic}, 跳过 {iskip}" + (f", 缺失 {im}" if im else "")))

    lines.append("  [Skills]")
    s_lines, sc, sskip, sm = copy_files(source, target, COPILOT_SKILLS)
    lines.extend(s_lines)
    lines.append(report("info", f"Skills: 复制 {sc}, 跳过 {sskip}" + (f", 缺失 {sm}" if sm else "")))

    lines.append("  [Agents]")
    a_lines, ac, a_skip, am = copy_files(source, target, COPILOT_AGENTS)
    lines.extend(a_lines)
    lines.append(report("info", f"Agents: 复制 {ac}, 跳过 {a_skip}" + (f", 缺失 {am}" if am else "")))

    total = cc + ic + sc + ac
    skipped = cs + iskip + sskip + a_skip
    lines.append(report("info", f"总计: 复制 {total}, 跳过 {skipped}" + (f", 缺失 {cm + im + sm + am}" if cm or im or sm or am else "")))
    return lines
