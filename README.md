# AI_Prompt

**跨越 AI 工具的 Agent 开发治理框架** —— 为 AI 设定边界，让开发过程可控、可追溯、可协作。

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/Liuary/AI_Prompt)
[![Plan](https://img.shields.io/badge/plan-v2.0--done-blue)](.ai/plan/plan.md)

```bash
python deploy.py /path/to/your-project          # 部署全部
python deploy.py /path/to/your-project -k       # 仅 Kilo
python deploy.py /path/to/your-project -c       # 仅 Claude Code
python deploy.py /path/to/your-project -p       # 仅 GitHub Copilot
python deploy.py /path/to/your-project -o       # 仅 OpenCode
python deploy.py --help                         # 查看帮助
```

---

## 快速开始

```bash
git clone https://github.com/Liuary/AI_Prompt.git
cd AI_Prompt
python deploy.py /path/to/your-project
```

部署后目标项目获得：

| 能力 | 说明 |
|------|------|
| **行为约束** | `AGENTS.md` 定义 AI 能做什么、不能做什么 |
| **工作区** | `.ai/` 统一管理计划、日志、审查、Bug、知识库 |
| **Agent 角色** | 多角色体系（architect / code / tester / debug），按工具适配 |
| **Skill 系统** | 7 个可复用技能模块，按需调用 |
| **Hook 保护** | Copilot 目录级编辑控制，运行时强制限制 |

## Obsidian 集成

将 `.ai/` 工作区在 Obsidian 中打开为 Vault，即可在图形化界面中管理项目：

```bash
python deploy.py /path/to/your-project --obsidian
```

部署后在 Obsidian 中打开目标项目的 `.ai/` 目录，你将获得：

| 能力 | 说明 |
|------|------|
| **双向链接** | `[[wikilink]]` 在计划、审查、Bug 文件之间自由跳转 |
| **图谱视图** | 可视化工作区文件的关联关系网络 |
| **仪表盘** | `.ai/obsidian/dashboard.md` 使用 Dataview 动态渲染阶段状态、审查条目和 Bug 列表 |
| **全局搜索** | 跨所有 .ai/ 文件的全文搜索 |

详情参见 [.ai/obsidian/README.md](.ai/obsidian/README.md)。

支持的 AI 工具：

| 工具 | 状态 | 部署选项 | 适配内容 |
|------|:--:|------|------|
| **Kilo** | ✓ | `-k` | Agent + Skill + Instructions + kilo.jsonc |
| **Claude Code** | ✓ | `-c` | CLAUDE.md + rules + skills + agents |
| **GitHub Copilot** | ✓ | `-p` | copilot-instructions + instructions + skills + agents + Hook |
| **OpenCode** | ✓ | `-o` | Agent + Skill + Instructions + opencode.jsonc |
| **Deep Code CLI** | ✓ | `-d` | Skill + 合并版 AGENTS |

---

## 解决什么问题

- **AI 容易改超范围、过度设计、忘记测试** → 约束体系： 6 条核心准则 + 编码规范 + 操作规范
- **计划、日志、审查、Bug、知识散落各处** → 统一收进 `.ai/` 工作区，结构一致
- **调试经验不该塞进行为约束** → 单独拆出 `.ai/kb/` 知识库，约束与知识分离
- **人工和自动混在一起互相干扰** → 拆分为 Agent 与 Worker Agent，双轨隔离
- **各工具配置格式不同，维护成本高** → 一键部署，按工具生成原生格式

---

## 架构

```
AI_Prompt/
├── AGENTS.md                    ← 核心约束（所有工具共用）
├── instructions/                ← 通用工作区规范
├── skills/                      ← 通用技能（7 个）
├── deploy.py → deploy/          ← 模块化部署引擎
├── .ai/                         ← 工作区框架（部署时创建）
├── adapters/
│   ├── kilo/agents/             ← Kilo Agent 定义（9 个）
│   ├── claude-code/             ← Claude Code（CLAUDE.md + agents）
│   ├── copilot/                 ← Copilot（instructions + skills + agents）
│   ├── deepcode/                ← Deep Code CLI 适配器
│   └── hermes/                  ← Hermes (Ollama) 适配器
├── scripts/                     ← CLI 工具集
├── specs/ + rules/ + lib/ + tests/  ← 规则 DSL 引擎
└── docs/                        ← 外部文档
```

**核心 + 适配器**：`AGENTS.md`、`instructions/`、`skills/` 是工具无关的核心层，`adapters/` 将治理体系翻译为各工具的原生格式。

---

## 约束体系

三层递进约束，优先级从低到高：

| 层级 | 文件 | 说明 |
|------|------|------|
| 永久约束 | `AGENTS.md` | 6 条核心行为准则 + 编码风格，跨工具通用 |
| 流程约束 | `instructions/core.md` | .ai/ 工作区操作规范（会话自检、计划、审查、Bug 生命周期） |
| 动态规则 | `.ai/dev/dev_core.md` | `[+]`/`[-]` 开关管理，项目级定制 |

约束（怎么做）与知识库（项目是什么样）严格分离，互不混淆。

---

## 工作流程

### 人工流程（默认）

```text
用户 → architect：制定计划
用户 → code：实现功能
用户 → architect：代码审查
用户 → code：修复审查问题
用户 → tester：测试、提交 Bug
用户 → code：修复 Bug → 验收通过
```

默认 `执行模式=manual`，Agent 按用户指令工作，适合需求变动和风险较高的阶段。

### 自动闭环（可选）

开启 `执行模式=auto` + `自动推进=enabled` 后，AutoRunner 在单个 worktree 内串行调度 Worker Agent：**编码 → 审查 → 修复 → 测试 → Bug 修复 → done**。自动流程只推进到子计划完成，最终合并仍由用户确认。

---

## v2.0 完成

v2.0 四个阶段全部完成，详见 [`.ai/plan/plan.md`](.ai/plan/plan.md)：

| 阶段 | 目标 | 状态 |
|------|------|:--:|
| 阶段一 | 规则 DSL + 编译器/校验器 + 知识库自动化 + 跨会话记忆 | ✓ done |
| 阶段二 | 多人/多 Agent 协作（任务归属、冲突检测、进度同步） | ✓ done |
| 阶段三 | Claude Code + Copilot 适配器 + 标准化接口 | ✓ done |
| 阶段四 | 规范文档体系 + 模板市场储备 | ✓ done |

---

## CLI 工具

```bash
python scripts/ai_cli.py status              # 所有阶段状态概览
python scripts/ai_cli.py review              # 待处理审查条目
python scripts/ai_cli.py bugs                # 待处理 Bug
python scripts/ai_cli.py log                 # 最近日志摘要
python scripts/ai_cli.py kb search <查询>     # 知识库搜索
python scripts/ai_cli.py kb list             # 知识库文件列表
```

## 项目文档

| 文档 | 说明 |
|------|------|
| [`.ai/plan/plan.md`](.ai/plan/plan.md) | v2.0 大计划 |
| [`DEPLOY.md`](DEPLOY.md) | 部署指令与工具一览 |
| [`ADAPTER_SPEC.md`](ADAPTER_SPEC.md) | 多工具适配器标准化接口 |
| [`.ai/obsidian/README.md`](.ai/obsidian/README.md) | Obsidian Vault 集成指南 |
| [`docs/claude/claude-config.md`](docs/claude/claude-config.md) | Claude Code 配置规范 |
| [`docs/github/copilot-customization-guide.md`](docs/github/copilot-customization-guide.md) | Copilot 自定义配置指南 |
| [`specs/OVERVIEW.md`](specs/OVERVIEW.md) | 规范体系概览 |

---

## 示例项目

- [novel_create](https://github.com/Liuary/novel_create) — 小说创作工具，使用 AI_Prompt 模板部署

---

## 手动部署（参考）

自动部署推荐使用 `deploy.py`。如需手动操作，详见 [`DEPLOY.md`](DEPLOY.md)：

1. 复制 `AGENTS.md` 到目标项目根目录
2. 创建 `.ai/` 工作区目录结构
3. 按工具复制指令 / 技能 / Agent 文件
4. 配置 `.gitignore` 和 `.ai/.info.json`
5. 逐项验证所有文件就位
