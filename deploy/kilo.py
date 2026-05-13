# deploy/kilo.py
# AI_Prompt 部署脚本 — Kilo 适配器

from pathlib import Path
from .common import report, copy_files

KILO_FILES = {
    "Kilo/Instructions/kilo_instructions_core.md": ".kilo/Instructions/kilo_instructions_core.md",
    "Kilo/agents/architect.md": ".kilo/agents/architect.md",
    "Kilo/agents/auto-runner.md": ".kilo/agents/auto-runner.md",
    "Kilo/agents/code.md": ".kilo/agents/code.md",
    "Kilo/agents/code-worker.md": ".kilo/agents/code-worker.md",
    "Kilo/agents/ask.md": ".kilo/agents/ask.md",
    "Kilo/agents/debug.md": ".kilo/agents/debug.md",
    "Kilo/agents/review-worker.md": ".kilo/agents/review-worker.md",
    "Kilo/agents/tester.md": ".kilo/agents/tester.md",
    "Kilo/agents/test-writer.md": ".kilo/agents/test-writer.md",
    "Kilo/skills/bug-acceptance/SKILL.md": ".kilo/skills/bug-acceptance/SKILL.md",
    "Kilo/skills/get-bugs/SKILL.md": ".kilo/skills/get-bugs/SKILL.md",
    "Kilo/skills/check-kb/SKILL.md": ".kilo/skills/check-kb/SKILL.md",
    "Kilo/skills/sync-status/SKILL.md": ".kilo/skills/sync-status/SKILL.md",
    "Kilo/skills/get-stage-status/SKILL.md": ".kilo/skills/get-stage-status/SKILL.md",
    "Kilo/skills/update-stage-status/SKILL.md": ".kilo/skills/update-stage-status/SKILL.md",
}

KILO_DIRS = [
    ".kilo/Instructions",
    ".kilo/agents",
    ".kilo/skills/bug-acceptance",
    ".kilo/skills/get-bugs",
    ".kilo/skills/check-kb",
    ".kilo/skills/sync-status",
    ".kilo/skills/get-stage-status",
    ".kilo/skills/update-stage-status",
]

KILO_JSONC_CONTENT = """\
{
  "$schema": "https://app.kilo.ai/config.json",
  "default_agent": "code",
  "instructions": [
    "AGENTS.md",
    ".kilo/Instructions/kilo_instructions_core.md"
  ],
  "skills": {
    "get-bugs": ".kilo/skills/get-bugs",
    "check-kb": ".kilo/skills/check-kb",
    "bug-acceptance": ".kilo/skills/bug-acceptance",
    "sync-status": ".kilo/skills/sync-status",
    "get-stage-status": ".kilo/skills/get-stage-status",
    "update-stage-status": ".kilo/skills/update-stage-status"
  },
  "experimental": {
    "agent_manager_tool": true
  }
}
"""


def configure_kilo_jsonc(target: Path) -> list[str]:
    """生成 kilo.jsonc（如不存在）。"""
    path = target / "kilo.jsonc"
    if path.exists():
        return [report("skipped", "kilo.jsonc", "已存在")]
    path.write_text(KILO_JSONC_CONTENT, encoding="utf-8")
    return [report("created", "kilo.jsonc")]


def deploy_kilo(source: Path, target: Path) -> list[str]:
    """部署 Kilo 适配器文件，返回报告行列表。"""
    lines = []
    lines.append("\n[Kilo 适配器]")
    k_lines, kc, ks, km = copy_files(source, target, KILO_FILES)
    lines.extend(k_lines)
    lines.append(report("info", f"Kilo 文件: 复制 {kc}, 跳过 {ks}" + (f", 缺失 {km}" if km else "")))

    lines.append("\n[Kilo 配置]")
    lines.extend(configure_kilo_jsonc(target))
    return lines
