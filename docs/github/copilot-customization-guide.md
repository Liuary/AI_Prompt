# Copilot 自定义配置整合指南

## 目的

本文作为当前仓库中 Copilot 自定义配置的唯一整合文档，统一说明以下内容：

- 全局约束、Instructions、Skill、Custom Agent、Hook 的边界与选型
- 本仓库已出现问题的根因、修正结果与维护规范
- 可直接复用的案例、正确/错误对照与推荐模板
- 后续排查与验证的标准流程

本文已经吸收并修正了旧的 `.ai/kb/copilot-customization.md`、`.ai/kb/copilot-customization-examples.md`、`.ai/kb/copilot-customization-guide.md` 三份文档内容，后续应只维护本文件。

## 当前仓库现状

- 已存在根目录 `AGENTS.md`，作为项目级行为约束源头
- 已存在 `.github/copilot-instructions.md`，作为面向 Copilot 的适配层，且文件头说明为自动生成
- 已存在 `.github/instructions/workspace.instructions.md`，用于 `.ai/` 工作区规则
- 已存在 `.github/agents/architect.agent.md`、`.github/agents/code.agent.md`、`.github/agents/reviewer.agent.md`
- 已存在 `.github/skills/` 目录，包含若干工作流 Skill
- 已存在 `.github/scripts/restrict-edit-scope.ps1`，用于在 Hook 中限制编辑范围
- 已存在 `copilot.code-workspace`，并显式配置了相关 Chat 设置
- `.ai/kb/` 已建立知识库文档，不再为空

## 快速结论

- 项目级、几乎每次都成立的约束，进入 `AGENTS.md` 或 `.github/copilot-instructions.md`
- 只对特定文件类型、目录或任务场景生效的规则，进入 `.instructions.md`
- 需要按需触发、并可能附带模板或脚本的复用流程，进入 Skill
- 需要独立角色、工具权限控制、子 Agent 委派能力的，进入 `.agent.md`
- 需要在运行时对工具调用进行硬拦截或审批的，进入 Hook
- 若某个 Agent 需要“全部权限”，不要枚举 `tools`，直接省略该字段以继承默认工具集

## 配置类型与边界

### 1. 全局约束文件

适用场景：

- 对整个仓库都成立的编码、测试、文档、协作规则
- 需要在绝大多数任务中持续生效的要求

常见文件：

- `AGENTS.md`
- `.github/copilot-instructions.md`

本仓库处理原则：

- `AGENTS.md` 作为规则源头
- `.github/copilot-instructions.md` 作为 Copilot 适配层，不建议直接长期手改
- 若两者出现漂移，优先确认 `AGENTS.md` 是否仍为唯一源头

### 2. 文件级 Instructions

适用场景：

- 只针对某一类文件或目录生效
- 规则不会覆盖整个仓库，只在特定工作面出现

典型例子：

- `.ai/` 工作区规则
- 前端组件目录的样式约定
- 数据迁移脚本的安全要求

建议位置：

- `.github/instructions/*.instructions.md`

使用要点：

- `description` 必须写清楚“什么时候用”
- `applyTo` 只匹配必要范围，不要无差别写成 `**`
- 一份 instruction 只管一个主题，避免把测试、接口、样式塞进同一文件

### 3. Skill

适用场景：

- 某类任务会重复出现，但不是每次聊天都需要
- 除了说明文字，还需要脚本、模板、参考文档等配套资源

建议位置：

- `.github/skills/<skill-name>/SKILL.md`

目录结构建议：

- `SKILL.md`：入口说明
- `scripts/`：自动化脚本
- `references/`：较长参考资料
- `assets/`：模板、样板文件

判断标准：

- 如果它更像“工作流包”，用 Skill
- 如果只是几条简短规范，不要升级成 Skill

### 4. 自定义 Agent

适用场景：

- 需要一个专门角色处理某类任务
- 需要限制工具权限，避免主 Agent 拿到过多能力
- 需要上下文隔离，作为子 Agent 被委派执行

建议位置：

- `.github/agents/*.agent.md`

判断标准：

- 如果只是复用流程，不需要新人格或权限隔离，优先 Skill
- 如果需要“谁来做”和“能用哪些工具”都单独定义，使用 Custom Agent

### 5. Hook

适用场景：

