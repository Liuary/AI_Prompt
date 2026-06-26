# deploy/opencode.py
# AI_Prompt 部署脚本 — OpenCode 适配器

from pathlib import Path
from .common import report, copy_files, deploy_resources

OPENCODE_FILES = {
    "adapters/opencode/agents/architect.md": ".opencode/agents/architect.md",
    "adapters/opencode/agents/auto-runner.md": ".opencode/agents/auto-runner.md",
    "adapters/opencode/agents/code.md": ".opencode/agents/code.md",
    "adapters/opencode/agents/code-worker.md": ".opencode/agents/code-worker.md",
    "adapters/opencode/agents/ask.md": ".opencode/agents/ask.md",
    "adapters/opencode/agents/debug.md": ".opencode/agents/debug.md",
    "adapters/opencode/agents/review-worker.md": ".opencode/agents/review-worker.md",
    "adapters/opencode/agents/tester.md": ".opencode/agents/tester.md",
    "adapters/opencode/agents/test-writer.md": ".opencode/agents/test-writer.md",
    "adapters/opencode/instructions/core.md": ".opencode/instructions/core.md",
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
    "update-stage-status": ".opencode/skills/update-stage-status",
    "search-kb": ".opencode/skills/search-kb"
  },
  "experimental": {
    "agent_manager_tool": false
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
    """部署 OpenCode 专用 Agent 和通用资源到 .opencode/ 下"""
    lines = []
    lines.append("\n[OpenCode]")

    # Agent 定义 + 专用指令（先部署，确保 OpenCode 专用 core.md 不被通用版覆盖）
    lines.append("  [Agent 定义 + 指令 → .opencode/]")
    a_lines, ac, as_skip, am = copy_files(source, target, OPENCODE_FILES)
    lines.extend(a_lines)
    lines.append(report("info", f"Agent: 复制 {ac}, 跳过 {as_skip}" + (f", 缺失 {am}" if am else "")))

    # 通用 Skills 部署到 .opencode/
    lines.append("  [通用 Skills → .opencode/]")
    res_lines, rc, rs = deploy_resources(source, target, ".opencode")
    lines.extend(res_lines)
    lines.append(report("info", f"Skills: 复制 {rc}, 跳过 {rs}"))

    lines.append("\n[OpenCode 配置]")
    lines.extend(configure_opencode_jsonc(target))
    return lines
