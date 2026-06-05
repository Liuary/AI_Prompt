# AI_Prompt

**璺?AI 宸ュ叿鐨?Agent 寮€鍙戞不鐞嗘鏋?* 鈥?涓?AI 璁惧畾杈圭晫锛岃寮€鍙戣繃绋嬪彲鎺с€佸彲杩芥函銆佸彲鍗忎綔銆?

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/Liuary/AI_Prompt)
[![Plan](https://img.shields.io/badge/plan-v2.0--done-blue)](.ai/plan/plan.md)

```bash
python deploy.py /path/to/your-project          # 閮ㄧ讲鍏ㄩ儴
python deploy.py /path/to/your-project -k       # 浠?Kilo
python deploy.py /path/to/your-project -c       # 浠?Claude Code
python deploy.py /path/to/your-project -p       # 浠?GitHub Copilot
python deploy.py /path/to/your-project -o       # 浠?OpenCode
python deploy.py --help                         # 鏌ョ湅甯姪
```

---

## 蹇€熷紑濮?

```bash
git clone https://github.com/Liuary/AI_Prompt.git
cd AI_Prompt
python deploy.py /path/to/your-project
```

閮ㄧ讲鍚庣洰鏍囬」鐩幏寰楋細

| 鑳藉姏 | 璇存槑 |
|------|------|
| **琛屼负绾︽潫** | `AGENTS.md` 瀹氫箟 AI 鑳藉仛浠€涔堛€佷笉鑳藉仛浠€涔?|
| **宸ヤ綔鍖?* | `.ai/` 缁熶竴绠＄悊璁″垝銆佹棩蹇椼€佸鏌ャ€丅ug銆佺煡璇嗗簱 |
| **Agent 瑙掕壊** | 澶氳鑹蹭綋绯伙紙architect / code / tester / debug锛夛紝鎸夊伐鍏烽€傞厤 |
| **Skill 绯荤粺** | 6 涓彲澶嶇敤鎶€鑳芥ā鍧楋紝鎸夐渶璋冪敤 |
| **Hook 淇濇姢** | Copilot 鐩綍绾х紪杈戞帶鍒讹紝杩愯鏃跺己鍒堕檺鍒?|

## Obsidian 闆嗘垚

灏?`.ai/` 宸ヤ綔鍖哄湪 Obsidian 涓墦寮€涓?Vault锛屽嵆鍙湪鍥惧舰鍖栫晫闈腑绠＄悊椤圭洰锛?

```bash
python deploy.py /path/to/your-project --obsidian
```

閮ㄧ讲鍚庡湪 Obsidian 涓墦寮€鐩爣椤圭洰鐨?`.ai/` 鐩綍锛屼綘灏嗚幏寰楋細

| 鑳藉姏 | 璇存槑 |
|------|------|
| **鍙屽悜閾炬帴** | `[[wikilink]]` 鍦ㄨ鍒掋€佸鏌ャ€丅ug 鏂囦欢涔嬮棿鑷敱璺宠浆 |
| **鍥捐氨瑙嗗浘** | 鍙鍖栧伐浣滃尯鏂囦欢鐨勫叧鑱斿叧绯荤綉缁?|
| **浠〃鐩?* | `.ai/obsidian/dashboard.md` 浣跨敤 Dataview 鍔ㄦ€佹覆鏌撻樁娈电姸鎬併€佸鏌ユ潯鐩拰 Bug 鍒楄〃 |
| **鍏ㄥ眬鎼滅储** | 璺ㄦ墍鏈?.ai/ 鏂囦欢鐨勫叏鏂囨湰鎼滅储 |

璇︽儏鍙傝 [.ai/obsidian/README.md](.ai/obsidian/README.md)銆?

鏀寔鐨?AI 宸ュ叿锛?

| 宸ュ叿 | 鐘舵€?| 閮ㄧ讲閫夐」 | 閫傞厤鍐呭 |
|------|:--:|------|------|
| **Kilo** | 鉁?| `-k` | Agent + Skill + Instructions + kilo.jsonc |
| **Claude Code** | 鉁?| `-c` | CLAUDE.md + rules + skills + agents |
| **GitHub Copilot** | 鉁?| `-p` | copilot-instructions + instructions + skills + agents + Hook |
| **OpenCode** | 鉁?| `-o` | Agent + Skill + Instructions + opencode.jsonc |
| **Deep Code CLI** | 鉁?| `-d` | Skill + 鍚堝苟鐗?AGENTS |

---

## 瑙ｅ喅浠€涔堥棶棰?

- **AI 瀹规槗鏀硅秴鑼冨洿銆佽繃搴﹁璁°€佸繕璁版祴璇?* 鈫?绾︽潫浣撶郴锛? 鏉℃牳蹇冨噯鍒?+ 缂栫爜瑙勮寖 + 鎿嶄綔瑙勮寖锛?
- **璁″垝銆佹棩蹇椼€佸鏌ャ€丅ug銆佺煡璇嗘暎钀藉悇澶?* 鈫?缁熶竴鏀惰繘 `.ai/` 宸ヤ綔鍖猴紝缁撴瀯涓€鑷?
- **璋冭瘯缁忛獙涓嶈濉炶繘琛屼负绾︽潫** 鈫?鍗曠嫭鎷嗗嚭 `.ai/kb/` 鐭ヨ瘑搴擄紝绾︽潫涓庣煡璇嗗垎绂?
- **浜哄伐鍜岃嚜鍔ㄦ贩鍦ㄤ竴璧蜂簰鐩稿共鎵?* 鈫?鎷嗗垎涓?Agent 涓?Worker Agent锛屽弻杞ㄩ殧绂?
- **鍚勫伐鍏烽厤缃牸寮忎笉鍚岋紝缁存姢鎴愭湰楂?* 鈫?涓€閿儴缃诧紝鎸夊伐鍏风敓鎴愬師鐢熸牸寮?

---

## 鏋舵瀯

```
AI_Prompt/
鈹溾攢鈹€ AGENTS.md                    鈫?鏍稿績绾︽潫锛堟墍鏈夊伐鍏峰叡鐢級
鈹溾攢鈹€ instructions/                鈫?閫氱敤宸ヤ綔鍖鸿鑼?
鈹溾攢鈹€ skills/                      鈫?閫氱敤鎶€鑳斤紙6 涓級
鈹溾攢鈹€ deploy.py 鈫?deploy/          鈫?妯″潡鍖栭儴缃插紩鎿?
鈹溾攢鈹€ .ai/                         鈫?宸ヤ綔鍖烘鏋讹紙閮ㄧ讲鏃跺垱寤猴級
鈹溾攢鈹€ adapters/kilo/agents/                  鈫?Kilo Agent 瀹氫箟锛? 涓級
鈹溾攢鈹€ adapters/
鈹?  鈹溾攢鈹€ claude-code/             鈫?Claude Code锛欳LAUDE.md + agents + docs
鈹?  鈹溾攢鈹€ copilot/                 鈫?Copilot锛歩nstructions + skills + agents + scripts
鈹?  鈹溾攢鈹€ opencode/               鈫?OpenCode 閫傞厤鍣紙澶嶇敤 Kilo Agent锛?
鈹?  鈹斺攢鈹€ deepcode/                鈫?Deep Code CLI 閫傞厤鍣?
鈹斺攢鈹€ specs/ + rules/ + lib/ + tests/  鈫?瑙勫垯 DSL 寮曟搸
```

**鏍稿績 + 閫傞厤鍣?*锛歚AGENTS.md`銆乣instructions/`銆乣skills/` 鏄伐鍏锋棤鍏崇殑鏍稿績灞傦紝`Kilo/` 鍜?`adapters/` 灏嗘不鐞嗕綋绯荤炕璇戜负鍚勫伐鍏风殑鍘熺敓鏍煎紡銆?

---

## 绾︽潫浣撶郴

涓夊眰閫掕繘绾︽潫锛屼紭鍏堢骇浠庝綆鍒伴珮锛?

| 灞傜骇 | 鏂囦欢 | 璇存槑 |
|------|------|------|
| 姘镐箙绾︽潫 | `AGENTS.md` | 6 鏉℃牳蹇冭涓哄噯鍒?+ 缂栫爜椋庢牸锛岃法宸ュ叿閫氱敤 |
| 娴佺▼绾︽潫 | `instructions/core.md` | .ai/ 宸ヤ綔鍖烘搷浣滆鑼冿紙浼氳瘽鑷銆佽鍒掋€佸鏌ャ€丅ug 鐢熷懡鍛ㄦ湡锛?|
| 鍔ㄦ€佽鍒?| `.ai/dev/dev_core.md` | `[+]`/`[-]` 寮€鍏崇鐞嗭紝椤圭洰绾у畾鍒?|

绾︽潫锛堟€庝箞鍋氫簨锛変笌鐭ヨ瘑搴擄紙椤圭洰鏄粈涔堟牱锛変弗鏍煎垎绂伙紝浜掍笉娣锋穯銆?

---

## 宸ヤ綔娴佺▼

### 浜哄伐娴佺▼锛堥粯璁わ級

```text
鐢ㄦ埛 鈫?architect锛氬埗瀹氳鍒?
鐢ㄦ埛 鈫?code锛氬疄鐜板姛鑳?
鐢ㄦ埛 鈫?architect锛氫唬鐮佸鏌?
鐢ㄦ埛 鈫?code锛氫慨澶嶅鏌ラ棶棰?
鐢ㄦ埛 鈫?tester锛氭祴璇曘€佹彁浜?Bug
鐢ㄦ埛 鈫?code锛氫慨澶?Bug 鈫?楠屾敹閫氳繃
```

榛樿 `鎵ц妯″紡=manual`锛孉gent 鎸夌敤鎴锋寚浠ゅ伐浣滐紝閫傚悎闇€姹傚彉鍔ㄥ拰椋庨櫓杈冮珮鐨勯樁娈点€?

### 鑷姩闂幆锛堝彲閫夛級

寮€鍚?`鎵ц妯″紡=auto` + `鑷姩鎺ㄨ繘=enabled` 鍚庯紝AutoRunner 鍦ㄥ崟涓?worktree 鍐呬覆琛岃皟搴?Worker Agent锛?*缂栫爜 鈫?瀹℃煡 鈫?淇 鈫?娴嬭瘯 鈫?Bug 淇 鈫?done**銆傝嚜鍔ㄦ祦绋嬪彧鎺ㄨ繘鍒板瓙璁″垝瀹屾垚锛屾渶缁堝悎骞朵粛鐢辩敤鎴风‘璁ゃ€?

---

## v2.0 瀹屾垚

v2.0 鍥涗釜闃舵鍏ㄩ儴瀹屾垚锛岃瑙?[`.ai/plan/plan.md`](.ai/plan/plan.md)锛?

| 闃舵 | 鐩爣 | 鐘舵€?|
|------|------|:--:|
| 闃舵涓€ | 瑙勫垯 DSL + 缂栬瘧鍣?鏍￠獙鍣?+ 鐭ヨ瘑搴撹嚜鍔ㄥ寲 + 璺ㄤ細璇濊蹇?| 鉁?done |
| 闃舵浜?| 澶氫汉/澶欰gent 鍗忎綔锛堜换鍔″綊灞炪€佸啿绐佹娴嬨€佽繘搴﹀悓姝ワ級 | 鉁?done |
| 闃舵涓?| Claude Code + Copilot 閫傞厤鍣?+ 鏍囧噯鍖栨帴鍙?| 鉁?done |
| 闃舵鍥?| 瑙勮寖鏂囨。浣撶郴 + 妯℃澘甯傚満鍌ㄥ | 鉁?done |

---

## CLI 宸ュ叿

```bash
python scripts/ai_cli.py status              # 鎵€鏈夐樁娈电姸鎬佹瑙?
python scripts/ai_cli.py review              # 寰呭鐞嗗鏌ユ潯鐩?
python scripts/ai_cli.py bugs                # 寰呭鐞?Bug
python scripts/ai_cli.py log                 # 鏈€杩戞棩蹇楁憳瑕?
python scripts/ai_cli.py kb search <鏌ヨ>     # 鐭ヨ瘑搴撴悳绱?
python scripts/ai_cli.py kb list             # 鐭ヨ瘑搴撴枃浠跺垪琛?
```

## 椤圭洰鏂囨。

| 鏂囨。 | 璇存槑 |
|------|------|
| [`.ai/plan/plan.md`](.ai/plan/plan.md) | v2.0 澶ц鍒?|
| [`DEPLOY.md`](DEPLOY.md) | 閮ㄧ讲鎸囦护涓庡伐鍏蜂竴瑙?|
| [`ADAPTER_SPEC.md`](ADAPTER_SPEC.md) | 澶氬伐鍏烽€傞厤鍣ㄦ爣鍑嗗寲鎺ュ彛 |
| [`.ai/obsidian/README.md`](.ai/obsidian/README.md) | Obsidian Vault 闆嗘垚鎸囧崡 |
| [`docs/claude/claude-config.md`](docs/claude/claude-config.md) | Claude Code 閰嶇疆瑙勮寖 |
| [`docs/github/copilot-customization-guide.md`](docs/github/copilot-customization-guide.md) | Copilot 鑷畾涔夐厤缃寚鍗?|
| [`specs/OVERVIEW.md`](specs/OVERVIEW.md) | 瑙勮寖浣撶郴姒傝 |

---

## 绀轰緥椤圭洰

- [novel_create](https://github.com/Liuary/novel_create) 鈥?灏忚鍒涗綔宸ュ叿锛屼娇鐢?AI_Prompt 妯℃澘閮ㄧ讲

---

## 鎵嬪姩閮ㄧ讲锛堝弬鑰冿級

鑷姩閮ㄧ讲鎺ㄨ崘浣跨敤 `deploy.py`銆傚闇€鎵嬪姩鎿嶄綔锛岃瑙?[`DEPLOY.md`](DEPLOY.md)锛?

1. 澶嶅埗 `AGENTS.md` 鍒扮洰鏍囬」鐩牴鐩綍
2. 鍒涘缓 `.ai/` 宸ヤ綔鍖虹洰褰曠粨鏋?
3. 鎸夊伐鍏峰鍒舵寚浠?/ 鎶€鑳?/ Agent 鏂囦欢
4. 閰嶇疆 `.gitignore` 鍜?`.ai/.info.json`
5. 閫愰」楠岃瘉鎵€鏈夋枃浠跺氨浣?