- 需要在运行时对工具调用做硬性限制，而不是只靠文案约束模型
- 需要对单次编辑、命令执行、审批流程进行 allow、ask、deny 控制

建议位置：

- Agent 内联 `hooks`
- `.github/hooks/*.json`

判断标准：

- 如果只是希望模型“尽量遵守”，用 Instructions 或 Agent 文案
- 如果必须强制阻止越界编辑、危险命令或未经确认的操作，用 Hook

## 选型顺序

新增 Copilot 配置时，按以下顺序判断：

1. 这条规则是不是整个仓库都需要？如果是，进入全局约束文件。
2. 这条规则是不是只针对某类文件或目录？如果是，用 `.instructions.md`。
3. 这件事是不是可重复执行的工作流，还需要模板或脚本？如果是，用 Skill。
4. 这件事是不是需要单独角色、权限隔离或子 Agent 调度？如果是，用 `.agent.md`。
5. 这件事是不是必须在运行时强制拦截？如果是，再补 Hook。

## 本次修正背景

### 问题现象

- `workspace.instructions.md` 已存在，但在处理 `.ai` 工作区任务时体感不稳定
- `architect`、`code`、`reviewer` 的 `tools` 字段与 VS Code 官方工具别名不一致
- `architect` 与 `reviewer` 的“只改特定目录”仅停留在文案约束，缺少硬性拦截
- `architect` 与 `reviewer` 对审查文档的落盘路径存在描述不一致
- `Architect` 在 UI 中一度表现为近似全权限，和预期不符
- `Code` Agent 先前被误配为“仅四类工具”，不符合“全部权限”的需求

### 根因分析

1. `.instructions.md` 的 `applyTo` 主要用于匹配目标文件后的自动附加，不能单独等价为“读取某目录时总会生效”。如果 `description` 不够明确，按任务语义触发的概率会偏低。
2. `.agent.md` 的 `tools` 需要使用 VS Code 官方支持的别名。此前使用的 `grep`、`glob`、`bash`、`write` 并不是该格式的标准别名，不可识别项会被忽略，导致权限与预期不一致。
3. `.agent.md` 原生只能限制“可用工具种类”，不能直接限制“可编辑目录范围”。仅在正文中写“只允许编辑 .ai/”并不能形成强制保护。
4. 工作区未显式启用 `chat.includeApplyingInstructions` 与 `chat.useCustomAgentHooks`，导致文件型指令和 agent-scoped hook 的生效前提不够明确。
5. 审查文档路径没有统一规范，导致 agent 之间对输出位置的理解不一致。
6. 若 `.instructions.md` 或 `.agent.md` 缺少 frontmatter 起始分隔符 `---`，VS Code 不会按自定义配置解析 header，相关 `tools`、`applyTo`、`hooks` 都可能失效或退回默认表现。
7. 若希望某个 Agent 拥有默认全部工具能力，却手工枚举了 `tools`，该 Agent 反而会被限制为枚举出的子集。

### 本次修正

- `workspace.instructions.md`：补强 `description`，使其同时覆盖 `.ai` 工作区任务语义与目录范围
- `architect.agent.md`：保留 `read`、`search`、`edit`，增加 `PreToolUse` hook，将输出路径统一到 `.ai/` 范围内
- `code.agent.md`：移除 `tools` 限制，默认继承当前环境中的全部可用工具能力
- `reviewer.agent.md`：改为 `read`、`search`、`edit`，并通过 hook 强制仅可写入 `.ai/code_review/`
- `copilot.code-workspace`：显式开启 `chat.includeApplyingInstructions`、`chat.useAgentsMdFile`、`chat.useCustomAgentHooks`
- `.github/scripts/restrict-edit-scope.ps1`：新增通用路径限制脚本，供 custom agent 的 `PreToolUse` hook 复用
- `.ai/dev/current.md` 与 `.ai/log/dev_last.md`：补齐任务记录与最近一次处理记录

## 统一配置规范

### 1. 指令文件规范

- `.github/copilot-instructions.md` 用于全局、常驻、跨任务的仓库级规则
- `.github/instructions/*.instructions.md` 用于文件或目录定向规则
- 所有带 YAML frontmatter 的自定义文件都必须同时具备起始和结束分隔符 `---`
- `description` 必须写清“Use when...”或等价触发语义，避免只写抽象标题
- `applyTo` 使用相对工作区根目录的 glob；目录规则优先写成 `.ai/**`、`src/**` 这类清晰模式
- 若规则依赖自动附加，工作区需显式开启 `chat.includeApplyingInstructions`

