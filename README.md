# AI_Prompt

该项目是一个迭代中的AI模版项目，旨在vibe开发中对工程方向进行把控，分层的约束和稳定化AI在项目中的行为，以达到更加规范化AI项目开发的目的

## 文件结构

```
AI_Prompt/
├── AGENTS.md                    # 项目永久性行为约束 + 编码规范（跨工具通用标准）
├── kilo.jsonc                   # Kilo 配置，引用 Instructions 文件
├── Kilo/                           # 模板文件
│   ├── Instructions/                # .ai 工作区操作规范
│   │   ├── kilo_instructions_core.md       # 单人协作版
│   │   └── kilo_instructions_core_team.md  # 多人协作版
│   ├── agents/
│   │   └── tester.md               # 测试 Subagent 模板
│   ├── skills/
│   │   ├── bug-acceptance.md       # Bug 验收 Skill 模板
│   │   ├── get-bugs.md             # 获取当前 Bug Skill 模板
│   │   └── check-kb.md             # 查阅知识库 Skill 模板
│   └── rules/
│       ├── coding-agent-addon.md   # 代码 Agent 附加指令模板
│       └── plan-agent-addon.md     # Plan Agent 附加指令模板
├── .ai/                          # AI 工作目录
│   ├── dev/                      # 核心规则与开发笔记
│   ├── log/                      # 操作日志
│   ├── plan/                     # 项目计划
│   ├── reviews/                  # 代码审查（开发阶段）
│   ├── bugs/                     # Bug 追踪（测试阶段）
│   ├── kb/                       # 知识库
│   └── tmp/                      # 临时文件
└── .gitignore
```

## 三层约束体系

| 层级 | 文件 | 定位 | 优先级 |
|------|------|------|--------|
| 永久约束 | `AGENTS.md` | 核心行为准则 + 编码规范，跨工具通用（Kilo/Cursor/Windsurf） | 基础 |
| 流程约束 | `kilo.jsonc` → Instructions 文件 | `.ai/` 工作区操作流程（单人/多人可选） | 覆盖 AGENTS.md |
| 动态规则 | `.ai/dev/dev_core.md` | 项目运行中沉淀的具体规则，`[+]`/`[-]` 开关管理 | 高于 AGENTS.md，低于用户指令 |

## 核心约束

两份 Instructions 文件定义了 `.ai/` 工作区操作流程，AGENTS.md 定义永久性行为准则。共同模块包括：

- **AGENTS.md**：需求分析确认、避免过度设计、修改范围控制、多方案对比选优、测试验证、元规则冲突仲裁、编码规范
- **Instructions**：`.ai/` 目录结构、日志管理、计划管理、代码审查等操作流程

### 单人版 vs 多人版

| 特性 | 单人版 | 多人协作版 |
|------|--------|-----------|
| `.ai` 目录 | 统一共享 | 分为公共域 + 私域（`users/{username}/`） |
| 用户身份 | 无 | `.ai/.info.json` 自动识别 |
| 操作状态 | `dev/dev_last.md` | `users/{username}/dev_last.md` |
| 日志命名 | `yyyy-mm-dd-NNN.md` | `yyyy-mm-dd-{username}-NNN.md` |
| 笔记归属 | 单份 | 公共笔记 + 个人笔记分离 |

## 私域与公共域（多人协作版）

- **公共域**：`.ai/dev/`、`.ai/log/`、`.ai/plan/`、`.ai/tmp/` — 项目级共享，纳入 Git
- **私域**：`.ai/users/{username}/` — 个人状态、笔记、临时文件，Git 忽略

## 部署

在目标项目中按以下步骤部署：

### 1. 核心约束与流程

| 步骤 | 操作 |
|------|------|
| 复制 `AGENTS.md` | 放置到目标项目根目录（Kilo 自动加载） |
| 创建 `kilo.jsonc` | 目标项目根目录创建，`instructions` 数组引用 Instructions 文件 |
| 复制 Instructions | `Kilo/Instructions/kilo_instructions_core.md` → 目标项目任意位置，在 `kilo.jsonc` 中引用 |

目标项目 `kilo.jsonc` 示例：
```jsonc
{
  "instructions": [
    ".kilo/rules/core.md",              // 指向 Instructions 文件副本
    ".kilo/rules/coding-agent-addon.md"  // 代码 Agent 附加指令
  ]
}
```

### 2. Subagent

将模板文件复制到目标项目的 `.kilo/agents/` 目录，Kilo 自动发现并注册：

```bash
# 在目标项目根目录执行
mkdir -p .kilo/agents
cp AI_Prompt/Kilo/agents/tester.md .kilo/agents/tester.md
```

- 文件命名即 Agent 名称（`tester.md` → Agent 名 `tester`）
- Subagent 无需额外注册，复制后重启会话即可被代码 Agent 通过 `task` 工具调用
- 调用方式：`task("验收 BUG-{编号}", subagent_type="tester")`

### 3. Skill

将 Skill 模板文件复制到目标项目的 `.kilo/skills/` 目录，Kilo 自动发现：

```bash
mkdir -p .kilo/skills
cp AI_Prompt/Kilo/skills/bug-acceptance.md .kilo/skills/bug-acceptance.md
cp AI_Prompt/Kilo/skills/get-bugs.md .kilo/skills/get-bugs.md
cp AI_Prompt/Kilo/skills/check-kb.md .kilo/skills/check-kb.md
```

- Skill 通过文件命名识别，Agent 使用 `load skill <name>` 或 `skill` 工具调用
- 调用示例：`load skill get-bugs` → 获取当前模块 Bug 列表
- Skill 与 Agent 无关，任何 Agent 均可按需加载

### 4. 代码 Agent 附加指令

复制并在 `kilo.jsonc` 中引用：

```bash
mkdir -p .kilo/rules
cp AI_Prompt/Kilo/rules/coding-agent-addon.md .kilo/rules/coding-agent-addon.md
```

在 `kilo.jsonc` 的 `instructions` 数组中追加路径（见步骤 1 示例）。指令将在每次会话中自动加载，为代码 Agent 提供 Bug 修复和审查问题处理的标准化流程。

### 5. 初始化 .ai/ 目录

按需在目标项目创建 `.ai/` 子目录：`dev/`、`log/`、`plan/`、`reviews/`、`bugs/`、`kb/`、`tmp/`。
