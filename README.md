# AI_Prompt

AI_Prompt 是一个持续迭代中的 Kilo Agent 模板项目，用来把个人项目里的 AI 协作方式固定下来：哪些规则要长期遵守、计划放在哪里、Bug 和审查怎么流转、哪些经验应该进知识库、什么时候可以自动跑完整个子任务。

这个项目不是业务代码库，而是一套可部署到其他项目里的工作方式模板。它的目标不是让 AI 完全替代开发者，而是给 AI 设定清晰边界：默认保留人工控制，需要时再开启自动闭环；自动流程也只推进到子计划完成，最终合并和清理仍由人确认。

它主要解决几个常见问题：

- AI 容易改超范围、过度设计、忘记测试，所以把行为约束写进 `AGENTS.md`。
- 项目计划、日志、审查、Bug、知识沉淀容易散落各处，所以统一收进 `.ai/` 工作区。
- 调试流程、编译经验不应该塞进 AGENTS.md，所以单独拆出 `.ai/kb/` 知识库。
- 人工开发和自动闭环容易互相干扰，所以拆分主 Agent 与 Worker Agent：人工使用 `architect` / `code`，自动流程由 `auto-runner` 调度 `code-worker` / `review-worker` 等子 Agent。

## 文件结构

```
AI_Prompt/
├── AGENTS.md                    # 项目永久性行为约束 + 编码规范（跨工具通用标准）
├── kilo.jsonc                   # Kilo 配置，引用 Instructions 文件
├── deploy.py                    # 一键部署脚本
├── DEPLOY.md                    # 部署操作文档
├── README.md                    # 项目总览
├── docs/                        # 项目文档
│   └── research/                # 研究分析文档
├── Kilo/                           # 模板文件
│   ├── Instructions/
│   │   └── kilo_instructions_core.md    # .ai 工作区操作规范（公域+私域统一版）
│   ├── agents/
│   │   ├── architect.md             # Architect Agent 模板（计划管理 + 代码审查）
│   │   ├── auto-runner.md           # AutoRunner Agent 模板（单 worktree 自动闭环调度）
│   │   ├── code.md                 # 代码 Agent 模板（Bug 修复 + 审查处理）
│   │   ├── code-worker.md          # CodeWorker 子 Agent 模板（自动闭环编码实现）
│   │   ├── ask.md                  # Ask Agent 模板
│   │   ├── debug.md                # Debug Agent 模板
│   │   ├── review-worker.md        # ReviewWorker 子 Agent 模板（自动闭环代码审查）
│   │   ├── tester.md               # 测试 Subagent 模板
│   │   └── test-writer.md          # 测试编写 Subagent 模板
│   ├── skills/
│   │   ├── bug-acceptance/
│   │   │   └── SKILL.md            # Bug 验收 Skill 模板
│   │   ├── get-bugs/
│   │   │   └── SKILL.md            # 获取当前 Bug Skill 模板
│   │   ├── check-kb/
│   │   │   └── SKILL.md            # 查阅知识库 Skill 模板
│   │   ├── get-stage-status/
│   │   │   └── SKILL.md            # 获取子计划状态 Skill 模板
│   │   └── update-stage-status/
│   │       └── SKILL.md            # 更新子计划状态 Skill 模板
├── .ai/                          # AI 工作目录
│   ├── .info.json                # 用户身份（本地，不纳入版本管理）
│   ├── dev/                      # 核心规则与公共笔记
│   ├── log/                      # 公共日志（仅团队级事件）
│   ├── code_review/              # 公共代码审查（核心结论摘要）
│   ├── bugs/                     # 公共 Bug 追踪（核心结论摘要）
│   ├── plan/                     # 项目计划
│   ├── kb/                       # 知识库
│   ├── tmp/                      # 公共临时文件
│   └── users/{username}/         # 私域（本地，不纳入版本管理）
│       ├── dev_last.md           # 个人操作状态
│       ├── log/                  # 个人日志
│       ├── note/                 # 个人笔记
│       ├── code_review/          # 代码审查（按计划命名）
│       ├── bugs/                 # Bug 追踪（按模块组织）
│       └── tmp/                  # 个人临时文件
└── .gitignore
```

## 项目文档

`docs/research/` 目录存放项目相关的分析研究文档，包括竞品对比、方向探索和决策分析：

