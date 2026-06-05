# deploy/opencode.py
# AI_Prompt 部署脚本 — OpenCode 适配器

from pathlib import Path
from .common import report, copy_files, deploy_resources

OPENCODE_FILES = {
    "adapters/kilo/agents/architect.md": ".opencode/agents/architect.md",
    "adapters/kilo/agents/auto-runner.md": ".opencode/agents/auto-runner.md",
    "adapters/kilo/agents/code.md": ".opencode/agents/code.md",
    "adapters/kilo/agents/code-worker.md": ".opencode/agents/code-worker.md",
    "adapters/kilo/agents/ask.md": ".opencode/agents/ask.md",
    "adapters/kilo/agents/debug.md": ".opencode/agents/debug.md",
    "adapters/kilo/agents/review-worker.md": ".opencode/agents/review-worker.md",
    "adapters/kilo/agents/tester.md": ".opencode/agents/tester.md",
    "adapters/kilo/agents/test-writer.md": ".opencode/agents/test-writer.md",
}

OPENCODE_DIRS = [
    ".opencode/agents",
    ".opencode/instructions",
    ".opencode/skills",
]

OPENCODE_JSONC_CONTENT = """\
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "code",
  "instructions": [
    "AGENTS.md",
    ".opencode/instructions/core.md"
  ],
  "skills": {
    "get-bugs": ".opencode/skills/get-bugs",
    "check-kb": ".opencode/skills/check-kb",
    "bug-acceptance": ".opencode/skills/bug-acceptance",
    "sync-status": ".opencode/skills/sync-status",
    "get-stage-status": ".opencode/skills/get-stage-status",
    "update-stage-status": ".opencode/skills/update-stage-status"
  },
  "experimental": {
    "agent_manager_tool": true
  }
}
"""


def configure_opencode_jsonc(target: Path) -> list[str]:
    path = target / "opencode.jsonc"
    if path.exists():
        return [report("skipped", "opencode.jsonc", "已存在")]
    path.write_text(OPENCODE_JSONC_CONTENT, encoding="utf-8")
    return [report("created", "opencode.jsonc")]


def deploy_opencode(source: Path, target: Path) -> list[str]:
    """部署 Kilo：通用资源 → .opencode/ 下，Agent → .opencode/agents/"""
    lines = []
    lines.append("\n[OpenCode]")
    lines.append("  [通用资源 → .opencode/]")

    # Instructions + Skills 部署到 .opencode/
    res_lines, rc, rs = deploy_resources(source, target, ".opencode")
    lines.extend(res_lines)
    lines.append(report("info", f"资源: 复制 {rc}, 跳过 {rs}"))

    # Agent 定义
    lines.append("  [Agent 定义 → .opencode/agents/]")
    a_lines, ac, as_skip, am = copy_files(source, target, OPENCODE_FILES)
    lines.extend(a_lines)
    lines.append(report("info", f"Agent: 复制 {ac}, 跳过 {as_skip}" + (f", 缺失 {am}" if am else "")))

    lines.append("\n[OpenCode 配置]")
    lines.extend(configure_opencode_jsonc(target))
    return lines
