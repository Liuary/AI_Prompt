# deploy/common.py
# AI_Prompt 部署脚本 — 通用逻辑

import os
import json
import shutil
from pathlib import Path

# ── 通用资源源文件（部署时按工具前缀复制到目标目录）───────

INSTRUCTION_SOURCES = [
    "instructions/core.md",
]

SKILL_SOURCES = [
    "skills/bug-acceptance/SKILL.md",
    "skills/get-bugs/SKILL.md",
    "skills/check-kb/SKILL.md",
    "skills/search-kb/SKILL.md",
    "skills/sync-status/SKILL.md",
    "skills/get-stage-status/SKILL.md",
    "skills/update-stage-status/SKILL.md",
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

CONFIG_YAML_CONTENT = """\
# .ai/config.yaml
# AI_Prompt 工作流统一配置
# 提供所有阶段的全局默认值
# 各阶段 status.md 可局部覆盖

meta:
  version: 1.0.0

# ---- 工作流默认值 ----
# 创建新阶段或 status.md 未填写时应用以下默认值
# 注：此为部署模板默认值（manual+disabled），仓库自身 config.yaml 可能不同
defaults:
  # 执行模式：manual=人工驱动，auto=Agent 驱动
  # 仅 auto+enabled 的阶段参与自动闭环
  execution_mode: manual

  # 自动推进：disabled=每步暂停，enabled=自动下一步
  # 需要 execution_mode=auto 才生效
  auto_advance: disabled

  # 单元测试链路：false=跳过 test_writing→testing→bug_fixing
  # 为 false 时 review_passed 直接过渡到 done
  test_enabled: false

  # Worktree 合并：manual=在 Agent Manager 中确认
  # auto=AutoRunner 完成后自动执行 git merge + 清理
  merge_mode: auto
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
    all_dirs = list(AI_DIRS) + list(tool_dirs)
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


def deploy_resources(source: Path, target: Path, prefix: str, rules_dir: str = "instructions") -> tuple[list[str], int, int]:
    """将通用 Instructions 和 Skills 部署到目标目录。"""
    lines = []
    inst_map = {s: f"{prefix}/{rules_dir}/{Path(s).name}" for s in INSTRUCTION_SOURCES}
    skill_map = {s: s.replace("skills/", f"{prefix}/skills/") for s in SKILL_SOURCES}
    total_copied, total_skipped = 0, 0

    lines.append(f"  [通用约束 → {prefix}/{rules_dir}/]")
    i_lines, ic, iskip, im = copy_files(source, target, inst_map)
    lines.extend(i_lines)
    lines.append(report("info", f"规则: 复制 {ic}, 跳过 {iskip}" + (f", 缺失 {im}" if im else "")))
    total_copied += ic; total_skipped += iskip

    lines.append(f"  [通用技能 → {prefix}/skills/]")
    s_lines, sc, sskip, sm = copy_files(source, target, skill_map)
    lines.extend(s_lines)
    lines.append(report("info", f"技能: 复制 {sc}, 跳过 {sskip}" + (f", 缺失 {sm}" if sm else "")))
    total_copied += sc; total_skipped += sskip

    return lines, total_copied, total_skipped


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


def configure_config_yaml(target: Path) -> list[str]:
    path = target / ".ai" / "config.yaml"
    if path.exists():
        return [report("skipped", ".ai/config.yaml", "已存在")]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CONFIG_YAML_CONTENT, encoding="utf-8")
    return [report("created", ".ai/config.yaml")]


def generate_workspace(target: Path) -> list[str]:
    name = f"{target.resolve().name}.code-workspace"
    ws_path = target / name
    if ws_path.exists():
        return [report("skipped", name, "已存在")]
    workspace = {
        "folders": [{"path": "."}],
        "settings": {
            "chat.includeApplyingInstructions": True,
            "chat.useAgentsMdFile": True,
            "chat.useCustomAgentHooks": True,
        },
    }
    ws_path.write_text(json.dumps(workspace, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    return [report("created", name)]