| 文档 | 说明 |
|------|------|
| `research-ai-prompt-framework.md` | AI_Prompt 框架研究：项目定位、竞品对比、差异分析、发展预测 |
| `vibe-coding-analysis.md` | Vibe Coding 现象分析 |
| `project-direction-and-significance.md` | 项目方向与意义讨论 |

## 三层约束体系

| 层级 | 文件 | 定位 | 优先级 |
|------|------|------|--------|
| 永久约束 | `AGENTS.md` | 核心行为准则 + 编码规范，跨工具通用（Kilo/Cursor/Windsurf） | 基础 |
| 流程约束 | `Kilo/Instructions/kilo_instructions_core.md` | `.ai/` 工作区操作流程 | 覆盖 AGENTS.md |
| 动态规则 | `.ai/dev/dev_core.md` | 项目运行中沉淀的具体规则，`[+]`/`[-]` 开关管理 | 高于 AGENTS.md，低于用户指令 |

## 公域与私域

.ai 目录分为**公共域**与**私域**两部分，所有用户（含单人项目）均遵循此分区：

- **公共域**：`.ai/dev/`、`.ai/log/`、`.ai/code_review/`、`.ai/bugs/`、`.ai/plan/`、`.ai/kb/`、`.ai/tmp/` — 项目级共享，纳入 Git
- **私域**：`.ai/users/{username}/` — 个人操作状态、日志、笔记、代码审查、Bug 追踪、临时文件，Git 忽略

私域中的代码审查和 Bug 追踪在完成时，将核心结论摘要写入公共日志，详细记录保留在本地。

## 人工流程

人工流程是默认模式，适合日常开发和还不稳定的项目阶段。子计划 `status.md` 默认保持：

```markdown
- **执行模式**：manual
- **自动推进**：disabled
```

在人工流程中，Agent 不会主动启动新的 Agent Manager session，只会按用户指令工作并维护 `.ai/` 记录。

典型流程：

```text
用户 → architect：制定或调整计划
用户 → code：按计划实现功能
用户 → architect：审查实现结果
用户 → code：修复审查问题
用户 → test-writer：补充测试（可选）
用户 → tester：测试、验收、提交 Bug
用户 → code：修复 Bug
用户 → tester：再次验收
```

人工流程使用主 Agent：

- `architect`：计划管理、代码审查、审查验收，不改源码
- `code`：功能实现、审查问题修复、Bug 修复
- `ask`：只读分析、知识检索、方案讨论
- `tester` / `debug` / `test-writer`：可由用户或主 Agent 按需调用

人工流程的好处是可控，适合需求还在变化、需要频繁确认或风险较高的阶段。

## 自动流程

自动流程是可选能力，用于希望让一个子计划尽量完整跑完的场景。只有当子计划 `status.md` 同时设置以下字段时才启用：

```markdown
- **执行模式**：auto
- **自动推进**：enabled
```

同时目标项目 `kilo.jsonc` 需要开启：

```jsonc
"experimental": {
  "agent_manager_tool": true
}
```

自动流程的核心设计是：**一个子计划只创建一个 AutoRunner worktree**。Architect 不会为 Code、Review、Test 分别创建多个 worktree，而是只启动一个 `auto-runner`，后续所有实现、审查、测试和 Bug 修复都在同一个 worktree 中完成。

典型流程：

```text
用户 → architect：创建子计划并开启 auto/enabled
architect → Agent Manager：启动 auto-{stage} worktree
auto-runner → code-worker：实现功能
auto-runner → review-worker：代码审查
auto-runner → code-worker：修复审查问题
auto-runner → test-writer：补充测试（如需要）
auto-runner → tester：执行测试并提交 Bug
auto-runner → code-worker：修复 Bug
auto-runner → tester：验收通过
auto-runner → status = done
用户 → Agent Manager：检查 diff，手动合并/应用/清理 worktree
```

自动流程使用 Worker Agent：

- `auto-runner`：调度者，不写源码，负责推进状态机
- `code-worker`：自动流程专用编码与修复
- `review-worker`：自动流程专用代码审查，源码只读
- `test-writer`：写测试，不做最终验收
- `tester`：测试、验收、提交 Bug
- `debug`：只读排查根因

自动流程只推进到 `done`，不会自动合并到主分支，也不会自动删除 worktree。最终仍需要用户在 Agent Manager 中检查 diff 后决定是否合并和清理。

## 部署

### 自动部署（推荐）

