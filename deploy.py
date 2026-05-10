#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
AI_Prompt 模板项目一键部署脚本。

用法:
    python deploy.py <目标路径>
    python deploy.py <目标路径> --source <模板源路径>

示例:
    python deploy.py /home/user/my-project
    python deploy.py D:\\Projects\\my-app --source ./AI_Prompt
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

# ─── 模板文件清单（源文件相对路径 → 目标文件相对路径）───────────────────
TEMPLATE_FILES = {
    "AGENTS.md": "AGENTS.md",
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

# ─── 需要创建的目录 ───────────────────────────────────────────────────
DIRS = [
    ".kilo/Instructions",
    ".kilo/agents",
    ".kilo/skills/bug-acceptance",
    ".kilo/skills/get-bugs",
    ".kilo/skills/check-kb",
    ".kilo/skills/get-stage-status",
    ".kilo/skills/update-stage-status",
    ".ai/dev/note",
    ".ai/log",
    ".ai/code_review",
    ".ai/bugs",
    ".ai/plan",
    ".ai/kb",
    ".ai/tmp",
    ".ai/users",
]

# ─── .gitignore 必需条目 ──────────────────────────────────────────────
GITIGNORE_ENTRIES = [
    ".ai/.info.json",
    ".ai/users/",
    ".kilo/",
]

# ─── kilo.jsonc 模板内容 ──────────────────────────────────────────────
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

# ─── .ai/.info.json 模板内容 ──────────────────────────────────────────
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


def create_directories(target: Path) -> list[str]:
    """创建目标项目目录结构，返回报告行列表。"""
    lines = []
    for d in DIRS:
        dir_path = target / d
        if dir_path.exists():
            lines.append(report("skipped", str(d), "已存在"))
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            lines.append(report("created", str(d)))
    return lines


def copy_template_files(source: Path, target: Path) -> list[str]:
    """复制模板文件到目标项目，返回报告行列表。"""
    lines = []
    total_copied = 0
    total_skipped = 0
    total_missing = 0

    for src_rel, dst_rel in TEMPLATE_FILES.items():
        src_path = source / src_rel
        dst_path = target / dst_rel

        if not src_path.exists():
            lines.append(report("warning", str(dst_rel), f"源文件不存在: {src_rel}"))
            total_missing += 1
            continue

        # 确保目标父目录存在
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        if dst_path.exists():
            lines.append(report("skipped", str(dst_rel), "已存在"))
            total_skipped += 1
        else:
            shutil.copy2(src_path, dst_path)
            lines.append(report("created", str(dst_rel)))
            total_copied += 1

    if total_copied or total_skipped or total_missing:
        lines.append(
            f"\n  复制 {total_copied}，跳过 {total_skipped}，缺失 {total_missing}"
        )
    return lines


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
    lines = []

    # 读取已有内容
    existing = set()
    if path.exists():
        existing = set(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())

    # 找出缺失条目
    missing = [e for e in GITIGNORE_ENTRIES if e not in existing]
    if not missing:
        return [report("skipped", ".gitignore", "条目完整")]

    # 追加
    with path.open("a", encoding="utf-8") as f:
        # 如果文件非空且不以换行结尾，先加一个换行
        if path.stat().st_size > 0:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.write("\n")
        f.writelines(e + "\n" for e in missing)

    lines.append(report("created", ".gitignore", f"追加 {len(missing)} 条"))
    return lines


def configure_info_json(target: Path) -> list[str]:
    """生成 .ai/.info.json（如不存在），返回报告行列表。"""
    path = target / ".ai" / ".info.json"
    if path.exists():
        return [report("skipped", ".ai/.info.json", "已存在")]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INFO_JSON_CONTENT, encoding="utf-8")
    return [report("created", ".ai/.info.json")]


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
        description="AI_Prompt 模板项目一键部署脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=r"""
示例:
  python deploy.py /home/user/my-project
  python deploy.py D:\\Projects\\my-app --source ./AI_Prompt
        """.strip(),
    )
    parser.add_argument(
        "target",
        help="目标项目路径（不存在则自动创建）",
    )
    parser.add_argument(
        "--source",
        help="模板源路径（默认为脚本所在目录）",
        default=None,
    )
    args = parser.parse_args()

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
        pass  # 不在源目录下，安全

    # 创建目标目录
    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)
    elif not target.is_dir():
        print(f"错误: 目标路径存在但不是目录: {target}")
        sys.exit(1)

    print(f"\n部署中...")
    print(f"  源: {source}")
    print(f"  目标: {target}\n")

    all_lines = []
    all_lines.append("[目录结构]")
    all_lines.extend(create_directories(target))
    all_lines.append("\n[模板文件]")
    all_lines.extend(copy_template_files(source, target))
    all_lines.append("\n[配置文件]")
    all_lines.extend(configure_kilo_jsonc(target))
    all_lines.extend(configure_gitignore(target))
    all_lines.extend(configure_info_json(target))
    all_lines.append("\n[工作区]")
    all_lines.extend(generate_workspace(target))

    # 输出报告
    for line in all_lines:
        print(line)

    print(f"\n部署完成。目标路径: {target}")
    print("重启 Kilo 会话后 Subagent 和 Skill 生效。")


if __name__ == "__main__":
    main()
