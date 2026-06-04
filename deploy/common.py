# deploy/common.py
# AI_Prompt 閮ㄧ讲鑴氭湰 鈥?閫氱敤閫昏緫

import os
import json
import shutil
from pathlib import Path

# 鈹€鈹€ 閫氱敤璧勬簮婧愭枃浠讹紙閮ㄧ讲鏃舵寜宸ュ叿鍓嶇紑澶嶅埗鍒扮洰鏍囩洰褰曪級鈹€鈹€鈹€鈹€鈹€鈹€鈹€

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

# 鍚戦噺鍖栫煡璇嗗簱鑴氭湰锛堥€氳繃 --with-vectors 鎸夐渶閮ㄧ讲锛?
VECTOR_SCRIPTS = [
    "scripts/build_kb_index.py",
    "scripts/search_kb.py",
]

VECTOR_DEPENDENCY_NOTICE = (
    "鍚戦噺鍖栨绱緷璧? pip install sentence-transformers\n"
    "  鏋勫缓绱㈠紩: python scripts/build_kb_index.py\n"
    "  璇箟鎼滅储: python scripts/search_kb.py \"鏌ヨ鏂囨湰\""
)

# 鈹€鈹€ 甯搁噺 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

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
# vectors/ 鐩綍绾冲叆 .gitignore 浣嗕繚鐣欑洰褰曠粨鏋勪互鍏佽绱㈠紩鏂囦欢瀛樺湪
# 鍚戦噺绱㈠紩鏄紦瀛樺眰锛屽彲闅忔椂浠?Markdown 鏂囦欢閲嶅缓
"""

CONFIG_YAML_CONTENT = """\
# .ai/config.yaml
# AI_Prompt 宸ヤ綔娴佺粺涓€閰嶇疆
# 鎻愪緵鎵€鏈夐樁娈电殑鍏ㄥ眬榛樿鍊?
# 鍚勯樁娈?status.md 鍙眬閮ㄨ鐩?

meta:
  version: 1.0.0

# ---- 宸ヤ綔娴侀粯璁ゅ€?----
# 鍒涘缓鏂伴樁娈垫垨 status.md 鏈～鍐欐椂搴旂敤浠ヤ笅榛樿鍊?
# 娉細姝や负閮ㄧ讲妯℃澘榛樿鍊硷紙manual+disabled锛夛紝浠撳簱鑷韩 config.yaml 鍙兘涓嶅悓
defaults:
  # 鎵ц妯″紡锛歮anual=浜哄伐椹卞姩锛宎uto=Agent 椹卞姩
  # 浠?auto+enabled 鐨勯樁娈靛弬涓庤嚜鍔ㄩ棴鐜?
  execution_mode: manual

  # 鑷姩鎺ㄨ繘锛歞isabled=姣忔鏆傚仠锛宔nabled=鑷姩涓嬩竴姝?
  # 闇€瑕?execution_mode=auto 鎵嶇敓鏁?
  auto_advance: disabled

  # 鍗曞厓娴嬭瘯閾捐矾锛歠alse=璺宠繃 test_writing鈫抰esting鈫抌ug_fixing
  # 涓?false 鏃?review_passed 鐩存帴杩囨浮鍒?done
  test_enabled: false

  # Worktree 鍚堝苟锛歮anual=鍦?Agent Manager 涓‘璁?
  # auto=AutoRunner 瀹屾垚鍚庤嚜鍔ㄦ墽琛?git merge + 娓呯悊
  merge_mode: auto
"""


# 鈹€鈹€ 宸ュ叿鍑芥暟 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

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
            lines.append(report("skipped", str(d), "宸插瓨鍦?))
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
            lines.append(report("warning", str(dst_rel), f"婧愭枃浠朵笉瀛樺湪: {src_rel}"))
            missing += 1
            continue
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        if dst_path.exists():
            lines.append(report("skipped", str(dst_rel), "宸插瓨鍦?))
            skipped += 1
        else:
            shutil.copy2(src_path, dst_path)
            lines.append(report("created", str(dst_rel)))
            copied += 1
    return lines, copied, skipped, missing


def deploy_resources(source: Path, target: Path, prefix: str, rules_dir: str = "instructions") -> tuple[list[str], int, int]:
    """灏嗛€氱敤 Instructions 鍜?Skills 閮ㄧ讲鍒扮洰鏍囩洰褰曘€?""
    lines = []
    inst_map = {s: f"{prefix}/{rules_dir}/{Path(s).name}" for s in INSTRUCTION_SOURCES}
    skill_map = {s: s.replace("skills/", f"{prefix}/skills/") for s in SKILL_SOURCES}
    total_copied, total_skipped = 0, 0

    lines.append(f"  [閫氱敤绾︽潫 鈫?{prefix}/{rules_dir}/]")
    i_lines, ic, iskip, im = copy_files(source, target, inst_map)
    lines.extend(i_lines)
    lines.append(report("info", f"瑙勫垯: 澶嶅埗 {ic}, 璺宠繃 {iskip}" + (f", 缂哄け {im}" if im else "")))
    total_copied += ic; total_skipped += iskip

    lines.append(f"  [閫氱敤鎶€鑳?鈫?{prefix}/skills/]")
    s_lines, sc, sskip, sm = copy_files(source, target, skill_map)
    lines.extend(s_lines)
    lines.append(report("info", f"鎶€鑳? 澶嶅埗 {sc}, 璺宠繃 {sskip}" + (f", 缂哄け {sm}" if sm else "")))
    total_copied += sc; total_skipped += sskip

    return lines, total_copied, total_skipped


# 鈹€鈹€ 閫氱敤閰嶇疆 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€

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
        lines.append(report("created", ".gitignore", f"杩藉姞 {len(missing)} 鏉?))
    else:
        lines.append(report("skipped", ".gitignore", "鏉＄洰瀹屾暣"))
    ai_path = target / ".ai" / ".gitignore"
    ai_path.parent.mkdir(parents=True, exist_ok=True)
    if ai_path.exists():
        lines.append(report("skipped", ".ai/.gitignore", "宸插瓨鍦?))
    else:
        ai_path.write_text(AI_GITIGNORE_CONTENT, encoding="utf-8")
        lines.append(report("created", ".ai/.gitignore"))
    return lines


def configure_info_json(target: Path) -> list[str]:
    path = target / ".ai" / ".info.json"
    if path.exists():
        return [report("skipped", ".ai/.info.json", "宸插瓨鍦?)]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INFO_JSON_CONTENT, encoding="utf-8")
    return [report("created", ".ai/.info.json")]


def configure_config_yaml(target: Path) -> list[str]:
    path = target / ".ai" / "config.yaml"
    if path.exists():
        return [report("skipped", ".ai/config.yaml", "宸插瓨鍦?)]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CONFIG_YAML_CONTENT, encoding="utf-8")
    return [report("created", ".ai/config.yaml")]


def generate_workspace(target: Path) -> list[str]:
    name = f"{target.resolve().name}.code-workspace"
    ws_path = target / name
    if ws_path.exists():
        return [report("skipped", name, "宸插瓨鍦?)]
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