### 2. Custom Agent 规范

- `.github/agents/*.agent.md` 的 `tools` 只能使用 VS Code 官方别名或明确可用的扩展工具
- 若 frontmatter 头部缺少起始 `---`，该 Agent 的 `tools`、`hooks`、`model` 等配置都不应视为有效
- 若某个 Agent 需要“全部权限”，不要枚举 `tools`，直接省略该字段以继承默认工具集
- 当前项目内优先使用的官方别名为：`read`、`search`、`edit`、`execute`、`agent`、`web`、`todo`
- 只读 Agent 至少使用 `read`、`search`；可落盘审查或计划文档的 Agent 需要额外声明 `edit`
- 如果 Agent 只能处理特定目录，正文说明不算完成，必须补充 Hook 做强制限制
- Agent 的 `description` 要同时描述职责、读写边界和适用场景

### 3. Hook 规范

- 目录级编辑约束通过 `PreToolUse` hook 实现，不依赖模型自行遵守
- Hook 脚本只做一件事：读取 `stdin` JSON，判断 `tool_name` 与 `tool_input` 中的目标路径，并返回 `allow`、`ask` 或 `deny`
- Hook 需要兼容相对路径与绝对路径，并将判断统一到工作区相对路径上
- 若无法从工具输入中识别目标路径，默认返回 `ask`，而不是静默放行
- 使用 agent-scoped hooks 时，工作区必须开启 `chat.useCustomAgentHooks`

### 4. 工作区设置规范

- `copilot.code-workspace` 至少显式包含以下设置：
	- `chat.includeApplyingInstructions: true`
	- `chat.useAgentsMdFile: true`
	- `chat.useCustomAgentHooks: true`
- 若未来新增自定义位置，再补充 `chat.instructionsFilesLocations`、`chat.agentFilesLocations`、`chat.hookFilesLocations`

### 5. 审查与记录规范

- 共享审查产物统一写入 `.ai/code_review/`
- `.ai/users/` 保留为成员私域，不作为团队共享审查结果的默认落点
- 每次修正 Copilot 配置后，同步更新 `.ai/dev/current.md`、`.ai/log/dev_last.md` 和相关知识库文档

## 具体案例

### 案例 1：为 `.ai` 工作区编写可自动应用的 instructions

适用场景：希望 AI 在处理 `.ai/` 下的计划、日志、知识库文件时自动带上工作区规则。

```md
---
description: "Use when working with files under .ai/: 创建、编辑、维护 .ai/dev、.ai/log、.ai/plan、.ai/bugs、.ai/kb、.ai/code_review 中的计划、日志、Bug、知识库和审查记录。"
applyTo: ".ai/**"
---

# .ai/ 工作区操作规范

- 修改 `.ai/dev/current.md` 声明任务和文件锁定
- 每次操作后同步更新 `.ai/log/` 和 `dev_last.md`
```

要点：

- 首行必须有 `---`
- `description` 既要说明目录，也要写清任务语义
- `applyTo` 只负责文件匹配，不能替代 `description` 的任务发现能力

### 案例 2：为受限的 Architect Agent 配置最小权限

适用场景：允许读取源码和搜索信息，但只能把结果写入 `.ai` 文档。

```md
---
name: architect
description: 用于项目计划管理、协作状态维护与代码审查；可读取和搜索源码，但只应编辑 .ai/ 目录下的文档记录，不直接修改业务源码。
tools:
	- read
	- search
	- edit
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/"'
---
```

要点：

- `edit` 只表示“可以编辑”，不表示“只能编辑某目录”
- 真正的目录限制需要靠 `PreToolUse` hook 执行
- 如果 frontmatter 起始 `---` 丢失，`tools` 和 `hooks` 都可能失效

### 案例 3：为 Code Agent 配置“全部权限”

适用场景：希望 Code Agent 默认继承当前环境里的全部可用工具，而不是手工枚举一部分。

```md
---
name: code
description: 用于 Bug 修复、问题处理与必要的验证；不限制工具集合，默认使用当前环境中的全部可用工具能力。
---
```

