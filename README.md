# AI_Prompt

**跨 AI 工具的 Agent 开发治理框架** — 为 AI 设定边界，让开发过程可控、可追溯、可协作。

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/Liuary/AI_Prompt)
[![Plan](https://img.shields.io/badge/plan-v2.0-blue)](.ai/plan/plan.md)

```bash
python deploy.py /path/to/your-project          # 部署全部
python deploy.py /path/to/your-project -k       # 仅 Kilo
python deploy.py /path/to/your-project -d       # 仅 Deep Code CLI
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
| **Agent 角色** | 9 个预定义角色（architect / code / tester 等），人工/自动双轨 |
| **Skill 系统** | 5 个可复用能力模块，按需调用 |

支持的 AI 工具：

| 工具 | 状态 | 部署选项 |
|------|:--:|------|
| **Kilo** | ✅ 已支持 | `-k` |
| **Deep Code CLI** | ✅ 已支持 | `-d` |
| **Claude Code** | 📋 计划中 | `-c`（v2.0） |
| **GitHub Copilot** | 📋 计划中 | `-p`（v2.0） |

---

## 解决什么问题

- **AI 容易改超范围、过度设计、忘记测试** → 把行为约束写进 `AGENTS.md`，三层约束逐级生效
- **计划、日志、审查、Bug、知识散落各处** → 统一收进 `.ai/` 工作区，结构一致
- **调试经验不该塞进行为约束** → 单独拆出 `.ai/kb/` 知识库，约束与知识分离
- **人工和自动混在一起互相干扰** → 拆分主 Agent (architect/code) 与 Worker Agent，双轨隔离

---

## 架构

```
AI_Prompt/
├── AGENTS.md                    ← 核心约束层（所有工具共用）
├── .ai/                         ← 工作区（工具无关）
│   ├── plan/   计划              │    ├── stage-01/  阶段子计划
│   ├── log/    公共日志          │    └── stage-02/  + status.md
│   ├── kb/     知识库            │
│   ├── code_review/  审查        ├── users/{name}/  私域
│   └── bugs/   Bug 追踪          │
├── deploy.py                    ← 一键部署脚本
├── Kilo/                        ← Kilo 适配器（Agent/Skill/Instructions）
└── adapters/                    ← 工具适配器
    └── deepcode/                ← Deep Code CLI 适配器
```

**核心 + 适配器**：`AGENTS.md` 和 `.ai/` 是工具无关的核心层，`Kilo/` 和 `adapters/` 将治理体系翻译为各工具的原生格式。

---

## 约束体系

三层递进约束，优先级从低到高：

| 层级 | 文件 | 说明 |
|------|------|------|
| 永久约束 | `AGENTS.md` | 6 条核心行为准则 + 编码风格，跨工具通用 |
| 流程约束 | Instructions / 合并版 AGENTS.md | .ai/ 工作区操作规范（会话自检、计划、审查、Bug 生命周期） |
| 动态规则 | `.ai/dev/dev_core.md` | `[+]`/`[-]` 开关管理，项目级定制 |

约束（怎么做事）与知识库（项目是什么样）严格分离，互不混淆。

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

默认 `执行模式=manual`，Agent 按用户指令工作，等待确认，适合需求变动和风险较高的阶段。

### 自动闭环（可选）

开启 `执行模式=auto` + `自动推进=enabled` 后，AutoRunner 在单个 worktree 内串行调度 Worker Agent：**编码 → 审查 → 修复 → 测试 → Bug 修复 → done**。自动流程只推进到子计划完成，最终合并仍由用户确认。

---

## v2.0 路线图

当前正在推进 v2.0，详见 [`.ai/plan/plan.md`](.ai/plan/plan.md)：

| 阶段 | 目标 | 状态 |
|------|------|:--:|
| 阶段一 | 规则 DSL + 编译器/校验器 + 知识库自动化 + 跨会话记忆 | `planned` |
| 阶段二 | 多人/多Agent 协作（任务归属、冲突检测、进度同步） | `planned` |
| 阶段三 | Claude Code + Copilot 适配器 + 标准化接口 | `planned` |
| 阶段四 | 规范文档体系 + 模板市场 | `planned` |

---

## 项目文档

| 文档 | 说明 |
|------|------|
| [`.ai/plan/plan.md`](.ai/plan/plan.md) | v2.0 大计划 |
| [`DEPLOY.md`](DEPLOY.md) | 完整部署操作文档 |
| [`docs/research/research-ai-prompt-framework.md`](docs/research/research-ai-prompt-framework.md) | 项目定位、竞品对比、发展预测 |
| [`docs/research/vibe-coding-analysis.md`](docs/research/vibe-coding-analysis.md) | Vibe Coding 分析 |
| [`adapters/deepcode/DEEPCODE.md`](adapters/deepcode/DEEPCODE.md) | Deep Code CLI 使用指南 |

---

## 示例项目

- [novel_create](https://github.com/Liuary/novel_create) — 小说创作工具，使用 AI_Prompt 模板部署

---

## 手动部署（参考）

自动部署推荐使用 `deploy.py`。如需手动操作，详见 [`DEPLOY.md`](DEPLOY.md) 的完整分步骤说明：

1. 复制 `AGENTS.md` 到目标项目根目录
2. 创建 `.ai/` 工作区目录结构
3. 按工具复制 Agent / Skill / Instructions 文件
4. 配置 `.gitignore` 和 `.ai/.info.json`
5. 逐项验证所有文件就位
