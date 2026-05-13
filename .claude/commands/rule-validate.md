#!/usr/bin/env python3
# .claude/commands/rule-validate.md
# Claude Code 命令：校验规则的完整性

## rule-validate

校验 `rules/rules.yaml` 规则实例的完整性和一致性。

### 用法

```
/rule-validate [--verbose]
```

- `--verbose`：显示 info 级别提示

### 实现

调用 `python rule_cli.py validate [--verbose]`
