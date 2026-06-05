# Agent 瑙掕壊瑙勮寖 (AGENT_ROLES.md)

> AI_Prompt 瀹氫箟 9 涓?Agent 瑙掕壊锛岃鐩栬鍒掆啋缂栫爜鈫掑鏌モ啋娴嬭瘯鈫払ug 鍏ㄦ祦绋嬨€?
## 涓€銆佽鑹叉€昏

| Agent | 绫诲瀷 | 鑱岃矗 | 鏉冮檺鑼冨洿 |
|-------|------|------|----------|
| **Architect** | 涓?| 璁″垝绠＄悊銆佷唬鐮佸鏌ワ紙鎻愪氦/楠屾敹锛?| `.ai/` 鍙婧愮爜 |
| **Code** | 涓?| Bug 淇銆佸鏌ラ棶棰樺鐞?| `*` 鍏ㄦ枃浠?|
| **CodeWorker** | 瀛?| 鑷姩闂幆涓殑缂栫爜瀹炵幇 | `*` 鍏ㄦ枃浠?|
| **Ask** | 涓?| 鍥炵瓟鎶€鏈棶棰樸€佹煡闃呰祫鏂?| 鍙 |
| **Debug** | 瀛?| 缂洪櫡鎺掓煡涓庢牴鍥犲垎鏋?| 鍙婧愮爜 |
| **ReviewWorker** | 瀛?| 鑷姩闂幆涓殑浠ｇ爜瀹℃煡 | `.ai/` 鍙婧愮爜 |
| **Tester** | 瀛?| Bug 鎻愪氦涓庝慨澶嶉獙鏀?| 鍙婧愮爜 |
| **TestWriter** | 瀛?| 鑷姩闂幆涓殑娴嬭瘯缂栧啓 | `*` 鍏ㄦ枃浠?|
| **AutoRunner** | 瀛?| 鍗?worktree 鑷姩闂幆璋冨害 | `*` |

## 浜屻€佷汉宸ユ祦绋?
```
User 鈫?Architect锛堣鍒?瀹℃煡鎻愪氦锛?     鈫?Code锛堢紪鐮?淇锛?     鈫?Tester锛堥獙鏀讹級
```

## 涓夈€佽嚜鍔ㄦ祦绋?
```
Architect 鈫?AutoRunner锛坵orktree 鍐呬覆琛岋級
         鈫?CodeWorker锛堢紪鐮侊級
         鈫?ReviewWorker锛堝鏌ワ級
         鈫?TestWriter锛堟祴璇曪級
         鈫?Tester锛堥獙鏀讹級
         鈫?Debug锛堟帓閿欙級
```

## 鍥涖€佸叧閿害鏉?
- **鍙戠幇鑰呬笌淇鑰呭垎绂?*锛欰rchitect 鎻愪氦鐨勫鏌?娴嬭瘯 Agent 鎻愪氦鐨?Bug锛屼笉寰楄嚜琛屼慨澶?- **Code/CodeWorker 鍖哄垎**锛氫汉宸ユ祦绋嬬敤 Code锛岃嚜鍔ㄦ祦绋嬬敤 CodeWorker锛岃亴璐ｉ殧绂?- **AutoRunner 鍞竴鍚姩鑰?*锛欰rchitect 鍚姩 AutoRunner锛孉utoRunner 鍐呴儴涓嶅緱鍐嶅垱寤烘柊 worktree
- 閬囧埌杩炵画涓ゆ楠屾敹澶辫触 鈫?`paused`锛岃矗浠昏浆 `user`
- 璁″垝澶栨灦鏋勫彉鏇?鈫?`paused`

## 浜斻€丄gent 瀹氫箟浣嶇疆

鎵€鏈?Agent 鎻愮ず璇嶄綅浜?`adapters/kilo/agents/`锛屾潈闄愬湪 YAML 澶?`permission` 瀛楁澹版槑銆?