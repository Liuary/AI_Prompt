# Agent 鍑芥暟璋冪敤瑙勮寖 (FUNCTION_CALL_SPEC.md)

> 瀹氫箟 Agent 宸ュ叿璋冪敤鐨勬爣鍑?Schema锛屽榻?OpenAI function calling 鏍煎紡銆?> 鎵€鏈夐€傞厤鍣紙浜戠 API / 鏈湴妯″瀷锛夌粺涓€浣跨敤姝ゆ牸寮忚繘琛屽伐鍏疯皟鐢ㄤ氦浜掋€?
## 涓€銆佹秷鎭牸寮?
Agent 涓庢ā鍨嬩箣闂寸殑瀵硅瘽閲囩敤 OpenAI Chat Completions 娑堟伅鏍煎紡锛?
```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "浣犳槸涓€涓唬鐮?Agent鈥?},
    {"role": "user", "content": "淇 src/main.py 涓殑 Bug"},
    {"role": "assistant", "content": null, "tool_calls": [...]},
    {"role": "tool", "tool_call_id": "call_xxx", "content": "..."}
  ],
  "tools": [...]
}
```

## 浜屻€佸伐鍏峰畾涔?Schema

姣忎釜宸ュ叿瀹氫箟閬靛惊浠ヤ笅 JSON Schema锛?
```json
{
  "type": "function",
  "function": {
    "name": "宸ュ叿鍚嶇О锛堣嫳鏂囨爣璇嗙锛?,
    "description": "宸ュ叿鍔熻兘鎻忚堪锛堜腑鏂囷級",
    "parameters": {
      "type": "object",
      "properties": {
        "param_name": {
          "type": "鍙傛暟绫诲瀷锛坰tring/number/boolean/object/array锛?,
          "description": "鍙傛暟鎻忚堪",
          "enum": ["鍙€夊€肩殑鏋氫妇鍒楄〃"],
          "required": ["鏄惁涓哄繀濉弬鏁板垪琛?]
        }
      },
      "required": ["蹇呭～鍙傛暟鍚嶅垪琛?]
    }
  }
}
```

### 宸ュ叿娉ㄥ唽绀轰緥

```json
{
  "type": "function",
  "function": {
    "name": "edit",
    "description": "鍦ㄦ寚瀹氭枃浠朵腑鎵ц绮剧‘瀛楃涓叉浛鎹?,
    "parameters": {
      "type": "object",
      "properties": {
        "filePath": {
          "type": "string",
          "description": "瑕佷慨鏀圭殑鏂囦欢缁濆璺緞"
        },
        "oldString": {
          "type": "string",
          "description": "瑕佹浛鎹㈢殑鏂囨湰"
        },
        "newString": {
          "type": "string",
          "description": "鏇挎崲鍚庣殑鏂囨湰"
        },
        "replaceAll": {
          "type": "boolean",
          "description": "鏄惁鏇挎崲鎵€鏈夊尮閰嶉」"
        }
      },
      "required": ["filePath", "oldString", "newString"]
    }
  }
}
```

## 涓夈€佸伐鍏疯皟鐢ㄨ姹?
褰撴ā鍨嬪喅瀹氳皟鐢ㄥ伐鍏锋椂锛宎ssistant 娑堟伅涓寘鍚?`tool_calls` 鏁扮粍锛?
```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "edit",
        "arguments": "{\"filePath\":\"/path/to/file.py\",\"oldString\":\"foo\",\"newString\":\"bar\"}"
      }
    }
  ]
}
```

### 瀛楁璇存槑

| 瀛楁 | 绫诲瀷 | 璇存槑 |
|------|------|------|
| `id` | string | 宸ュ叿璋冪敤鍞竴鏍囪瘑锛岀敤浜庡悗缁?tool 鍝嶅簲鍖归厤 |
| `type` | string | 鍥哄畾鍊?`function` |
| `function.name` | string | 璋冪敤鐨勫伐鍏峰悕绉?|
| `function.arguments` | string | JSON 瀛楃涓诧紝宸ュ叿璋冪敤鍙傛暟 |

## 鍥涖€佸伐鍏疯皟鐢ㄥ搷搴?
Agent 鎵ц宸ュ叿鍚庯紝灏嗙粨鏋滀互 `tool` 瑙掕壊娑堟伅杩斿洖锛?
```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"success\": true, \"message\": \"鏂囦欢宸蹭慨鏀筡"}"
}
```

