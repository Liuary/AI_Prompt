# Copilot 约束、Skill、自定义 Agent 处理说明

## 目的

本文用于说明本仓库中如何处理 Copilot 相关配置，避免把全局约束、文件级规则、Skill、Custom Agent 混在一起维护。

## 当前仓库现状

- 已存在根目录 AGENTS.md，用于沉淀项目级行为约束。
- 已存在 .github/copilot-instructions.md，文件头标明其由 AI_Prompt 自动生成。
- 当前仓库还没有 .github/instructions/、.github/skills/、.github/agents/ 目录。
- .ai/kb 当前为空，因此本文作为首份知识库文档写入。

## 先看结论

- 项目级、几乎每次对话都生效的规则，放在全局约束文件。
- 只对特定文件类型、目录、任务场景生效的规则，放在 .instructions.md。
- 需要“按需触发 + 携带脚本/模板/参考资料”的工作流，放在 Skill。
- 需要“独立角色 + 工具权限控制 + 可被主 Agent 委派”的能力，放在 .agent.md。
- 不要把同一套规则重复写进多个载体，避免漂移。

## 四类配置的边界

### 1. 全局约束文件

适用场景：

- 对整个仓库都成立的编码、测试、文档、协作规则。
- 需要在绝大多数任务中持续生效的要求。

常见文件：

- AGENTS.md
- .github/copilot-instructions.md

官方参考的原则：

- 通常只保留一种全局约束载体，不建议手写两份内容长期并存。
- AGENTS.md 更适合做分层约束，支持根目录和子目录继承。
- .github/copilot-instructions.md 更适合作为 Copilot 的项目级统一说明文件。

本仓库的处理原则：

- 由于 .github/copilot-instructions.md 已明确标注为“自动生成”，应优先把 AGENTS.md 视为规则源头。
- 若需要调整项目级约束，优先修改 AGENTS.md，再同步或重新生成 .github/copilot-instructions.md。
- 除非生成链路失效，不建议直接手改 .github/copilot-instructions.md。

### 2. 文件级 Instructions

适用场景：

- 只针对某一类文件或目录生效。
- 规则不会覆盖整个仓库，只在特定工作面出现。

典型例子：

- 前端组件目录的样式约定。
- 数据迁移脚本的安全要求。
- API 路由目录的错误处理规范。

建议位置：

- .github/instructions/*.instructions.md

使用要点：

- description 必须写清楚“什么时候用”。
- applyTo 只匹配必要范围，不要默认写成 **。
- 一份 instruction 只管一个主题，避免把测试、接口、样式塞进同一文件。

### 3. Skill

适用场景：

- 某类任务会重复出现，但不是每次聊天都需要。
- 除了说明文字，还需要脚本、模板、参考文档等配套资源。

建议位置：

- .github/skills/<skill-name>/SKILL.md

目录结构建议：

- SKILL.md：入口说明
- scripts/：自动化脚本
- references/：较长参考资料
- assets/：模板、样板文件

判断标准：

- 如果它更像“工作流包”，用 Skill。
- 如果只是几条简短规范，不要升级成 Skill。

编写要点：

- name 必须与文件夹名一致。
- description 里写清关键词和触发场景。
- SKILL.md 保持短小，把长文拆到 references/。
- 引用资源时使用相对路径。

### 4. 自定义 Agent

适用场景：

- 需要一个专门角色处理某类任务。
- 需要限制工具权限，避免主 Agent 拿到过多能力。
- 需要上下文隔离，作为子 Agent 被委派执行。

建议位置：

- .github/agents/*.agent.md

判断标准：

- 如果只是复用流程，不需要新人格或权限隔离，优先 Skill。
- 如果需要“谁来做”和“能用哪些工具”都单独定义，使用 Custom Agent。

编写要点：

- description 要写出清晰触发词，便于被发现和委派。
- tools 只给最小必要集合。
- 明确写出不能做什么，避免角色边界模糊。
- 一个 Agent 只负责一种角色，不做瑞士军刀。

## 选型顺序

新增 Copilot 配置时，按以下顺序判断：

1. 这条规则是不是整个仓库都需要？如果是，进入全局约束文件。
2. 这条规则是不是只针对某类文件或目录？如果是，用 .instructions.md。
3. 这件事是不是可重复执行的工作流，还需要模板或脚本？如果是，用 Skill。
4. 这件事是不是需要单独角色、权限隔离或子 Agent 调度？如果是，用 .agent.md。

## 本仓库推荐维护策略

### 全局约束

- 把 AGENTS.md 作为主维护入口。
- 把 .github/copilot-instructions.md 视为面向 Copilot 的适配层。
- 修改全局规则时，避免两边分别手工演化。

### 新增文件级规则

- 只有当规则不适合放进 AGENTS.md 时，才新增 .instructions.md。
- 每份 instruction 对应一个明确场景，不做大全文档。

### 新增 Skill

- 仅在任务具备明显复用价值时创建。
- 先写清 description，再补脚本和 references，避免“能被加载但不会被触发”。

### 新增自定义 Agent

- 只有当 Skill 不能满足上下文隔离或权限控制时才创建。
- 先约束工具和职责，再写执行步骤。

## 当前仓库需要注意的问题

- 目前同时存在 AGENTS.md 和 .github/copilot-instructions.md。
- 官方参考通常建议二选一，避免重复维护。
- 但本仓库的 .github/copilot-instructions.md 已标注为自动生成，因此可以接受“双文件存在但单一来源维护”的模式。
- 后续如果发现两者内容漂移，应优先确认 AGENTS.md 是否仍是唯一源头。

## 常见误区

- 把所有规范都塞进全局约束，导致上下文臃肿。
- 为了一个简单规则创建 Skill 或 Agent，过度设计。
- description 写得过于抽象，导致无法被正确发现。
- 把 applyTo 写得过宽，导致无关任务也加载大段说明。
- Skill 的 name 与目录名不一致，或 frontmatter 语法错误。
- Agent 给了过多工具，角色边界失效。

## 建议的后续动作

- 若准备继续完善 Copilot 配置，优先补 .github/instructions/，而不是继续扩写全局约束。
- 若存在固定研发流程，例如“代码评审”“发布检查”“接口变更验证”，可考虑逐个沉淀为 Skill。
- 若后续要做多 Agent 协作，再为明确角色创建 .github/agents/*.agent.md。