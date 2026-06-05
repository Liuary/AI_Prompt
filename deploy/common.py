# deploy/common.py
# AI_Prompt 闁劎璁查懘姘拱 閳?闁氨鏁ら柅鏄忕帆

import os
import json
import shutil
from pathlib import Path

# 閳光偓閳光偓 闁氨鏁ょ挧鍕爱濠ф劖鏋冩禒璁圭礄闁劎璁查弮鑸靛瘻瀹搞儱鍙块崜宥囩磻婢跺秴鍩楅崚鎵窗閺嶅洨娲拌ぐ鏇礆閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

OBSIDIAN_RESOURCES = [
    ".ai/obsidian/README.md",
    ".ai/obsidian/dashboard.md",
    ".ai/obsidian/.obsidian/obsidian.json",
]

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

# 閸氭垿鍣洪崠鏍叀鐠囧棗绨遍懘姘拱閿涘牓鈧俺绻?--with-vectors 閹稿娓堕柈銊ц閿?
VECTOR_SCRIPTS = [
    "scripts/build_kb_index.py",
    "scripts/search_kb.py",
]

VECTOR_DEPENDENCY_NOTICE = (
    "閸氭垿鍣洪崠鏍梾缁鳖澀绶风挧? pip install sentence-transformers\n"
    "  閺嬪嫬缂撶槐銏犵穿: python scripts/build_kb_index.py\n"
    "  鐠囶厺绠熼幖婊呭偍: python scripts/search_kb.py \"閺屻儴顕楅弬鍥ㄦ拱\""
)

# 閳光偓閳光偓 鐢悂鍣?閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

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
# vectors/ 閻╊喖缍嶇痪鍐插弳 .gitignore 娴ｅ棔绻氶悾娆戞窗瑜版洜绮ㄩ弸鍕簰閸忎浇顔忕槐銏犵穿閺傚洣娆㈢€涙ê婀?
# 閸氭垿鍣虹槐銏犵穿閺勵垳绱︾€涙ê鐪伴敍灞藉讲闂呭繑妞傛禒?Markdown 閺傚洣娆㈤柌宥呯紦
"""

CONFIG_YAML_CONTENT = """\
# .ai/config.yaml
# AI_Prompt 瀹搞儰缍斿ù浣虹埠娑撯偓闁板秶鐤?
# 閹绘劒绶甸幍鈧張澶愭▉濞堢數娈戦崗銊ョ湰姒涙顓婚崐?
# 閸氬嫰妯佸▓?status.md 閸欘垰鐪柈銊洬閻?

meta:
  version: 1.0.0

# ---- 瀹搞儰缍斿ù渚€绮拋銈呪偓?----
# 閸掓稑缂撻弬浼存▉濞堝灚鍨?status.md 閺堫亜锝為崘娆愭鎼存梻鏁ゆ禒銉ょ瑓姒涙顓婚崐?
# 濞夘煉绱板銈勮礋闁劎璁插Ο鈩冩緲姒涙顓婚崐纭风礄manual+disabled閿涘绱濇禒鎾崇氨閼奉亣闊?config.yaml 閸欘垵鍏樻稉宥呮倱
defaults:
  # 閹笛嗩攽濡€崇础閿涙anual=娴滃搫浼愭す鍗炲З閿涘畮uto=Agent 妞瑰崬濮?
  # 娴?auto+enabled 閻ㄥ嫰妯佸▓闈涘棘娑撳氦鍤滈崝銊╂４閻?
  execution_mode: manual

  # 閼奉亜濮╅幒銊ㄧ箻閿涙瓰isabled=濮ｅ繑顒為弳鍌氫粻閿涘當nabled=閼奉亜濮╂稉瀣╃濮?
  # 闂団偓鐟?execution_mode=auto 閹靛秶鏁撻弫?
  auto_advance: disabled

  # 閸楁洖鍘撳ù瀣槸闁炬崘鐭鹃敍姝燼lse=鐠哄疇绻?test_writing閳姲esting閳妼ug_fixing
  # 娑?false 閺?review_passed 閻╁瓨甯存潻鍥ㄦ诞閸?done
  test_enabled: false

  # Worktree 閸氬牆鑻熼敍姝產nual=閸?Agent Manager 娑擃厾鈥樼拋?
  # auto=AutoRunner 鐎瑰本鍨氶崥搴ゅ殰閸斻劍澧界悰?git merge + 濞撳懐鎮?
  merge_mode: auto
