# deploy/cli.py
# AI_Prompt 部署脚本 — 命令行解析（与调度逻辑分离）

import argparse
import sys


def show_help():
    """输出自定义帮助信息。"""
    print(r"""AI_Prompt — 跨 AI 工具开发治理模板部署脚本
============================================

用法:
  python deploy.py <目标路径> [选项]

选项:
  -k, --kilo          仅部署 Kilo 框架（Agent/Skill/Instructions → .kilo/）
  -d, --deepcode      仅部署 Deep Code CLI 框架（合并版 AGENTS.md + Skill → .agents/）
  -c, --claude        仅部署 Claude Code 适配器（CLAUDE.md + .claude/commands/）
  -p, --copilot       仅部署 GitHub Copilot 适配器（.github/copilot-instructions.md）
  -o, --opencode      仅部署 OpenCode 适配器（Agent/Skill → .opencode/）
  -m, --hermes        仅部署 Hermes (Ollama) 适配器（docker-compose.yml + Modelfile）
  --obsidian          部署 Obsidian Vault 模板（.ai/obsidian/ → 目标项目）
  -l, --list          列出所有支持的 AI 工具
  -h, --help          显示本帮助信息
  --source <路径>     指定模板源路径（默认为脚本所在目录）

不指定工具选项时默认部署全部框架。
项目: https://github.com/Liuary/AI_Prompt""")
    sys.exit(0)


def show_list():
    """输出支持的工具列表。"""
    print("支持的 AI 工具：\n")
    print("  kilo        Kilo — 终端 Agent 工具，支持完整 Agent 角色体系与自动闭环")
    print("  deepcode    Deep Code CLI — 终端 AI 编码助手，通过 Skill + AGENTS.md 提供核心治理能力")
    print("  claude      Claude Code — Anthropic 的终端 Agent 工具，通过 CLAUDE.md + 命令提供治理能力")
    print("  copilot     GitHub Copilot — IDE 内嵌 AI 助手，通过 copilot-instructions.md 提供行为约束")
    print("  opencode    OpenCode — 开源终端 Agent 工具（Kilo 上游），支持完整 Agent 角色体系")
    print("  hermes      Hermes (Ollama) — 本地模型适配器，通过 Ollama 运行 Hermes-3 模型")
    print("\n用法：python deploy.py <目标路径> [-k | -d | -c | -p | -o | -m]")
    print("不指定选项时默认部署全部。")
    sys.exit(0)


def build_parser():
    """构建 argparse 解析器。"""
    parser = argparse.ArgumentParser(
        description="AI_Prompt 模板项目一键部署脚本（多工具支持）",
        add_help=False,
    )
    parser.add_argument("target", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("--source", help=argparse.SUPPRESS, default=None)
    tool_group = parser.add_mutually_exclusive_group()
    tool_group.add_argument("-k", "--kilo",    action="store_true", help=argparse.SUPPRESS)
    tool_group.add_argument("-d", "--deepcode", action="store_true", help=argparse.SUPPRESS)
    tool_group.add_argument("-c", "--claude",   action="store_true", help=argparse.SUPPRESS)
    tool_group.add_argument("-p", "--copilot",  action="store_true", help=argparse.SUPPRESS)
    tool_group.add_argument("-o", "--opencode", action="store_true", help=argparse.SUPPRESS)
    tool_group.add_argument("-m", "--hermes",   action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--obsidian", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-l", "--list", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-h", "--help", action="store_true", help=argparse.SUPPRESS)
    return parser


def resolve_tool(args) -> str:
    """根据命令行参数确定部署工具。"""
    if args.kilo:     return "kilo"
    if args.deepcode: return "deepcode"
    if args.claude:   return "claude"
    if args.copilot:  return "copilot"
    if args.opencode: return "opencode"
    if args.hermes:   return "hermes"
    return "all"


def should_deploy_obsidian(args) -> bool:
    """判断是否需要部署 Obsidian Vault 模板。"""
    return args.obsidian
