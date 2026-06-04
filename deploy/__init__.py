# deploy/__init__.py
# AI_Prompt 部署脚本 — 主入口

import shutil
import sys
from pathlib import Path

from .cli import build_parser, show_help, show_list, resolve_tool, should_deploy_obsidian
from .common import (
    report, create_directories, copy_files,
    configure_gitignore, configure_info_json, configure_config_yaml, generate_workspace,
    OBSIDIAN_RESOURCES,
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


def _configure_agents_md(source, target, tool):
    lines = []
    src_rel = "adapters/deepcode/AGENTS.md" if tool == "deepcode" else "AGENTS.md"
    src_path = source / src_rel
    dst_path = target / "AGENTS.md"
    if not src_path.exists():
        lines.append(report("warning", "AGENTS.md", f"源文件不存在: {src_rel}"))
        return lines
    if dst_path.exists():
        lines.append(report("skipped", "AGENTS.md", "已存在"))
    else:
        shutil.copy2(src_path, dst_path)
        lines.append(report("created", "AGENTS.md"))
    return lines


def _deploy_obsidian_resources(source, target):
    """将 Obsidian Vault 模板复制到目标项目。"""
    lines = []
    lines.append("\n[Obsidian Vault]")
    file_map = {s: s for s in OBSIDIAN_RESOURCES}
    o_lines, copied, skipped, missing = copy_files(source, target, file_map)
    lines.extend(o_lines)
    lines.append(report("info", f"Obsidian: 复制 {copied}, 跳过 {skipped}" + (f", 缺失 {missing}" if missing else "")))
    return lines


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args()

    if args.help:   show_help()
    if args.list:   show_list()

    tool = resolve_tool(args)

    if not args.target:
        print("错误: 需要指定目标项目路径\n")
        print("用法：python deploy.py <目标路径> [-k | -d | -c | -p | -o]")
        print("      python deploy.py --help 查看完整帮助")
        sys.exit(1)

    source = Path(args.source).resolve() if args.source else Path(__file__).resolve().parent.parent
    if not source.exists():
        print(f"错误: 模板源路径不存在: {source}")
        sys.exit(1)

    target = Path(args.target).resolve()
    try:
        target.relative_to(source)
        print("错误: 不允许部署到模板源目录自身或其子目录")
        sys.exit(1)
    except ValueError:
        pass

    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)
    elif not target.is_dir():
        print(f"错误: 目标路径存在但不是目录: {target}")
        sys.exit(1)

    label = "全部工具" if tool == "all" else TOOLS[tool]["label"]
    print(f"\n部署中...")
    print(f"  源:     {source}")
    print(f"  目标:   {target}")
    print(f"  工具:   {label}\n")

    all_lines = []
    targets = list(TOOLS) if tool == "all" else [tool]

    # 目录结构
    tool_dirs = []
    for t in targets:
        tool_dirs.extend(TOOLS[t]["dirs"])
    all_lines.append("[目录结构]")
    all_lines.extend(create_directories(target, tool_dirs))

    # AGENTS.md（第一个工具写入，后续跳过）
    all_lines.append("\n[AGENTS.md]")
    all_lines.extend(_configure_agents_md(source, target, targets[0]))

    # 各工具适配器（各自部署 Instructions + Skills 到自己的目录）
    for t in targets:
        all_lines.extend(TOOLS[t]["fn"](source, target))

    # 通用配置
    all_lines.append("\n[Git 配置]")
    all_lines.extend(configure_gitignore(target))

    # Obsidian Vault 模板（仅当 --obsidian 标志启用时部署）
    if should_deploy_obsidian(args):
        all_lines.extend(_deploy_obsidian_resources(source, target))

    all_lines.append("\n[工作区]")
    all_lines.extend(configure_info_json(target))
    all_lines.append("\n[工作流配置]")
    all_lines.extend(configure_config_yaml(target))
    all_lines.extend(generate_workspace(target))

    for line in all_lines:
        print(line)

    print(f"\n部署完成。目标路径: {target}")
    for t in targets:
        print(TOOLS[t]["tip"])


if __name__ == "__main__":
    main()