"""

# 閹稿膩閸ㄥ鎮楃粩顖滄畱 models 闁板秶鐤嗛懞鍌浤侀弶?
MODELS_CONFIG_TEMPLATES = {
    "openai": """\
# ---- 濡€崇€烽崥搴ｎ伂闁板秶鐤?----
# 鐏?Agent 閼宠棄濮忛幓蹇氬牚娑撳骸鍙挎担鎾茨侀崹瀣倵缁旑垵袙閼?
# 娴兼ê鍘涚痪褝绱癆gent 缁狙嗩洬閻?> role 缁狙嗩洬閻?> default
models:
  # 姒涙顓诲Ο鈥崇€烽崥搴ｎ伂
  default:
    provider: openai
    model_name: gpt-4o
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY

  # 閹稿顫楅懝鍙夊瘹鐎规碍膩閸ㄥ绱欑粈杞扮伐閿?
  roles: {}
  # 閹?Agent 鐎圭偘绶ラ幐鍥х暰閿涘牏銇氭笟瀣剁礆
  agents: {}
""",
    "anthropic": """\
# ---- 濡€崇€烽崥搴ｎ伂闁板秶鐤?----
models:
  default:
    provider: anthropic
    model_name: claude-sonnet-4-20250514
    base_url: https://api.anthropic.com
    api_key_env: ANTHROPIC_API_KEY

  roles: {}
  agents: {}
""",
    "ollama": """\
# ---- 濡€崇€烽崥搴ｎ伂闁板秶鐤?----
models:
  default:
    provider: ollama
    model_name: hermes-3:8b
    base_url: http://localhost:11434/v1
    api_key_env: ""

  roles: {}
  agents: {}
