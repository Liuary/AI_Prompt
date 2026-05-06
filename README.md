# AI_Prompt

该项目是一个迭代中的AI模版项目，旨在vibe开发中对工程方向进行把控，分层的约束和稳定化AI在项目中的行为，以达到更加规范化AI项目开发的目的

## 文件结构

```
AI_Prompt/
├── AGENTS.md                    # 项目永久性行为约束 + 编码规范（跨工具通用标准）
├── kilo.jsonc                   # Kilo 配置，引用 Instructions 文件
├── deploy.py                    # 一键部署脚本
├── Kilo/                           # 模板文件
│   ├── Instructions/
│   │   └── kilo_instructions_core.md    # .ai 工作区操作规范（公域+私域统一版）
│   ├── agents/
│   │   ├── plan.md                 # Plan Agent 模板
│   │   ├── ask.md                  # Ask Agent 模板
│   │   ├── debug.md                # Debug Agent 模板
│   │   └── tester.md               # 测试 Subagent 模板
│   ├── skills/
│   │   ├── bug-acceptance/
│   │   │   └── SKILL.md            # Bug 验收 Skill 模板
│   │   ├── get-bugs/
│   │   │   └── SKILL.md            # 获取当前 Bug Skill 模板
│   │   └── check-kb/
│   │       └── SKILL.md            # 查阅知识库 Skill 模板
│   └── rules/
│       ├── coding-agent-addon.md   # 代码 Agent 附加指令模板
│       └── plan-agent-addon.md     # Plan Agent 附加指令模板
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

## 三层约束体系

| 层级 | 文件 | 定位 | 优先级 |
|------|------|------|--------|
| 永久约束 | `AGENTS.md` | 核心行为准则 + 编码规范，跨工具通用（Kilo/Cursor/Windsurf） | 基础 |
| 流程约束 | `kilo.jsonc` → Instructions 文件 | `.ai/` 工作区操作流程 | 覆盖 AGENTS.md |
| 动态规则 | `.ai/dev/dev_core.md` | 项目运行中沉淀的具体规则，`[+]`/`[-]` 开关管理 | 高于 AGENTS.md，低于用户指令 |

## 公域与私域

.ai 目录分为**公共域**与**私域**两部分，所有用户（含单人项目）均遵循此分区：

- **公共域**：`.ai/dev/`、`.ai/log/`、`.ai/code_review/`、`.ai/bugs/`、`.ai/plan/`、`.ai/kb/`、`.ai/tmp/` — 项目级共享，纳入 Git
- **私域**：`.ai/users/{username}/` — 个人操作状态、日志、笔记、代码审查、Bug 追踪、临时文件，Git 忽略

私域中的代码审查和 Bug 追踪在完成时，将核心结论摘要写入公共日志，详细记录保留在本地。

## 部署

### 自动部署（推荐）

```bash
python deploy.py /path/to/target
```

### 手动部署

在目标项目中按以下步骤部署：

### 1. 核心约束与流程

| 步骤 | 操作 |
|------|------|
| 复制 `AGENTS.md` | 放置到目标项目根目录（Kilo 自动加载） |
| 创建 `kilo.jsonc` | 目标项目根目录创建，`instructions` 数组引用 `.kilo/rules/` 下的文件 |
| 复制 Instructions | `Kilo/Instructions/kilo_instructions_core.md` → 目标项目 `.kilo/rules/` 目录 |
| 复制附加指令 | `Kilo/rules/coding-agent-addon.md`、`plan-agent-addon.md` → 目标项目 `.kilo/rules/` 目录 |

目标项目 `kilo.jsonc` 示例：
```jsonc
{
  "$schema": "https://app.kilo.ai/config.json",
  "instructions": [
    ".kilo/rules/kilo_instructions_core.md",
    ".kilo/rules/coding-agent-addon.md",
    ".kilo/rules/plan-agent-addon.md"
  ]
}
```

### 2. Agent

将 Agent 模板文件复制到目标项目的 `.kilo/agents/` 目录，Kilo 自动发现并覆盖内置同名 Agent：

```bash
# 在目标项目根目录执行
mkdir -p .kilo/agents
cp AI_Prompt/Kilo/agents/plan.md .kilo/agents/plan.md
cp AI_Prompt/Kilo/agents/ask.md  .kilo/agents/ask.md
cp AI_Prompt/Kilo/agents/debug.md .kilo/agents/debug.md
cp AI_Prompt/Kilo/agents/tester.md .kilo/agents/tester.md
```

- `plan`、`ask` 为主 Agent，覆盖 Kilo 内置同名 Agent，带有角色权限约束
- `code` 保留 Kilo 内置，通过 `coding-agent-addon.md` 注入工作流指令
- `debug`、`tester` 为子代办 Agent，由主 Agent 通过 `task` 工具按需调用

### 3. Skill

将 Skill 模板文件复制到目标项目的 `.kilo/skills/` 目录，Kilo 自动发现：

```bash
mkdir -p .kilo/skills/bug-acceptance
mkdir -p .kilo/skills/get-bugs
mkdir -p .kilo/skills/check-kb
cp AI_Prompt/Kilo/skills/bug-acceptance/SKILL.md .kilo/skills/bug-acceptance/SKILL.md
cp AI_Prompt/Kilo/skills/get-bugs/SKILL.md .kilo/skills/get-bugs/SKILL.md
cp AI_Prompt/Kilo/skills/check-kb/SKILL.md .kilo/skills/check-kb/SKILL.md
```

- Skill 通过文件命名识别，Agent 使用 `load skill <name>` 或 `skill` 工具调用
- 调用示例：`load skill get-bugs` → 获取当前模块 Bug 列表
- Skill 与 Agent 无关，任何 Agent 均可按需加载

### 4. 代码 Agent 与 Plan Agent 附加指令

复制并在 `kilo.jsonc` 中引用：

```bash
mkdir -p .kilo/rules
cp AI_Prompt/Kilo/rules/coding-agent-addon.md .kilo/rules/coding-agent-addon.md
cp AI_Prompt/Kilo/rules/plan-agent-addon.md .kilo/rules/plan-agent-addon.md
```

在 `kilo.jsonc` 的 `instructions` 数组中追加路径。指令将在每次会话中自动加载，为代码 Agent 提供 Bug 修复和审查问题处理的标准化流程，为 Plan Agent 提供计划管理和审查提交验收流程。

### 5. 初始化 .ai/ 目录

按需在目标项目创建 `.ai/` 子目录：`dev/note/`、`log/`、`plan/`、`kb/`、`tmp/`、`users/`。创建 `.ai/.info.json` 标识用户身份，并在 `.gitignore` 中忽略 `.ai/.info.json` 和 `.ai/users/`。
