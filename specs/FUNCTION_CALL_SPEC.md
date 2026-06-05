# Agent Function Call Specification (FUNCTION_CALL_SPEC.md)

> Defines the standard Schema for Agent tool calls, aligned with OpenAI function calling format.
> All adapters (cloud API / local models) use this format uniformly for tool call interactions.

## 1. Message Format
Conversations between Agent and model use the OpenAI Chat Completions message format:
```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "You are a code Agent..."},
    {"role": "user", "content": "Fix the bug in src/main.py"},
    {"role": "assistant", "content": null, "tool_calls": [...]},
    {"role": "tool", "tool_call_id": "call_xxx", "content": "..."}
  ],
  "tools": [...]
}
```

## 2. Tool Definition Schema

Each tool definition follows this JSON Schema:
```json
{
  "type": "function",
  "function": {
    "name": "Tool name (English identifier)",
    "description": "Tool function description",
    "parameters": {
      "type": "object",
      "properties": {
        "param_name": {
          "type": "Parameter type (string/number/boolean/object/array)",
          "description": "Parameter description",
          "enum": ["Enumeration list of allowed values"],
          "required": ["List of required parameter names"]
        }
      },
      "required": ["List of required parameter names"]
    }
  }
}
```

### Tool Registration Example

```json
{
  "type": "function",
  "function": {
    "name": "edit",
    "description": "Performs exact string replacements in the specified file",
    "parameters": {
      "type": "object",
      "properties": {
        "filePath": {
          "type": "string",
          "description": "Absolute path of the file to modify"
        },
        "oldString": {
          "type": "string",
          "description": "The text to replace"
        },
        "newString": {
          "type": "string",
          "description": "The text to replace it with"
        },
        "replaceAll": {
          "type": "boolean",
          "description": "Whether to replace all occurrences"
        }
      },
      "required": ["filePath", "oldString", "newString"]
    }
  }
}
```

## 3. Tool Call Request
When the model decides to call a tool, the assistant message contains a `tool_calls` array:
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

### Field Descriptions

| Field | Type | Description |
|------|------|------|
| `id` | string | Unique tool call identifier, used for matching subsequent tool responses |
| `type` | string | Fixed value `function` |
| `function.name` | string | Name of the tool being called |
| `function.arguments` | string | JSON string, tool call parameters |

## 4. Tool Call Response
After the Agent executes the tool, it returns the result as a `tool` role message:
```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"success\": true, \"message\": \"File modified\"}"
}
```

`tool_call_id` must match the `id` in the request. `content` is in string format (complex results use JSON strings).

## 5. Parallel Tool Calls

The model can initiate multiple tool calls simultaneously (parallel execution):

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

After parallel execution, Agent returns the corresponding number of `tool` response messages.

## 6. Streaming Response
The model returns streaming responses via SSE (Server-Sent Events) format:
```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"delta":{"tool_calls":[{"index":0,"id":"call_abc","type":"function","function":{"name":"edit","arguments":""}}]}}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"delta":{"tool_calls":[{"index":0,"function":{"arguments":"{\"file"}}]}}]}

data: [DONE]
```

### Streaming tool_calls Aggregation Rules

- First chunk: carries `id`, `type`, `function.name`
- Subsequent chunks: only carry incremental `function.arguments` fragments
- Agent must concatenate arguments and parse JSON after receiving completion (`finish_reason=tool_calls`)

## 7. finish_reason Semantics

| finish_reason | Meaning | Agent Behavior |
|---------------|------|-----------|
| `stop` | Model completed reply, no tool calls | Return reply content to user |
| `tool_calls` | Model decided to call tools | Execute tool calls, return results to model |
| `length` | Exceeded token limit | Truncate or request continuation |
| `content_filter` | Content filtered by safety | Terminate current interaction, report filter reason |

## 8. Error Handling
The model may return abnormal tool call parameters; Agent must validate:

1. **Tool name not found**: return error tool message `{"error": "unknown tool: xxx"}`
2. **Parameter JSON parse failure**: return error `{"error": "invalid arguments JSON"}`
3. **Missing required parameter**: return error `{"error": "missing required param: filePath"}`
4. **Parameter type mismatch**: return error `{"error": "type mismatch: filePath expected string"}`

Error message format:
```json
{
  "role": "tool",
  "tool_call_id": "call_abc",
  "content": "{\"error\": \"unknown tool: undefined_tool\", \"available_tools\": [\"read\", \"write\", \"edit\", \"bash\", \"grep\", \"glob\"]}"
}
```

## 9. Local Model Compatibility
For locally deployed models such as Hermes-3, the following compatibility must be verified:

| Feature | OpenAI Format | Hermes Compatibility Requirement |
|------|------------|----------------|
| Message structure | `messages` array | Must support system/user/assistant/tool roles |
| Tool definition | `tools` array | Must support JSON Schema parameter definitions |
| Tool calls | `tool_calls` in assistant | Must generate `tool_calls` array |
| Streaming calls | SSE format | Must support incremental arguments streaming output |
| finish_reason | String enum | Must return `tool_calls` / `stop` |

## 10. References
- OpenAI Function Calling docs: https://platform.openai.com/docs/guides/function-calling
- Ollama API docs: https://github.com/ollama/ollama/blob/main/docs/api.md
- Hermes-3 Model (NousResearch): https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-8B
