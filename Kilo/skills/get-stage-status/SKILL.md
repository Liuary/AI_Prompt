---
name: get-stage-status
description: 读取 .ai/plan/{stage}/status.md，判断当前子计划状态、责任 Agent、是否允许自动推进以及下一步建议。用于 Architect/Code/TestWriter/Tester 在处理阶段任务前确认流程状态。
---

# 获取子计划状态

## 输入

- 计划阶段名 `{stage}`（如 `stage01`、`auth-login`）
- 若用户未提供阶段名，先读取 `.ai/plan/plan_index.md` 查找当前活跃阶段；仍不明确时询问用户

## 执行步骤

### 1. 定位状态文件

读取 `.ai/plan/{stage}/status.md`。

若文件不存在：
- 不要自行进入自动流程。
- 返回 `missing_status`，提示需要 Architect 先创建状态文件。

### 2. 提取字段

解析以下字段：

- `执行模式`
- `自动推进`
- `状态`
- `当前责任 Agent`
- `上一责任 Agent`
- `更新时间`
- `当前任务`
- `阻塞 / 暂停原因`

### 3. 判断自动推进资格

只有同时满足以下条件才返回 `can_auto_continue = true`：

- `执行模式` 为 `auto`
- `自动推进` 为 `enabled`
- `状态` 不是 `done` 或 `paused`
- `当前责任 Agent` 不是 `user`

否则返回 `can_auto_continue = false`，并说明原因。

### 4. 输出格式

```markdown
## 子计划状态

- 阶段：{stage}
- 执行模式：manual | auto
- 自动推进：disabled | enabled
- 状态：{status}
- 当前责任 Agent：{agent}
- 可自动推进：true | false
- 阻塞原因：{reason 或 无}

## 下一步建议
{根据状态给出下一步，例如：启动 Code、等待用户、启动 Tester、停止流程}
```

## 状态到下一步映射

| 状态 | 下一步建议 |
|------|------------|
| `planned` | 等待用户确认或 Architect 细化计划 |
| `ready_for_code` | Architect 可启动 Code |
| `coding` | Code 正在开发 |
| `ready_for_review` | Code 可启动 Architect 审查，或等待用户触发 |
| `review_failed` | Architect 可启动 Code 修复审查问题 |
| `review_passed` | Architect 可推进到 ready_for_test |
| `ready_for_test` | Architect 可启动 TestWriter 或 Tester |
| `test_writing` | TestWriter 正在写测试 |
| `testing` | Tester 正在测试 |
| `bug_found` | Tester 可启动 Code 修复 Bug |
| `bug_fixing` | Code 正在修复 Bug |
| `done` | 流程完成，停止 |
| `paused` | 等待用户处理暂停原因 |
