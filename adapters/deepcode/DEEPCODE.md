# AI_Prompt × Deep Code CLI

Deep Code CLI（[lessweb/deepcode-cli](https://github.com/lessweb/deepcode-cli)）是专为 DeepSeek-V4 优化的终端 AI 编码助手。本适配器将 AI_Prompt 的治理体系部署到 Deep Code CLI 项目中。

## 与 Kilo 适配器的差异

Deep Code CLI 没有 Kilo 的 `instructions` 加载机制（无法通过 `kilo.jsonc` 加载多份 Instructions 文件）。为解决此问题，AI_Prompt 为 deepcode 提供了**合并版 AGENTS.md**，将以下内容整合为单一文件：

| 来源 | 内容 |
|------|------|
| 根 `AGENTS.md` | 核心行为约束、编码规范、注释规范 |
| `Kilo/Instructions/kilo_instructions_core.md` | .ai/ 工作区操作规范、日志规范、计划规范、审查/Bug 生命周期、知识库写入规范 |

部署时，此合并版 AGENTS.md 同时写入 `./AGENTS.md` 和 `./.deepcode/AGENTS.md`，确保 Deep Code CLI 在任何读取路径下都能获取完整的治理规则。

| 能力 | Kilo | Deep Code CLI | AI_Prompt 适配 |
|------|------|--------------|----------------|
| **AGENTS.md** | ✅ 项目根目录 + Instructions 分文件 | ✅ 项目根目录 + `.deepcode/`（合并版） | 部署合并版（含 Instructions 规范） |
| **Agent 角色** | ✅ 完整 Agent 体系 | ❌ 无 Agent 概念 | 通过 Skill 模拟关键角色 |
| **Skill 系统** | `.kilo/skills/` | `.agents/skills/` | 自动映射到正确路径 |
| **Instructions** | `kilo.jsonc` 引用多文件 | ❌ 无此概念 | 内容合并到 AGENTS.md |
| **状态机** | ✅ status.md | ❌ | 通过 `.ai/` 工作区文件系统实现 |
| **审查/Bug 追踪** | ✅ | ❌ | 通过 `.ai/` 工作区文件系统实现 |
| **自动闭环** | ✅ AutoRunner + Worker | ❌ | 不支持（需手动执行各阶段） |
| **知识库** | `.ai/kb/` | `.ai/kb/` | 共享，无差异 |

## 部署后的目录结构

```
你的项目/
├── AGENTS.md                         # AI_Prompt 核心约束（deepcode 优先读取）
├── .deepcode/
│   └── AGENTS.md                     # deepcode 项目指令（兜底）
├── .agents/
│   └── skills/                       # deepcode 项目级 Skill
│       ├── check-kb/SKILL.md         #   查阅知识库
│       ├── get-bugs/SKILL.md         #   获取待处理 Bug
│       ├── bug-acceptance/SKILL.md   #   Bug 验收流程
│       ├── get-stage-status/SKILL.md #   获取计划阶段状态
│       └── update-stage-status/SKILL.md # 更新计划阶段状态
├── .ai/                              # AI 工作区（工具无关）
│   ├── dev/
│   │   ├── dev_core.md               #   动态规则
│   │   └── current.md                #   当前进度
│   ├── log/                          #   公共日志
│   ├── plan/                         #   项目计划
│   │   ├── plan.md
│   │   └── {stage}/status.md
│   ├── kb/                           #   知识库
│   │   ├── index.md
│   │   ├── architecture.md
│   │   ├── patterns.md
│   │   ├── troubleshooting.md
│   │   └── setup.md
│   ├── code_review/                  #   代码审查
│   └── bugs/                         #   Bug 追踪
└── ~/.deepcode/
    └── settings.json                 # Deep Code CLI 用户配置（需手动设置）
```

## 安装与配置

### 1. 安装 Deep Code CLI

```bash
npm install -g @vegamo/deepcode-cli
```

### 2. 配置 Settings

创建 `~/.deepcode/settings.json`（与 VSCode 插件共享）：

```json
{
  "env": {
    "MODEL": "deepseek-v4-pro",
    "BASE_URL": "https://api.deepseek.com",
    "API_KEY": "sk-..."
  },
  "thinkingEnabled": true,
  "reasoningEffort": "max"
}
```

### 3. 部署 AI_Prompt

```bash
python deploy.py /path/to/your-project --tool deepcode
```

或在 AI 对话中：

```
请将 AI_Prompt 部署到 /path/to/your-project，使用 deepcode 适配器
```

### 4. 启动

```bash
cd /path/to/your-project
deepcode
```

在 Deep Code CLI 中使用 `/skills` 查看可用的 AI_Prompt Skill，或通过 `/` 菜单选择。

## Skill 使用说明

部署后提供 5 个 Skill，对应 AI_Prompt 的核心工作流：

| Skill | 用途 | 使用方式 |
|-------|------|----------|
| `check-kb` | 查阅 `.ai/kb/` 知识库，获取项目背景信息 | 输入 `/` 选择，或输入相关关键词自动匹配 |
| `get-bugs` | 获取 `.ai/bugs/` 中当前模块的待处理 Bug | 同上 |
| `bug-acceptance` | 按标准流程验收已修复的 Bug | 同上 |
| `get-stage-status` | 读取 `.ai/plan/{stage}/status.md` 状态 | 同上，需提供阶段名 |
| `update-stage-status` | 更新子计划状态（需提供阶段名和新状态） | 同上 |

## 人工流程使用

由于 Deep Code CLI 没有 Agent 概念，AI_Prompt 的人工流程在使用时简化为：

1. 用 `/check-kb` Skill 了解项目背景
2. 用 `/get-stage-status` Skill 查看当前计划阶段
3. 通过对话让 AI 执行编码、审查等任务（AI 会在 AGENTS.md 约束下工作）
4. 用 `/update-stage-status` Skill 推进计划状态
5. 用 `/get-bugs` + `/bug-acceptance` Skill 处理 Bug

## 限制

- **无自动闭环**：Deep Code CLI 不支持 AutoRunner + Worker 架构，所有流程需手动推进
- **无 Agent 角色隔离**：所有任务由单一 LLM 会话完成，无权限分离
- **Skill 自动匹配**：Deep Code CLI 支持根据输入自动匹配 Skill，但建议使用 `/` 菜单显式选择以保证准确

## 配置 Deep Code CLI Settings

`~/.deepcode/settings.json` 完整选项：

```json
{
  "env": {
    "MODEL": "deepseek-v4-pro",
    "BASE_URL": "https://api.deepseek.com",
    "API_KEY": "sk-..."
  },
  "thinkingEnabled": true,
  "reasoningEffort": "max",
  "debugLogEnabled": false,
  "notify": "",
  "webSearchTool": ""
}
```

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `env.MODEL` | 模型名称 | `deepseek-v4-pro` |
| `env.BASE_URL` | API 端点 | `https://api.deepseek.com` |
| `env.API_KEY` | API 密钥 | - |
| `thinkingEnabled` | 启用深度思考 | `true` |
| `reasoningEffort` | 推理强度：`min`/`low`/`medium`/`high`/`max` | `max` |
| `debugLogEnabled` | 启用调试日志 | `false` |
| `notify` | 通知脚本路径 | `""` |
| `webSearchTool` | 自定义搜索脚本路径 | `""` |
