# deploy/kilo.py
# AI_Prompt 部署脚本 — Kilo 适配器

from pathlib import Path
from .common import report, copy_files, deploy_resources

KILO_FILES = {
    "Kilo/agents/architect.md": ".kilo/agents/architect.md",
    "Kilo/agents/auto-runner.md": ".kilo/agents/auto-runner.md",
    "Kilo/agents/code.md": ".kilo/agents/code.md",
    "Kilo/agents/code-worker.md": ".kilo/agents/code-worker.md",
    "Kilo/agents/ask.md": ".kilo/agents/ask.md",
    "Kilo/agents/debug.md": ".kilo/agents/debug.md",
    "Kilo/agents/review-worker.md": ".kilo/agents/review-worker.md",
    "Kilo/agents/tester.md": ".kilo/agents/tester.md",
    "Kilo/agents/test-writer.md": ".kilo/agents/test-writer.md",
}

KILO_DIRS = [
    ".kilo/agents",
    ".kilo/instructions",
    ".kilo/skills",
]

KILO_JSONC_CONTENT = """\
{
  "$schema": "https://app.kilo.ai/config.json",
  "default_agent": "code",
  "instructions": [
    "AGENTS.md",
    ".kilo/instructions/core.md"
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
    path = target / "kilo.jsonc"
    if path.exists():
        return [report("skipped", "kilo.jsonc", "已存在")]
    path.write_text(KILO_JSONC_CONTENT, encoding="utf-8")
    return [report("created", "kilo.jsonc")]


def deploy_kilo(source: Path, target: Path) -> list[str]:
    """部署 Kilo：通用资源 → .kilo/ 下，Agent → .kilo/agents/"""
    lines = []
    lines.append("\n[Kilo]")
    lines.append("  [通用资源 → .kilo/]")

    # Instructions + Skills 部署到 .kilo/
    res_lines, rc, rs = deploy_resources(source, target, ".kilo")
    lines.extend(res_lines)
    lines.append(report("info", f"资源: 复制 {rc}, 跳过 {rs}"))

    # Agent 定义
    lines.append("  [Agent 定义 → .kilo/agents/]")
    a_lines, ac, as_skip, am = copy_files(source, target, KILO_FILES)
    lines.extend(a_lines)
    lines.append(report("info", f"Agent: 复制 {ac}, 跳过 {as_skip}" + (f", 缺失 {am}" if am else "")))

    lines.append("\n[Kilo 配置]")
    lines.extend(configure_kilo_jsonc(target))
    return lines
