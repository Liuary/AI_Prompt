# AI_Prompt 瑙勮寖浣撶郴姒傝

> 鏈€鍚庢洿鏂帮細2026-05-13

## 瑙勮寖娓呭崟

| 缂栧彿 | 鏂囦欢 | 璇存槑 |
|------|------|------|
| SPEC-01 | `rules.yaml` | 瑙勫垯 DSL Schema v1.0 鈥?9 瀛楁 + 4 鍏崇郴绫诲瀷 |
| SPEC-02 | `WORKSPACE.md` | .ai/ 宸ヤ綔鍖鸿鑼?鈥?鍏煙/绉佸煙缁撴瀯銆佹棩蹇?瀹℃煡/Bug 娴佺▼ |
| SPEC-03 | `AGENT_ROLES.md` | Agent 瑙掕壊瑙勮寖 鈥?9 涓?Agent 鐨勮亴璐ｃ€佹潈闄愩€佹祦杞?|
| SPEC-04 | `STATE_MACHINE.md` | 鐘舵€佹満瑙勮寖 鈥?status.md 鐢熷懡鍛ㄦ湡 |
| SPEC-05 | `RULE_SYSTEM.md` | 瑙勫垯 DSL 浣撶郴 鈥?缂栬瘧/鏍￠獙/鑷姩鍐欏叆 |
| 鈥?| `AIPACK.md` | .aipack 妯℃澘鎵撳寘鏍煎紡璁捐 |

## 闃呰椤哄簭

1. **鏂版垚鍛?*锛氬厛璇?`WORKSPACE.md` 浜嗚В椤圭洰缁撴瀯锛屽啀璇?`AGENT_ROLES.md` 浜嗚В鍒嗗伐
2. **寮€鍙戣€?*锛氬厛璇?`RULE_SYSTEM.md` 鍜?`rules.yaml` 浜嗚В瑙勫垯寮曟搸
3. **Architect**锛氬厛璇?`STATE_MACHINE.md` 浜嗚В鐘舵€佹祦杞?
## 瀹炵幇鐘舵€?
| 瑙勮寖 | 鐘舵€?| 鏍稿績浜х墿 |
|------|------|----------|
| SPEC-01 | 鉁?| `specs/rules.yaml` + `rules/rules.yaml` |
| SPEC-02 | 鉁?| `instructions/core.md` + `AGENTS.md` |
| SPEC-03 | 鉁?| `adapters/kilo/agents/` 涓?9 涓?Agent 瀹氫箟鏂囦欢 |
| SPEC-04 | 鉁?| `status.md` 鐘舵€佹満 + `plan/` 璁″垝浣撶郴 |
| SPEC-05 | 鉁?| `rule_cli.py` + `lib/rule_engine.py` + `tests/` |
