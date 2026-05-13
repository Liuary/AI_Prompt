#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AI_Prompt 模板项目一键部署脚本（多工具支持）。

用法:
    python deploy.py <目标路径>
    python deploy.py <目标路径> --tool kilo
    python deploy.py <目标路径> --tool deepcode
    python deploy.py <目标路径> --tool all
    python deploy.py <目标路径> --source <模板源路径>

示例:
    python deploy.py /home/user/my-project                        # 默认 Kilo
    python deploy.py /home/user/my-project --tool deepcode        # Deep Code CLI
    python deploy.py /home/user/my-project --tool all             # 全部工具
    python deploy.py D:\\Projects\\my-app --source ./AI_Prompt
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════
# 通用文件（所有工具都部署）
# ═══════════════════════════════════════════════════════════════════════

COMMON_FILES = {
    # AGENTS.md 由各适配器分别提供（Kilo 用根版本，deepcode 用合并版本）
}

# ═══════════════════════════════════════════════════════════════════════
# Kilo 专用文件
# ═══════════════════════════════════════════════════════════════════════

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
    "Kilo/skills/get-stage-status/SKILL.md": ".kilo/skills/get-stage-status/SKILL.md",
    "Kilo/skills/update-stage-status/SKILL.md": ".kilo/skills/update-stage-status/SKILL.md",
}

KILO_DIRS = [
    ".kilo/Instructions",
    ".kilo/agents",
    ".kilo/skills/bug-acceptance",
    ".kilo/skills/get-bugs",
    ".kilo/skills/check-kb",
    ".kilo/skills/get-stage-status",
    ".kilo/skills/update-stage-status",
]

# ═══════════════════════════════════════════════════════════════════════
# Deep Code CLI 专用文件
# ═══════════════════════════════════════════════════════════════════════

DEEPCODE_FILES = {
    "adapters/deepcode/skills/check-kb/SKILL.md": ".agents/skills/check-kb/SKILL.md",
    "adapters/deepcode/skills/get-bugs/SKILL.md": ".agents/skills/get-bugs/SKILL.md",
    "adapters/deepcode/skills/bug-acceptance/SKILL.md": ".agents/skills/bug-acceptance/SKILL.md",
    "adapters/deepcode/skills/get-stage-status/SKILL.md": ".agents/skills/get-stage-status/SKILL.md",
    "adapters/deepcode/skills/update-stage-status/SKILL.md": ".agents/skills/update-stage-status/SKILL.md",
}

DEEPCODE_DIRS = [
    ".agents/skills/check-kb",
    ".agents/skills/get-bugs",
    ".agents/skills/bug-acceptance",
    ".agents/skills/get-stage-status",
    ".agents/skills/update-stage-status",
    ".deepcode",
]

# ═══════════════════════════════════════════════════════════════════════
# Claude Code 专用文件
# ═══════════════════════════════════════════════════════════════════════

CLAUDE_FILES = {
    "adapters/claude-code/CLAUDE.md": "CLAUDE.md",
    ".claude/commands/rule-compile.md": ".claude/commands/rule-compile.md",
    ".claude/commands/rule-validate.md": ".claude/commands/rule-validate.md",
}

CLAUDE_DIRS = [
    ".claude/commands",
]

# ═══════════════════════════════════════════════════════════════════════
# GitHub Copilot 专用文件
# ═══════════════════════════════════════════════════════════════════════

COPILOT_FILES = {
    "adapters/copilot/copilot-instructions.md": ".github/copilot-instructions.md",
}

COPILOT_DIRS = [
    ".github",
]

# ═══════════════════════════════════════════════════════════════════════
# 通用目录
# ═══════════════════════════════════════════════════════════════════════

AI_DIRS = [
    ".ai/dev/note",
    ".ai/log",
    ".ai/code_review",
    ".ai/bugs",
    ".ai/plan",
    ".ai/kb",
    ".ai/tmp",
    ".ai/users",
]

# ═══════════════════════════════════════════════════════════════════════
# .gitignore 必需条目
# ═══════════════════════════════════════════════════════════════════════

GITIGNORE_ENTRIES = [
    ".ai/.info.json",
    ".ai/users/",
    ".kilo/",
]

# ═══════════════════════════════════════════════════════════════════════
# kilo.jsonc 模板内容
# ═══════════════════════════════════════════════════════════════════════

KILO_JSONC_CONTENT = """\
{
  "$schema": "https://app.kilo.ai/config.json",
  "instructions": [
    ".kilo/Instructions/kilo_instructions_core.md"
  ],
  "experimental": {
    "agent_manager_tool": true
  }
}
"""

# ═══════════════════════════════════════════════════════════════════════
# .ai/.info.json 模板内容
# ═══════════════════════════════════════════════════════════════════════