错误示例：

```md
---
name: code
description: Bug 修复 Agent
tools:
	- read
	- search
	- edit
	- execute
---
```

说明：上面的错误示例并不是语法错，而是语义上会把 Code Agent 限制为枚举出的那几个工具，无法达到“全部权限”的目标。

### 案例 4：为 Reviewer Agent 限制只能写入 `.ai/code_review/`

适用场景：代码审查 Agent 只允许输出审查记录，禁止编辑源码或其他 `.ai` 文档。

```md
---
name: reviewer
description: 用于代码审查；只读取和搜索源码，仅在 .ai/code_review/ 下写入审查文档，不直接修改业务源码。
tools:
	- read
	- search
	- edit
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/code_review/"'
---
```

预期效果：

- 编辑 `.ai/code_review/REV-1.md` 时返回 `allow`
- 编辑 `.ai/kb/copilot-customization.md` 时返回 `deny`
- 工具输入里无法识别目标路径时返回 `ask`

### 案例 5：`PreToolUse` hook 的最小配置与返回结果

适用场景：希望对单次工具调用做硬性批准、询问或拒绝，而不是只靠提示词约束。

Agent 内联 hook 示例：

```yaml
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/"'
```

脚本返回 `deny` 的 JSON 示例：

```json
{
	"hookSpecificOutput": {
		"hookEventName": "PreToolUse",
		"permissionDecision": "deny",
		"permissionDecisionReason": "This agent may only edit these paths: .ai. Blocked target paths: AGENTS.md."
	}
}
```

脚本返回 `ask` 的 JSON 示例：

```json
{
	"hookSpecificOutput": {
		"hookEventName": "PreToolUse",
		"permissionDecision": "ask",
		"permissionDecisionReason": "Unable to determine the target file path from tool input. Please confirm before continuing."
	}
}
```

### 案例 6：排查“配置看起来对，但界面权限不对”

适用场景：Agent 文件已经写了 `tools`，但 UI 中仍然像是全权限或默认权限。

排查顺序：

1. 检查文件首行是否为 `---`
2. 检查 `tools` 是否使用官方别名，而不是 `grep`、`glob`、`bash`、`write` 这类旧写法
3. 检查工作区是否开启 `chat.useAgentsMdFile` 与 `chat.useCustomAgentHooks`
4. 在 Chat Customizations Diagnostics 中确认该 Agent 是否已被正确加载
5. 若文件已修正但 UI 未刷新，执行一次 `Developer: Reload Window`

## 正确与错误对照

### 对照 1：frontmatter 起始分隔符

正确示例：

```md
---
name: architect
description: 只读源码，写入 .ai 文档
tools:
	- read
	- search
	- edit
---
```

错误示例：

```md
name: architect
description: 只读源码，写入 .ai 文档
tools:
	- read
	- search
	- edit
---
```

影响：第二种写法里，VS Code 很可能把整个头部当普通 Markdown，`tools` 和 `hooks` 都不会按配置生效。

### 对照 2：旧工具别名与官方工具别名

正确示例：

```md
tools:
	- read
	- search
	- edit
	- execute
```

错误示例：

```md
tools:
	- read
	- grep
	- glob
	- bash
```

影响：`grep`、`glob`、`bash` 属于旧体系或其他环境下的命名，在当前 VS Code custom agent 语义里不能当作通用官方别名依赖。

### 对照 3：全部权限与部分工具枚举

正确示例：

```md
---
name: code
description: 默认使用全部可用工具能力。
---
```

错误示例：

```md
---
name: code
description: 希望拥有全部权限。
tools:
	- read
	- search
	- edit
	- execute
---
```

影响：错误示例会把 Agent 限制在这四类工具内，而不是继承默认工具集。

### 对照 4：目录限制只写在文案里 vs 配置级强制限制

正确示例：

```md
---
name: reviewer
description: 仅在 .ai/code_review/ 下写入审查文档。
tools:
	- read
	- search
	- edit
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/code_review/"'
---
```

错误示例：

```md
---
name: reviewer
description: 仅在 .ai/code_review/ 下写入审查文档。
tools:
	- read
	- search
	- edit
---
```

影响：错误示例只能“提示模型遵守”，不能在运行时真正拦截越界编辑。

