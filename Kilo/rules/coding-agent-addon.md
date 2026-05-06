# 代码 Agent 附加指令

代码 Agent 负责 **Bug 修复** 与 **审查问题处理**，完成后再调用对应 Agent 验收。每次会话启动时应：

1. 执行 `.ai/` 目录结构自检（见 `kilo_instructions_core.md` 会话启动自检章节），缺失则自动补建。
2. 调用 `load skill get-bugs` 获取待处理 Bug，调用 `load skill check-kb` 查阅知识库。
3. 分析用户指令是否需要计划化，若涉及多步骤 / 跨会话 / 多模块，主动更新 `.ai/plan/plan.md` 或 `.ai/dev/current.md`。

---

## Bug 修复流程

### 1. 发现 Bug

每次会话启动时，调用 `load skill get-bugs` 获取当前模块下状态为 `open` 或 `fixing` 的 Bug 列表。若存在 `open` Bug，将其作为当前会话的待处理项之一。

### 2. 承接 Bug

确定修复某个 Bug 后：
- 将 Bug 文件中 `- **状态**：open` 改为 `- **状态**：fixing`。
- 在 `## 修复记录` 表格中追加一行：`| {当前时间} | {username} | 开始修复 | - |`。
- 更新 `.ai/users/{username}/bugs/index.md` 中该 Bug 的状态。
- 更新 `.ai/users/{username}/bugs/log.md` 追加 `[模块/编号] fixing: 开始修复`。

### 3. 修复与记录

完成代码修改后：
- 在 `## 修复记录` 表格中追加一行：`| {当前时间} | {username} | {修复说明} | {commit hash} |`。
- 将 Bug 文件中 `- **状态**：fixing` 改为 `- **状态**：resolved`。
- 更新 `.ai/users/{username}/bugs/index.md` 中该 Bug 的状态。
- 更新 `.ai/users/{username}/bugs/log.md` 追加 `[模块/编号] resolved: {修复说明}`。

### 4. 请求验收

- 使用 `task` 工具调用 `tester` Subagent。
- Prompt 格式：`验收 BUG-{模块}-{编号}`。

---

## 审查问题处理流程

### 1. 发现审查问题

根据用户自然语言指令触发。当用户提及审查相关任务（如"处理审查问题""修复审查""review""代码审查"等）时，读取 `.ai/users/{username}/code_review/index.md`，列出各阶段 `pending` 状态的审查条目供用户选择。

### 2. 承接问题

确定处理某个审查条目后：
- 将该条目的状态从 `pending` 改为 `fixing`。
- 更新 `.ai/users/{username}/code_review/index.md` 中对应文件的状态计数。
- 更新 `.ai/users/{username}/code_review/log.md` 追加 `[REV-{stage}-{NO}] fixing: 开始处理`。

### 3. 修改与记录

完成代码修改后：
- 在对应条目的 `### 处理记录` 表格中追加一行：`| {当前时间} | {username} | {修改说明} | {commit hash} |`。
- 将该条目的状态从 `fixing` 改为 `resolved`。
- 更新 `.ai/users/{username}/code_review/index.md` 和 `log.md`。

### 4. 等待验收

审查条目标记为 `resolved` 后，由 Plan Agent 在下一轮审查中验收。无需代码 Agent 主动请求。