INFO_JSON_CONTENT = """\
{
    "user": ""
}
"""

# ═══════════════════════════════════════════════════════════════════════
# 核心逻辑
# ═══════════════════════════════════════════════════════════════════════


def report(status: str, path: str, detail: str = "") -> str:
    """格式化报告行。"""
    prefix = {"created": "[+]", "skipped": "[=]", "warning": "[!]", "error": "[X]"}.get(status, "   ")
    line = f"  {prefix} {path}"
    if detail:
        line += f"  ({detail})"
    return line


def create_directories(target: Path, tool: str) -> list[str]:
    """创建目标项目目录结构，返回报告行列表。"""
    lines = []
    dirs_to_create = list(AI_DIRS)

    if tool in ("kilo", "all"):
        dirs_to_create.extend(KILO_DIRS)
    if tool in ("deepcode", "all"):
        dirs_to_create.extend(DEEPCODE_DIRS)
    if tool in ("claude", "all"):
        dirs_to_create.extend(CLAUDE_DIRS)
    if tool in ("copilot", "all"):
        dirs_to_create.extend(COPILOT_DIRS)

    for d in dirs_to_create:
        dir_path = target / d
        if dir_path.exists():
            lines.append(report("skipped", str(d), "已存在"))
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            lines.append(report("created", str(d)))
    return lines


def copy_files(source: Path, target: Path, file_map: dict) -> tuple[list[str], int, int, int]:
    """复制文件映射到目标项目，返回 (报告行列表, 已复制, 已跳过, 缺失)。"""
    lines = []
    copied = 0
    skipped = 0
    missing = 0

    for src_rel, dst_rel in file_map.items():
        src_path = source / src_rel
        dst_path = target / dst_rel

        if not src_path.exists():
            lines.append(report("warning", str(dst_rel), f"源文件不存在: {src_rel}"))
            missing += 1
            continue

        dst_path.parent.mkdir(parents=True, exist_ok=True)

        if dst_path.exists():
            lines.append(report("skipped", str(dst_rel), "已存在"))
            skipped += 1
        else:
            shutil.copy2(src_path, dst_path)
            lines.append(report("created", str(dst_rel)))
            copied += 1

    return lines, copied, skipped, missing


def configure_kilo_jsonc(target: Path) -> list[str]:
    """生成 kilo.jsonc（如不存在），返回报告行列表。"""
    path = target / "kilo.jsonc"
    if path.exists():
        return [report("skipped", "kilo.jsonc", "已存在")]
    path.write_text(KILO_JSONC_CONTENT, encoding="utf-8")
    return [report("created", "kilo.jsonc")]


def configure_gitignore(target: Path) -> list[str]:
    """配置 .gitignore，追加缺失条目，返回报告行列表。"""
    path = target / ".gitignore"
    lines_result = []

    existing = set()
    if path.exists():
        existing = set(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

    missing = [e for e in GITIGNORE_ENTRIES if e not in existing]
    if not missing:
        return [report("skipped", ".gitignore", "条目完整")]

    with path.open("a", encoding="utf-8") as f:
        if path.stat().st_size > 0:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.write("\n")
        f.writelines(e + "\n" for e in missing)

    lines_result.append(report("created", ".gitignore", f"追加 {len(missing)} 条"))
    return lines_result


def configure_info_json(target: Path) -> list[str]:
    """生成 .ai/.info.json（如不存在），返回报告行列表。"""
    path = target / ".ai" / ".info.json"
    if path.exists():
        return [report("skipped", ".ai/.info.json", "已存在")]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INFO_JSON_CONTENT, encoding="utf-8")
    return [report("created", ".ai/.info.json")]


def configure_agents_md(source: Path, target: Path, tool: str) -> list[str]:
    """部署 AGENTS.md 到项目根目录，按工具选择版本，返回报告行列表。"""
    lines = []
    dst_path = target / "AGENTS.md"

    # 选择源文件：all 和 deepcode 用合并版（含 Instructions 规范），kilo 用标准版
    if tool in ("deepcode", "all"):
        src_rel = "adapters/deepcode/AGENTS.md"
    else:
        src_rel = "AGENTS.md"

    src_path = source / src_rel
    if not src_path.exists():
        lines.append(report("warning", "AGENTS.md", f"源文件不存在: {src_rel}"))
        return lines

    if dst_path.exists():
        lines.append(report("skipped", "AGENTS.md", "已存在"))
    else:
        shutil.copy2(src_path, dst_path)
        lines.append(report("created", "AGENTS.md"))
    return lines


