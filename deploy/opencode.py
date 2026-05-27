# deploy/opencode.py
# AI_Prompt 部署脚本 — OpenCode 适配器

from pathlib import Path
from .common import report, copy_files

OPENCODE_FILES = {
    "adapters/opencode/opencode.md": ".opencode/opencode.md",
}

OPENCODE_INSTRUCTIONS = {
    "adapters/opencode/instructions/workspace.instructions.md": ".opencode/instructions/workspace.instructions.md",
}

OPENCODE_SKILLS = {
    "adapters/opencode/skills/get-bugs/SKILL.md": ".opencode/skills/get-bugs/SKILL.md",
    "adapters/opencode/skills/check-kb/SKILL.md": ".opencode/skills/check-kb/SKILL.md",
    "adapters/opencode/skills/bug-acceptance/SKILL.md": ".opencode/skills/bug-acceptance/SKILL.md",
    "adapters/opencode/skills/sync-status/SKILL.md": ".opencode/skills/sync-status/SKILL.md",
}

OPENCODE_AGENTS = {
    "adapters/opencode/agents/architect.agent.md": ".opencode/agents/architect.agent.md",
    "adapters/opencode/agents/code.agent.md": ".opencode/agents/code.agent.md",
    "adapters/opencode/agents/tester.agent.md": ".opencode/agents/tester.agent.md",
    "adapters/opencode/agents/debug.agent.md": ".opencode/agents/debug.agent.md",
}

OPENCODE_DIRS = [
    ".opencode",
    ".opencode/instructions",
    ".opencode/skills/get-bugs",
    ".opencode/skills/check-kb",
    ".opencode/skills/bug-acceptance",
    ".opencode/skills/sync-status",
    ".opencode/agents",
]


def deploy_opencode(source: Path, target: Path) -> list[str]:
    """部署 OpenCode：适配层 + Instructions + Skills + Agents。"""
    lines = []
    lines.append("\n[OpenCode]")

    lines.append("  [全局适配层]")
    c_lines, cc, cs, cm = copy_files(source, target, OPENCODE_FILES)
    lines.extend(c_lines)

    lines.append("  [文件级 Instructions]")
    i_lines, ic, iskip, im = copy_files(source, target, OPENCODE_INSTRUCTIONS)
    lines.extend(i_lines)

    lines.append("  [Skills]")
    s_lines, sc, sskip, sm = copy_files(source, target, OPENCODE_SKILLS)
    lines.extend(s_lines)

    lines.append("  [Agents]")
    a_lines, ac, a_skip, am = copy_files(source, target, OPENCODE_AGENTS)
    lines.extend(a_lines)

    total = cc + ic + sc + ac
    lines.append(report("info", f"总计: 复制 {total}, 跳过 {cs + iskip + sskip + a_skip}" +
                 (f", 缺失 {cm + im + sm + am}" if cm or im or sm or am else "")))
    return lines