""",
}


# 閳光偓閳光偓 瀹搞儱鍙块崙鑺ユ殶 閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓閳光偓

def report(status: str, path: str, detail: str = "") -> str:
    prefix = {"created": "[+]", "skipped": "[=]", "warning": "[!]", "error": "[X]", "info": " i "}.get(status, "   ")
    line = f"  {prefix} {path}"
    if detail:
        line += f"  ({detail})"
    return line


def create_directories(target: Path, tool_dirs: list[str]) -> list[str]:
    """Create AI and tool-specific directories."""
    lines = []
    all_dirs = list(AI_DIRS) + list(tool_dirs)
    for d in all_dirs:
        dir_path = target / d
        if dir_path.exists():
            lines.append(report("skipped", str(d)))
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            lines.append(report("created", str(d)))
    return lines


def copy_files(source: Path, target: Path, file_map: dict) -> tuple:
    """Copy files from source to target based on file_map."""
    lines, copied, skipped, missing = [], 0, 0, 0
    for src_rel, dst_rel in file_map.items():
        src_path = source / src_rel
        dst_path = target / dst_rel
        if not src_path.exists():
            lines.append(report("warning", str(dst_rel), "source missing"))
            missing += 1
            continue
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        if dst_path.exists():
            lines.append(report("skipped", str(dst_rel)))
            skipped += 1
        else:
            shutil.copy2(src_path, dst_path)
            lines.append(report("created", str(dst_rel)))
            copied += 1
    return lines, copied, skipped, missing


def deploy_resources(source: Path, target: Path, prefix: str, rules_dir: str = "instructions") -> tuple[list[str], int, int]:
    """Deploy Instructions and Skills to target directory."""
    lines = []
    inst_map = {s: f"{prefix}/{rules_dir}/{Path(s).name}" for s in INSTRUCTION_SOURCES}
    skill_map = {s: s.replace("skills/", f"{prefix}/skills/") for s in SKILL_SOURCES}
    total_copied, total_skipped = 0, 0
    lines.append(f"  [Instructions => {prefix}/{rules_dir}/]")
    i_lines, ic, iskip, im = copy_files(source, target, inst_map)
    lines.extend(i_lines)
    lines.append(report("info", f"Instructions: copied {ic}, skipped {iskip}"))
    total_copied += ic; total_skipped += iskip
    lines.append(f"  [Skills => {prefix}/skills/]")
    s_lines, sc, sskip, sm = copy_files(source, target, skill_map)
    lines.extend(s_lines)
    lines.append(report("info", f"Skills: copied {sc}, skipped {sskip}"))
    total_copied += sc; total_skipped += sskip
    return lines, total_copied, total_skipped

def configure_gitignore(target: Path) -> list[str]:
    """Configure root .gitignore with required entries."""
    lines = []
    root_path = target / ".gitignore"
    existing = set()
    if root_path.exists():
        existing = set(line.strip() for line in root_path.read_text(encoding="utf-8").splitlines() if line.strip())
    missing_entries = [e for e in ROOT_GITIGNORE_ENTRIES if e not in existing]
    if missing_entries:
        with root_path.open("a", encoding="utf-8") as f:
            if root_path.stat().st_size > 0:
                f.seek(0, os.SEEK_END)
                if f.tell() > 0: f.write("\n")
            f.writelines(e + "\n" for e in missing_entries)
        lines.append(report("created", ".gitignore", f"added {len(missing_entries)} entries"))
    else:
        lines.append(report("skipped", ".gitignore"))
    ai_path = target / ".ai" / ".gitignore"
    ai_path.parent.mkdir(parents=True, exist_ok=True)
    if ai_path.exists():
        lines.append(report("skipped", ".ai/.gitignore"))
    else:
        ai_path.write_text(AI_GITIGNORE_CONTENT, encoding="utf-8")
        lines.append(report("created", ".ai/.gitignore"))
    return lines


def configure_info_json(target: Path) -> list[str]:
    """Configure .ai/.info.json with user identity."""
    path = target / ".ai" / ".info.json"
    if path.exists():
        return [report("skipped", ".ai/.info.json")]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INFO_JSON_CONTENT, encoding="utf-8")
    return [report("created", ".ai/.info.json")]


def configure_config_yaml(target: Path) -> list[str]:
    """Configure .ai/config.yaml with workflow defaults."""
    path = target / ".ai" / "config.yaml"
    if path.exists():
        return [report("skipped", ".ai/config.yaml")]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(CONFIG_YAML_CONTENT, encoding="utf-8")
    return [report("created", ".ai/config.yaml")]


def configure_config_yaml_with_backend(target: Path, backend: str) -> list[str]:
    """Configure config.yaml with model backend settings."""
    path = target / ".ai" / "config.yaml"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if "models:" in existing:
            return [report("skipped", ".ai/config.yaml", "models section already exists")]
        model_section = MODELS_CONFIG_TEMPLATES.get(backend, MODELS_CONFIG_TEMPLATES["openai"])
        new_content = existing.rstrip() + "\n" + model_section
        path.write_text(new_content, encoding="utf-8")
        return [report("created", ".ai/config.yaml", "appended models section")]
    path.parent.mkdir(parents=True, exist_ok=True)
    model_section = MODELS_CONFIG_TEMPLATES.get(backend, MODELS_CONFIG_TEMPLATES["openai"])
    path.write_text(CONFIG_YAML_CONTENT + model_section, encoding="utf-8")
    return [report("created", ".ai/config.yaml", "created with models section")]



def generate_workspace(target: Path) -> list[str]:
    """Generate VS Code workspace file."""
    name = f'{target.resolve().name}.code-workspace'
    ws_path = target / name
    if ws_path.exists():
        return [report("skipped", name)]
    workspace = {
        "folders": [{"path": "."}],
        "settings": {
            "chat.includeApplyingInstructions": True,
            "chat.useAgentsMdFile": True,
            "chat.useCustomAgentHooks": True,
        },
    }
    ws_path.write_text(json.dumps(workspace, indent=2, ensure_ascii=False), encoding="utf-8")
    return [report("created", name)]
