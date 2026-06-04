# deploy/__init__.py
# AI_Prompt 部署脚本 — 主入口

import shutil
import sys
from pathlib import Path

from .cli import build_parser, show_help, show_list, resolve_tool
from .common import (
    report, create_directories, copy_files,
    configure_gitignore, configure_info_json, configure_config_yaml, configure_config_yaml_with_backend, generate_workspace,
    VECTOR_SCRIPTS, VECTOR_DEPENDENCY_NOTICE,
)
from .kilo import KILO_DIRS, deploy_kilo
from .deepcode import DEEPCODE_DIRS, deploy_deepcode
from .claude import CLAUDE_DIRS, deploy_claude
from .copilot import COPILOT_DIRS, deploy_copilot
from .opencode import OPENCODE_DIRS, deploy_opencode

TOOLS = {
    "kilo":    {"dirs": KILO_DIRS,    "label": "Kilo",           "fn": deploy_kilo,    "tip": "重启 Kilo 会话后 Subagent 和 Skill 生效。"},
    "deepcode":{"dirs": DEEPCODE_DIRS, "label": "Deep Code CLI", "fn": deploy_deepcode, "tip": "启动 Deep Code CLI 后使用 /skills 查看可用 Skill。"},
    "claude":  {"dirs": CLAUDE_DIRS,  "label": "Claude Code",    "fn": deploy_claude,   "tip": "Claude Code 同时加载 CLAUDE.md 和 AGENTS.md。"},
    "copilot": {"dirs": COPILOT_DIRS, "label": "GitHub Copilot", "fn": deploy_copilot,  "tip": "GitHub Copilot 将自动读取 .github/copilot-instructions.md。"},
    "opencode":{"dirs": OPENCODE_DIRS, "label": "OpenCode",       "fn": deploy_opencode, "tip": "重启 OpenCode 会话后 Subagent 和 Skill 生效。"},
}