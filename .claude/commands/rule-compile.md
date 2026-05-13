#!/usr/bin/env python3
# .claude/commands/rule-compile.md
# Claude Code 命令：将规则 DSL 编译为 Markdown

## rule-compile

将 `rules/rules.yaml` 规则实例编译为 Markdown 格式输出。

### 用法

```
/rule-compile [--output OUTPUT]
```

- `--output OUTPUT`：输出文件路径（默认标准输出）

### 实现

调用 `python rule_cli.py compile [--output OUTPUT]`
