---
name: update-stage-status
description: 标准化更新 .ai/plan/{stage}/status.md 的子计划状态、责任 Agent 和状态记录，避免各 Agent 随意改写状态文件。适用于自动闭环和人工流程中的阶段状态变更。
---

# 更新子计划状态

## 输入

- 计划阶段名 `{stage}`
- 新状态 `{status}`
- 当前责任 Agent `{current_agent}`
- 上一责任 Agent `{previous_agent}`
- 说明 `{note}`
- 是否保持自动推进 `{keep_auto}`（默认保持原值）

## 执行步骤

### 1. 读取状态文件

读取 `.ai/plan/{stage}/status.md`。

若文件不存在，由 Architect 才能创建；其他 Agent 不得自行创建，必须提示用户或 Architect 先初始化阶段状态。

### 2. 校验状态变更

允许的状态值：

```text
planned | ready_for_code | coding | ready_for_review | review_failed | review_passed | ready_for_test | test_writing | testing | bug_found | bug_fixing | done | paused
```

若新状态不在列表中，停止并说明错误。

### 3. 更新字段

更新以下字段：

- `状态`
- `当前责任 Agent`
- `上一责任 Agent`
- `更新时间`

除非用户明确要求，否则不得改变：

- `执行模式`
- `自动推进`

### 4. 追加状态记录

在 `## 状态记录` 表格末尾追加：

```markdown
| yyyy-mm-dd HH:MM | {agent} | {旧状态} → {新状态} | {note} |
```

### 5. 安全暂停规则

遇到以下情况必须将状态改为 `paused`，当前责任 Agent 改为 `user`：

- 计划外架构变更
- 需要修改范围超过原计划
- 权限不明确
- 测试环境缺失
- 连续两次验收失败
- 自动推进链路无法判断下一步

### 6. 输出结果

输出更新摘要：

```markdown
已更新 {stage}/status.md：
- 状态：{旧状态} → {新状态}
- 当前责任 Agent：{current_agent}
- 自动推进：保持 {enabled/disabled}
```
