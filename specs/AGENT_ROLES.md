# Agent 角色规范 (AGENT_ROLES.md)

> AI_Prompt 定义 9 个 Agent 角色，覆盖计划→编码→审查→测试→Bug 全流程。

## 一、角色总览

| Agent | 类型 | 职责 | 权限范围 |
|-------|------|------|----------|
| **Architect** | 主 | 计划管理、代码审查（提交/验收） | `.ai/` 只读源码 |
| **Code** | 主 | Bug 修复、审查问题处理 | `*` 全文件 |
| **CodeWorker** | 子 | 自动闭环中的编码实现 | `*` 全文件 |
| **Ask** | 主 | 回答技术问题、查阅资料 | 只读 |
| **Debug** | 子 | 缺陷排查与根因分析 | 只读源码 |
| **ReviewWorker** | 子 | 自动闭环中的代码审查 | `.ai/` 只读源码 |
| **Tester** | 子 | Bug 提交与修复验收 | 只读源码 |
| **TestWriter** | 子 | 自动闭环中的测试编写 | `*` 全文件 |
| **AutoRunner** | 子 | 单 worktree 自动闭环调度 | `*` |

## 二、人工流程

```
User → Architect（计划+审查提交）
     → Code（编码+修复）
     → Tester（验收）
```

## 三、自动流程

```
Architect → AutoRunner（worktree 内串行）
         → CodeWorker（编码）
         → ReviewWorker（审查）
         → TestWriter（测试）
         → Tester（验收）
         → Debug（排错）
```

## 四、关键约束

- **发现者与修复者分离**：Architect 提交的审查/测试 Agent 提交的 Bug，不得自行修复
- **Code/CodeWorker 区分**：人工流程用 Code，自动流程用 CodeWorker，职责隔离
- **AutoRunner 唯一启动者**：Architect 启动 AutoRunner，AutoRunner 内部不得再创建新 worktree
- 遇到连续两次验收失败 → `paused`，责任转 `user`
- 计划外架构变更 → `paused`

## 五、Agent 定义位置

所有 Agent 提示词位于 `Kilo/agents/`，权限在 YAML 头 `permission` 字段声明。