## 本项目推荐模板

### 模板 1：`workspace.instructions.md`

建议内容：

```md
---
description: "Use when working with files under .ai/: 创建、编辑、维护 .ai/dev、.ai/log、.ai/plan、.ai/bugs、.ai/kb、.ai/code_review 中的计划、日志、Bug、知识库和审查记录。"
applyTo: ".ai/**"
---

# .ai/ 工作区操作规范

## 目录结构
- `.ai/dev/` — 开发期动态规则和当前进度
- `.ai/log/` — 操作日志
- `.ai/code_review/` — 审查条目
- `.ai/bugs/` — Bug 追踪
- `.ai/plan/` — 计划体系
- `.ai/kb/` — 项目知识库

## 关键操作
- 修改 `.ai/dev/current.md` 声明任务和文件锁定
- 每次操作后同步更新 `.ai/log/` 和 `dev_last.md`
```

### 模板 2：`architect.agent.md`

建议内容：

```md
---
name: architect
description: 用于项目计划管理、协作状态维护与代码审查；可读取和搜索源码，但只应编辑 .ai/ 目录下的文档记录，不直接修改业务源码。
tools:
	- read
	- search
	- edit
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/"'
---
```

### 模板 3：`code.agent.md`

建议内容：

```md
---
name: code
description: 用于 Bug 修复、问题处理与必要的验证；不限制工具集合，默认使用当前环境中的全部可用工具能力。
---
```

### 模板 4：`reviewer.agent.md`

建议内容：

```md
---
name: reviewer
description: 用于代码审查；只读取和搜索源码，仅在 .ai/code_review/ 下写入审查文档，不直接修改业务源码。
tools:
	- read
	- search
	- edit
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/code_review/"'
---
```

### 模板 5：`copilot.code-workspace` 设置

建议内容：

```json
{
	"folders": [
		{
			"path": "."
		}
	],
	"settings": {
		"chat.includeApplyingInstructions": true,
		"chat.useAgentsMdFile": true,
		"chat.useCustomAgentHooks": true
	}
}
```

### 模板 6：`restrict-edit-scope` hook 的接入方式

适用场景：已有 `.github/scripts/restrict-edit-scope.ps1`，只需要在不同 Agent 上切换允许目录前缀。

Architect：

```yaml
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/"'
```

Reviewer：

```yaml
hooks:
	PreToolUse:
		- type: command
			windows: 'powershell -NoProfile -ExecutionPolicy Bypass -File .github\scripts\restrict-edit-scope.ps1 -AllowedPrefix ".ai/code_review/"'
```

## 验证与排查

### 验证清单

1. 在 Chat Customizations Diagnostics 中确认 `instructions`、`agents`、`hooks` 均被加载。
2. 在处理 `.ai` 目录任务时，确认 References 中能看到 `workspace.instructions.md`。
3. 选中 `architect` 或 `reviewer` 后，尝试编辑非允许目录文件，确认 Hook 返回 `deny` 或 `ask`。
4. 选中 `code` Agent 后，确认仍可正常执行读、搜、改、命令验证流程。
5. 新增配置文件时，优先对照本指南检查 `description`、`tools`、`hooks` 和 workspace settings。

### 常见误区

- 把所有规范都塞进全局约束，导致上下文臃肿
- 为了一个简单规则创建 Skill 或 Agent，过度设计
- `description` 写得过于抽象，导致无法被正确发现
- 把 `applyTo` 写得过宽，导致无关任务也加载大段说明
- Skill 的 `name` 与目录名不一致，或 frontmatter 语法错误
- Agent 给了过多工具，角色边界失效
- 以为写了 `edit` 就自动具备目录级限制，实际仍需 Hook
- 以为手工枚举更多工具就等于“全部权限”，实际恰恰可能把 Agent 限制住

## 后续维护建议

- 后续继续完善 Copilot 配置时，以本文件为唯一维护入口
- 若新增固定研发流程，例如“代码评审”“发布检查”“接口变更验证”，优先判断是否应沉淀为 Skill
- 若后续要做多 Agent 协作，再为明确角色创建新的 `.github/agents/*.agent.md`
- 若本文件后续继续膨胀，再按“规范 / 案例 / 模板 / FAQ”拆回多个附录；但在用户明确要求单文档期间，以本文件为准