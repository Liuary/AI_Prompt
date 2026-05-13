# deploy/kilo.py
# AI_Prompt 部署脚本 — Kilo 适配器（仅 Agent 定义，Instructions/Skills 已提升为通用）

from pathlib import Path
from .common import report, copy_files

# Agent 定义（仅 Kilo 支持 Agent 角色体系）
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
]

KILO_JSONC_CONTENT = """\
{
  "$schema": "https://app.kilo.ai/config.json",
  "default_agent": "code",
  "instructions": [
    "AGENTS.md",
    "instructions/kilo_instructions_core.md"
  ],
  "skills": {
    "get-bugs": "skills/get-bugs",
    "check-kb": "skills/check-kb",
    "bug-acceptance": "skills/bug-acceptance",
    "sync-status": "skills/sync-status",
    "get-stage-status": "skills/get-stage-status",
    "update-stage-status": "skills/update-stage-status"
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
    """部署 Kilo Agent 定义。"""
    lines = []
    lines.append("\n[Kilo Agent]")
    k_lines, kc, ks, km = copy_files(source, target, KILO_FILES)
    lines.extend(k_lines)
    lines.append(report("info", f"Agent: 复制 {kc}, 跳过 {ks}" + (f", 缺失 {km}" if km else "")))

    lines.append("\n[Kilo 配置]")
    lines.extend(configure_kilo_jsonc(target))
    return lines
