# Claude Code 项目指令

> 本文件为 Claude Code 特化内容。通用行为约束见项目根目录的 `AGENTS.md`。

## 可用命令

| 命令 | 说明 |
|------|------|
| `/rule-compile` | 将 rules/rules.yaml 规则 DSL 编译为 Markdown |
| `/rule-validate` | 校验规则的完整性和一致性 |

用法：直接在对话中输入 `/rule-compile` 或 `/rule-validate`。

## 与 AGENTS.md 的关系

Claude Code 同时加载 `AGENTS.md`（项目根目录）和本文件。本文件仅补充 Claude Code 特有的工具链命令，不重复通用约束。