```bash
python deploy.py /path/to/target
```

或者让 AI 读取 DEPLOY.md ，按照规则自动部署。

### 手动部署

在目标项目中按以下步骤部署：

### 1. 核心约束与流程

| 步骤 | 操作 |
|------|------|
| 复制 `AGENTS.md` | 放置到目标项目根目录（Kilo 自动加载） |
| 创建 `kilo.jsonc` | 目标项目根目录创建，`instructions` 数组引用 Instructions 文件 |
| 复制 Instructions | `Kilo/Instructions/kilo_instructions_core.md` → 目标项目 `.kilo/Instructions/` 目录 |

目标项目 `kilo.jsonc` 示例：
```jsonc
{
  "$schema": "https://app.kilo.ai/config.json",
  "instructions": [
    ".kilo/Instructions/kilo_instructions_core.md"
  ],
  "experimental": {
    "agent_manager_tool": true
  }
}
```

### 2. Agent

将 Agent 模板文件复制到目标项目的 `.kilo/agents/` 目录，Kilo 自动发现并覆盖内置同名 Agent：

```bash
# 在目标项目根目录执行
mkdir -p .kilo/agents
cp AI_Prompt/Kilo/agents/architect.md .kilo/agents/architect.md
cp AI_Prompt/Kilo/agents/auto-runner.md .kilo/agents/auto-runner.md
cp AI_Prompt/Kilo/agents/code.md .kilo/agents/code.md
cp AI_Prompt/Kilo/agents/code-worker.md .kilo/agents/code-worker.md
cp AI_Prompt/Kilo/agents/ask.md  .kilo/agents/ask.md
cp AI_Prompt/Kilo/agents/debug.md .kilo/agents/debug.md
cp AI_Prompt/Kilo/agents/review-worker.md .kilo/agents/review-worker.md
cp AI_Prompt/Kilo/agents/tester.md .kilo/agents/tester.md
cp AI_Prompt/Kilo/agents/test-writer.md .kilo/agents/test-writer.md
```

- `architect`、`code`、`ask` 为主 Agent，覆盖 Kilo 内置同名 Agent，带有角色权限约束
- `auto-runner`、`code-worker`、`review-worker`、`debug`、`tester`、`test-writer` 为子代办 Agent。
- 人工流程使用主 `architect` / `code`；自动闭环使用 `auto-runner` 调度 `code-worker` / `review-worker`，两套职责隔离。
- 自动闭环时 Architect 只启动一个 `auto-runner` worktree，后续由 AutoRunner 在同一 worktree 内通过 `task` 串行调度其他 Agent。

### 3. Skill

将 Skill 模板文件复制到目标项目的 `.kilo/skills/` 目录，Kilo 自动发现：

```bash
mkdir -p .kilo/skills/bug-acceptance
mkdir -p .kilo/skills/get-bugs
mkdir -p .kilo/skills/check-kb
mkdir -p .kilo/skills/get-stage-status
mkdir -p .kilo/skills/update-stage-status
cp AI_Prompt/Kilo/skills/bug-acceptance/SKILL.md .kilo/skills/bug-acceptance/SKILL.md
cp AI_Prompt/Kilo/skills/get-bugs/SKILL.md .kilo/skills/get-bugs/SKILL.md
cp AI_Prompt/Kilo/skills/check-kb/SKILL.md .kilo/skills/check-kb/SKILL.md
cp AI_Prompt/Kilo/skills/get-stage-status/SKILL.md .kilo/skills/get-stage-status/SKILL.md
cp AI_Prompt/Kilo/skills/update-stage-status/SKILL.md .kilo/skills/update-stage-status/SKILL.md
```

- Skill 通过文件命名识别，Agent 使用 `load skill <name>` 或 `skill` 工具调用
- 调用示例：`load skill get-bugs` → 获取当前模块 Bug 列表
- Skill 与 Agent 无关，任何 Agent 均可按需加载

### 4. 初始化 .ai/ 目录

按需在目标项目创建 `.ai/` 子目录：`dev/note/`、`log/`、`plan/`、`kb/`、`tmp/`、`users/`。创建 `.ai/.info.json` 标识用户身份，并在 `.gitignore` 中忽略 `.ai/.info.json` 和 `.ai/users/`。

## 示例项目

- [novel_create](https://github.com/Liuary/novel_create) — 小说创作工具，使用 AI_Prompt 作为模板项目部署
