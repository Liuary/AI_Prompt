# deploy/common.py
# AI_Prompt 部署脚本 — 通用逻辑（Instructions/Skills/目录/配置）

import os
import json
import shutil
from pathlib import Path

# ── 通用资源（所有工具都部署）───────────────────────────────

# Instructions — 跨工具的 .ai/ 工作区操作规范
INSTRUCTIONS_FILES = {
    "instructions/core.md": "instructions/core.md",
}

SKILLS_FILES = {
    "skills/bug-acceptance/SKILL.md": "skills/bug-acceptance/SKILL.md",
    "skills/get-bugs/SKILL.md": "skills/get-bugs/SKILL.md",
    "skills/check-kb/SKILL.md": "skills/check-kb/SKILL.md",
    "skills/sync-status/SKILL.md": "skills/sync-status/SKILL.md",
    "skills/get-stage-status/SKILL.md": "skills/get-stage-status/SKILL.md",
    "skills/update-stage-status/SKILL.md": "skills/update-stage-status/SKILL.md",
}

INSTRUCTIONS_DIRS = [
    "instructions",
]

SKILLS_DIRS = [
    "skills",
]

# ── 常量 ────────────────────────────────────────────────────────

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

INFO_JSON_CONTENT = """\
{
    "user": ""
}
"""

ROOT_GITIGNORE_ENTRIES = [
    ".kilo/",
]

AI_GITIGNORE_CONTENT = """\
.info.json
users/
tmp/
"""


# ── 工具函数 ────────────────────────────────────────────────────

def report(status: str, path: str, detail: str = "") -> str:
    prefix = {"created": "[+]", "skipped": "[=]", "warning": "[!]", "error": "[X]", "info": " i "}.get(status, "   ")
    line = f"  {prefix} {path}"
    if detail:
        line += f"  ({detail})"
    return line


def create_directories(target: Path, tool_dirs: list[str]) -> list[str]:
    lines = []
    all_dirs = list(AI_DIRS) + list(INSTRUCTIONS_DIRS) + list(SKILLS_DIRS) + list(tool_dirs)
    for d in all_dirs:
        dir_path = target / d
        if dir_path.exists():
            lines.append(report("skipped", str(d), "已存在"))
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            lines.append(report("created", str(d)))
    return lines


def copy_files(source: Path, target: Path, file_map: dict) -> tuple:
    lines, copied, skipped, missing = [], 0, 0, 0
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


# ── 通用配置 ────────────────────────────────────────────────────

def configure_gitignore(target: Path) -> list[str]:
    lines = []
    root_path = target / ".gitignore"
    existing = set()
    if root_path.exists():
        existing = set(line.strip() for line in root_path.read_text(encoding="utf-8").splitlines() if line.strip())
    missing = [e for e in ROOT_GITIGNORE_ENTRIES if e not in existing]
    if missing:
        with root_path.open("a", encoding="utf-8") as f:
            if root_path.stat().st_size > 0:
                f.seek(0, os.SEEK_END)
                if f.tell() > 0: f.write("\n")
            f.writelines(e + "\n" for e in missing)
        lines.append(report("created", ".gitignore", f"追加 {len(missing)} 条"))
    else:
        lines.append(report("skipped", ".gitignore", "条目完整"))
    ai_path = target / ".ai" / ".gitignore"
    ai_path.parent.mkdir(parents=True, exist_ok=True)
    if ai_path.exists():
        lines.append(report("skipped", ".ai/.gitignore", "已存在"))
    else:
        ai_path.write_text(AI_GITIGNORE_CONTENT, encoding="utf-8")
        lines.append(report("created", ".ai/.gitignore"))
    return lines


def configure_info_json(target: Path) -> list[str]:
    path = target / ".ai" / ".info.json"
    if path.exists():
        return [report("skipped", ".ai/.info.json", "已存在")]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INFO_JSON_CONTENT, encoding="utf-8")
    return [report("created", ".ai/.info.json")]


def generate_workspace(target: Path) -> list[str]:
    name = f"{target.resolve().name}.code-workspace"
    ws_path = target / name
    if ws_path.exists():
        return [report("skipped", name, "已存在")]
    ws_path.write_text(json.dumps({"folders": [{"path": "."}], "settings": {}}, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    return [report("created", name)]
