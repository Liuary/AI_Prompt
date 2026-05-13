# 状态机规范 (STATE_MACHINE.md)

> 定义 `.ai/plan/{stage}/status.md` 的状态流转和自动闭环规则。

## 一、状态列表

| 状态 | 含义 | 操作者 |
|------|------|--------|
| `planned` | 计划已创建，等待确认 | Architect |
| `ready_for_code` | 可进入编码 | Architect |
| `coding` | 代码实现中 | Code / CodeWorker |
| `ready_for_review` | 等待审查 | Code → Architect |
| `review_failed` | 审查不通过 | Architect → Code |
| `review_passed` | 审查通过 | Architect |
| `ready_for_test` | 等待测试 | Architect |
| `test_writing` | 测试编写中 | TestWriter |
| `testing` | 测试执行中 | Tester |
| `bug_found` | 发现 Bug | Tester |
| `bug_fixing` | Bug 修复中 | Code |
| `done` | 阶段完成 | — |
| `paused` | 暂停 | user |

## 二、人工流程（默认）

```
planned → ready_for_code → coding → ready_for_review → review_failed ──┐
                                         │                              │
                                         └→ review_passed → done       │
                                         ┌──────────────────────────────┘
                                         └→ coding（修复后重新提交）
```

## 三、自动流程

```
auto_running ──→ CodeWorker → ReviewWorker → TestWriter → Tester
                    │              │                            │
                    └── bug_found ←┘                            │
                         │                                      │
                         └→ CodeWorker ──→ ReviewWorker ──→ done
```

## 四、暂停条件

任一 Agent 遇到以下情况须 `paused`：
- 计划外架构变更
- 权限不明确
- 测试环境缺失
- 连续两次验收失败

## 五、status.md 模板

```markdown
# {stage} 状态
- **执行模式**：manual | auto
- **自动推进**：disabled | enabled
- **状态**：{状态}
- **当前责任 Agent**：{agent}
- **更新时间**：yyyy-mm-dd HH:MM

## 任务清单
- [ ] ...
## 状态记录
| 时间 | Agent | 状态变化 | 说明 |
```