def configure_deepcode_agents_md(source: Path, target: Path) -> list[str]:
    """部署 AGENTS.md 到 deepcode 目录（.deepcode/AGENTS.md），如不存在则创建。"""
    lines = []
    src_path = source / "adapters" / "deepcode" / "AGENTS.md"
    dst_path = target / ".deepcode" / "AGENTS.md"

    if not src_path.exists():
        lines.append(report("warning", ".deepcode/AGENTS.md", "源文件 AGENTS.md 不存在"))
        return lines

    dst_path.parent.mkdir(parents=True, exist_ok=True)

    if dst_path.exists():
        lines.append(report("skipped", ".deepcode/AGENTS.md", "已存在"))
    else:
        shutil.copy2(src_path, dst_path)
        lines.append(report("created", ".deepcode/AGENTS.md"))
    return lines


def generate_workspace(target: Path) -> list[str]:
    """生成 .code-workspace 文件，返回报告行列表。"""
    project_name = target.resolve().name
    workspace_name = f"{project_name}.code-workspace"
    workspace_path = target / workspace_name

    if workspace_path.exists():
        return [report("skipped", workspace_name, "已存在")]

    workspace = {
        "folders": [
            {
                "path": "."
            }
        ],
        "settings": {}
    }

    workspace_path.write_text(
        json.dumps(workspace, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    return [report("created", workspace_name)]


def show_help():
    """输出自定义帮助信息（覆盖 argparse 默认 --help）。"""
    print(r"""AI_Prompt — 跨 AI 工具开发治理模板部署脚本
============================================

用法:
  python deploy.py <目标路径> [选项]

选项:
  -k, --kilo          仅部署 Kilo 框架（Agent/Skill/Instructions → .kilo/）
  -d, --deepcode      仅部署 Deep Code CLI 框架（合并版 AGENTS.md + Skill → .agents/）
  -c, --claude        仅部署 Claude Code 适配器（CLAUDE.md + .claude/commands/）
  -p, --copilot       仅部署 GitHub Copilot 适配器（.github/copilot-instructions.md）
  -l, --list          列出所有支持的 AI 工具
  -h, --help          显示本帮助信息
  --source <路径>     指定模板源路径（默认为脚本所在目录）

不指定工具选项时默认部署全部框架。

示例:
  python deploy.py /home/user/my-project               # 部署全部
  python deploy.py /home/user/my-project -k            # 仅 Kilo
  python deploy.py /home/user/my-project -d            # 仅 Deep Code CLI
  python deploy.py /home/user/my-project -c            # 仅 Claude Code
  python deploy.py /home/user/my-project -p            # 仅 Copilot
  python deploy.py --list                              # 列出工具
  python deploy.py --help                              # 本帮助

项目: https://github.com/Liuary/AI_Prompt""")
    sys.exit(0)


def show_list():
    """输出支持的工具列表。"""
    print("支持的 AI 工具：\n")
    print("  kilo        Kilo — 终端 Agent 工具，支持完整 Agent 角色体系与自动闭环")
    print("  deepcode    Deep Code CLI — 终端 AI 编码助手，通过 Skill + AGENTS.md 提供核心治理能力")
    print("  claude      Claude Code — Anthropic 的终端 Agent 工具，通过 CLAUDE.md + 命令提供治理能力")
    print("  copilot     GitHub Copilot — IDE 内嵌 AI 助手，通过 copilot-instructions.md 提供行为约束")
    print("\n用法：python deploy.py <目标路径> [-k | -d | -c | -p]")
    print("不指定选项时默认部署全部。")
    sys.exit(0)


# ═══════════════════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════════════════


def main():
    # 尽早设置 stdout 编码，避免 Windows GBK 乱码
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="AI_Prompt 模板项目一键部署脚本（多工具支持）",
        add_help=False,  # 禁用默认 --help，使用自定义帮助
    )
    parser.add_argument(
        "target",
        nargs="?",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--source",
        help=argparse.SUPPRESS,
        default=None,
    )
    tool_group = parser.add_mutually_exclusive_group()
    tool_group.add_argument(
        "-k", "--kilo",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    tool_group.add_argument(
        "-d", "--deepcode",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    tool_group.add_argument(
        "-c", "--claude",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    tool_group.add_argument(
        "-p", "--copilot",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    # ── --help：自定义帮助 ──
    if args.help:
        show_help()

    # ── --list：列出工具 ──
    if args.list:
        show_list()

    # ── 确定部署哪些工具 ──
    if args.kilo:
        tool = "kilo"
    elif args.deepcode:
        tool = "deepcode"
    elif args.claude:
        tool = "claude"
    elif args.copilot:
        tool = "copilot"
    else:
        tool = "all"

    # target 为必填
    if not args.target:
        print("错误: 需要指定目标项目路径\n")
        print("用法：python deploy.py <目标路径> [-k | -d | -c | -p]")
        print("      python deploy.py --help 查看完整帮助")
        sys.exit(1)

    # 确定源路径
    if args.source:
        source = Path(args.source).resolve()
    else:
        source = Path(__file__).resolve().parent

    if not source.exists():
        print(f"错误: 模板源路径不存在: {source}")
        sys.exit(1)

    # 确定目标路径
    target = Path(args.target).resolve()

    # 安全检查：禁止部署到源目录自身或其子目录
    try:
        target.relative_to(source)
        print("错误: 不允许部署到模板源目录自身或其子目录")
        sys.exit(1)
    except ValueError:
        pass

    # 创建目标目录
    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)
    elif not target.is_dir():
        print(f"错误: 目标路径存在但不是目录: {target}")
        sys.exit(1)

    tool_label = {"kilo": "Kilo", "deepcode": "Deep Code CLI", "claude": "Claude Code", "copilot": "GitHub Copilot", "all": "全部工具"}[tool]

    print(f"\n部署中...")
    print(f"  源:     {source}")
    print(f"  目标:   {target}")
    print(f"  工具:   {tool_label}\n")

    all_lines = []

    # ── 通用文件 ──
    all_lines.append("[通用文件]")
    common_lines, cc, cs, cm = copy_files(source, target, COMMON_FILES)
    all_lines.extend(common_lines)

    # ── AGENTS.md（按工具选择版本）──
    all_lines.append("\n[AGENTS.md]")
    all_lines.extend(configure_agents_md(source, target, tool))

    # ── 目录结构 ──
    all_lines.append("\n[目录结构]")
    all_lines.extend(create_directories(target, tool))

    # ── Kilo 专用 ──
    if tool in ("kilo", "all"):
        all_lines.append("\n[Kilo 适配器]")
        kilo_lines, kc, ks, km = copy_files(source, target, KILO_FILES)
        all_lines.extend(kilo_lines)
        all_lines.append(report("info", f"Kilo 文件: 复制 {kc}, 跳过 {ks}" + (f", 缺失 {km}" if km else "")))

        all_lines.append("\n[Kilo 配置]")
        all_lines.extend(configure_kilo_jsonc(target))

    # ── Deep Code CLI 专用 ──
    if tool in ("deepcode", "all"):
        all_lines.append("\n[Deep Code CLI 适配器]")
        dc_lines, dc_copied, dc_skipped, dc_missing = copy_files(source, target, DEEPCODE_FILES)
        all_lines.extend(dc_lines)
        all_lines.append(report("info", f"DeepCode 文件: 复制 {dc_copied}, 跳过 {dc_skipped}" + (f", 缺失 {dc_missing}" if dc_missing else "")))

        # 部署 AGENTS.md 的 deepcode 专用副本
        all_lines.append("\n[DeepCode .deepcode/]")
        all_lines.extend(configure_deepcode_agents_md(source, target))

    # ── Claude Code 专用 ──
    if tool in ("claude", "all"):
        all_lines.append("\n[Claude Code 适配器]")
        cc_lines, cc_copied, cc_skipped, cc_missing = copy_files(source, target, CLAUDE_FILES)
        all_lines.extend(cc_lines)
        all_lines.append(report("info", f"Claude Code 文件: 复制 {cc_copied}, 跳过 {cc_skipped}" + (f", 缺失 {cc_missing}" if cc_missing else "")))

    # ── Copilot 专用 ──
    if tool in ("copilot", "all"):
        all_lines.append("\n[GitHub Copilot 适配器]")
        cp_lines, cp_copied, cp_skipped, cp_missing = copy_files(source, target, COPILOT_FILES)
        all_lines.extend(cp_lines)
        all_lines.append(report("info", f"Copilot 文件: 复制 {cp_copied}, 跳过 {cp_skipped}" + (f", 缺失 {cp_missing}" if cp_missing else "")))

    # ── 通用配置 ──
    all_lines.append("\n[Git 配置]")
    all_lines.extend(configure_gitignore(target))

    all_lines.append("\n[工作区]")
    all_lines.extend(configure_info_json(target))
    all_lines.extend(generate_workspace(target))

    # 输出报告
    for line in all_lines:
        print(line)

    print(f"\n部署完成。目标路径: {target}")
    if tool in ("kilo", "all"):
        print("重启 Kilo 会话后 Subagent 和 Skill 生效。")
    if tool in ("deepcode", "all"):
        print("启动 Deep Code CLI 后使用 /skills 查看可用 Skill。")
    if tool in ("claude", "all"):
        print("Claude Code 会话将自动读取 CLAUDE.md，使用 /rule-compile /rule-validate 命令。")
    if tool in ("copilot", "all"):
        print("GitHub Copilot 将自动读取 .github/copilot-instructions.md 作为行为约束。")


if __name__ == "__main__":
    main()