`tool_call_id` 蹇呴』涓庤姹備腑鐨?`id` 鍖归厤銆俙content` 涓哄瓧绗︿覆鏍煎紡锛堝鏉傜粨鏋滀娇鐢?JSON 瀛楃涓诧級銆?
## 浜斻€佸宸ュ叿骞惰璋冪敤

妯″瀷鍙悓鏃跺彂璧峰涓伐鍏疯皟鐢紙骞惰鎵ц锛夛細

```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {"id": "call_1", "type": "function", "function": {"name": "read", "arguments": "{\"filePath\":\"a.py\"}"}},
    {"id": "call_2", "type": "function", "function": {"name": "read", "arguments": "{\"filePath\":\"b.py\"}"}},
    {"id": "call_3", "type": "function", "function": {"name": "grep", "arguments": "{\"pattern\":\"TODO\"}"}}
  ]
}
```

Agent 骞惰鎵ц鍚庯紝杩斿洖瀵瑰簲鏁伴噺鐨?`tool` 鍝嶅簲娑堟伅銆?
## 鍏€佹祦寮忓搷搴?
妯″瀷閫氳繃 SSE (Server-Sent Events) 鏍煎紡杩斿洖娴佸紡鍝嶅簲锛?
```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"delta":{"tool_calls":[{"index":0,"id":"call_abc","type":"function","function":{"name":"edit","arguments":""}}]}}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"delta":{"tool_calls":[{"index":0,"function":{"arguments":"{\"file"}}]}}]}

data: [DONE]
```

### 娴佸紡 tool_calls 鑱氬悎瑙勫垯

- 棣栦釜 chunk锛氭惡甯?`id`銆乣type`銆乣function.name`
- 鍚庣画 chunk锛氬彧鎼哄甫 `function.arguments` 澧為噺鐗囨
- Agent 闇€鍦ㄦ帴鏀跺畬鎴愶紙`finish_reason=tool_calls`锛夊悗鎷兼帴 arguments 骞惰В鏋?JSON

## 涓冦€乫inish_reason 璇箟

| finish_reason | 鍚箟 | Agent 琛屼负 |
|---------------|------|-----------|
| `stop` | 妯″瀷瀹屾垚鍥炲锛屾棤宸ュ叿璋冪敤 | 灏嗗洖澶嶅唴瀹硅繑鍥炵敤鎴?|
| `tool_calls` | 妯″瀷鍐冲畾璋冪敤宸ュ叿 | 鎵ц宸ュ叿璋冪敤锛屽皢缁撴灉杩斿洖妯″瀷 |
| `length` | 瓒呰繃 token 涓婇檺 | 鎴柇鎴栬姹傜画鍐?|
| `content_filter` | 鍐呭琚畨鍏ㄨ繃婊?| 缁堟褰撳墠浜や簰锛屾姤鍛婅繃婊ゅ師鍥?|

## 鍏€侀敊璇鐞?
妯″瀷鍙兘杩斿洖寮傚父鐨勫伐鍏疯皟鐢ㄥ弬鏁帮紝Agent 闇€杩涜鏍￠獙锛?
1. **宸ュ叿鍚嶄笉瀛樺湪**锛氳繑鍥為敊璇?tool 娑堟伅 `{"error": "unknown tool: xxx"}`
2. **鍙傛暟 JSON 瑙ｆ瀽澶辫触**锛氳繑鍥為敊璇?`{"error": "invalid arguments JSON"}`
3. **蹇呭～鍙傛暟缂哄け**锛氳繑鍥為敊璇?`{"error": "missing required param: filePath"}`
4. **鍙傛暟绫诲瀷涓嶅尮閰?*锛氳繑鍥為敊璇?`{"error": "type mismatch: filePath expected string"}`

閿欒娑堟伅鏍煎紡锛?
```json
{
  "role": "tool",
  "tool_call_id": "call_abc",
  "content": "{\"error\": \"unknown tool: undefined_tool\", \"available_tools\": [\"read\", \"write\", \"edit\", \"bash\", \"grep\", \"glob\"]}"
}
```

## 涔濄€佹湰鍦版ā鍨嬪吋瀹?
瀵逛簬鏈湴閮ㄧ讲鐨?Hermes-3 绛夋ā鍨嬶紝椤婚獙璇佷互涓嬪吋瀹规€э細

| 鐗规€?| OpenAI 鏍煎紡 | Hermes 鍏煎瑕佹眰 |
|------|------------|----------------|
| 娑堟伅缁撴瀯 | `messages` 鏁扮粍 | 蹇呴』鏀寔 system/user/assistant/tool 瑙掕壊 |
| 宸ュ叿瀹氫箟 | `tools` 鏁扮粍 | 蹇呴』鏀寔 JSON Schema 鍙傛暟瀹氫箟 |
| 宸ュ叿璋冪敤 | `tool_calls` in assistant | 蹇呴』鐢熸垚 `tool_calls` 鏁扮粍 |
| 娴佸紡璋冪敤 | SSE format | 蹇呴』鏀寔澧為噺 arguments 娴佸紡杈撳嚭 |
| finish_reason | 瀛楃涓叉灇涓?| 蹇呴』杩斿洖 `tool_calls` / `stop` |

## 鍗併€佸弬鑰?
- OpenAI Function Calling 鏂囨。: https://platform.openai.com/docs/guides/function-calling
- Ollama API 鏂囨。: https://github.com/ollama/ollama/blob/main/docs/api.md
- Hermes-3 妯″瀷 (NousResearch): https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-8B
