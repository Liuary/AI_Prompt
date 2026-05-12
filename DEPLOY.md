# 部署指令

本文件供 AI Agent 自动执行部署，也提供 `deploy.py` 脚本供用户手动一键部署。

## 自动部署（推荐）

```bash
# 部署全部工具（默认）
python deploy.py /path/to/target

# 仅部署指定工具
python deploy.py /path/to/target -k      # Kilo
python deploy.py /path/to/target -d      # Deep Code CLI

# 查看帮助和工具列表
python deploy.py --help
python deploy.py --list

# 指定模板源路径
python deploy.py /path/to/target --source /path/to/template
```

脚本自动完成所有目录创建、文件复制和配置生成。详见 `python deploy.py --help`。

---

## 支持的 AI 工具

| 工具 | 选项 | 说明 |
|------|------|------|
| **全部**（默认） | （不指定） | 同时部署 Kilo + Deep Code CLI 适配文件 |
| **Kilo** | `-k` / `--kilo` | 部署 Agent/Skill/Instructions 到 `.kilo/` 目录 |
| **Deep Code CLI** | `-d` / `--deepcode` | 部署合并版 AGENTS.md + Skill 到 `.agents/skills/` + `.deepcode/` |

各工具的详细使用说明：
- Kilo：AI_Prompt 经 `kilo.jsonc` 加载 Instructions 和 Agent
- Deep Code CLI：见 `adapters/deepcode/DEEPCODE.md`

---

## 手动部署

按步骤顺序操作，每步完成后确认成功再进入下一步。

## 环境判定

首先检查目标项目根目录是否存在 `AGENTS.md`、`kilo.jsonc` 或 `.kilo/` 目录。若三者均不存在则为**首次部署**，执行全部步骤；否则为**增量部署**，跳过已存在的文件/目录并告知用户跳过的项。

---

## 步骤 1：创建目录结构

在目标项目根目录依次执行（已存在则跳过）：

### 通用目录（所有工具）

```bash
mkdir -p .ai/dev/note
mkdir -p .ai/log
mkdir -p .ai/code_review
mkdir -p .ai/bugs
mkdir -p .ai/plan
mkdir -p .ai/kb
mkdir -p .ai/tmp
mkdir -p .ai/users
```

### Kilo 专用目录（`-k`（仅 Kilo）或不指定（全部））

```bash
mkdir -p .kilo/Instructions
mkdir -p .kilo/agents
mkdir -p .kilo/skills/bug-acceptance
mkdir -p .kilo/skills/get-bugs
mkdir -p .kilo/skills/check-kb
mkdir -p .kilo/skills/get-stage-status
mkdir -p .kilo/skills/update-stage-status
```

### Deep Code CLI 专用目录（`-d`（仅 Deep Code CLI）或不指定（全部））

```bash
mkdir -p .deepcode
mkdir -p .agents/skills/check-kb
mkdir -p .agents/skills/get-bugs
mkdir -p .agents/skills/bug-acceptance
mkdir -p .agents/skills/get-stage-status
mkdir -p .agents/skills/update-stage-status
```

---

## 步骤 2：部署通用文件

### 2.1 AGENTS.md

若目标项目已存在 `AGENTS.md` 则跳过。否则读取**当前项目**的 `AGENTS.md` 完整内容，写入目标项目根目录 `AGENTS.md`。

部署到 `.deepcode/AGENTS.md`（`-d`（仅 Deep Code CLI）或不指定（全部） 时）：将 `AGENTS.md` 内容同时写入 `.deepcode/AGENTS.md`。若已存在则跳过。

---

## 步骤 3：部署 Kilo 专用文件（`-k`（仅 Kilo）或不指定（全部））

### 3.1 kilo.jsonc

若目标项目已存在 `kilo.jsonc` 则跳过。否则创建并写入：

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

### 3.2 Instructions

源文件统一从**当前项目**路径读取。若当前项目不可用（如通过 URL 远程部署），则以 GitHub 源文件为回退：

| 源文件（当前项目） | 目标文件 | 说明 |
|---|---|---|
| `Kilo/Instructions/kilo_instructions_core.md` | `.kilo/Instructions/kilo_instructions_core.md` | .ai 工作区操作规范（公域+私域） |

每个文件的部署操作：
1. 若目标文件已存在且内容非空 → 跳过。
2. 读取源文件完整内容 → 写入目标文件。
3. 若源文件读取失败，回退读取 GitHub 原始文件：
   ```
   https://raw.githubusercontent.com/Liuary/AI_Prompt/main/{源文件路径}
   ```

### 3.3 Agent 文件

将以下 Agent 定义文件逐一从源复制到目标（已存在则跳过）：

| 源文件 | 目标文件 | 类型 |
|--------|----------|------|
| `Kilo/agents/architect.md` | `.kilo/agents/architect.md` | 主 Agent（新建 architect） |
| `Kilo/agents/auto-runner.md` | `.kilo/agents/auto-runner.md` | 子代办（单 worktree 自动闭环调度） |
| `Kilo/agents/code.md` | `.kilo/agents/code.md` | 主 Agent（覆盖内置 code） |
| `Kilo/agents/code-worker.md` | `.kilo/agents/code-worker.md` | 子代办（自动闭环编码实现） |
| `Kilo/agents/ask.md` | `.kilo/agents/ask.md` | 主 Agent（覆盖内置 ask） |
| `Kilo/agents/debug.md` | `.kilo/agents/debug.md` | 子代办（由 code 调用） |
| `Kilo/agents/review-worker.md` | `.kilo/agents/review-worker.md` | 子代办（自动闭环代码审查） |
| `Kilo/agents/tester.md` | `.kilo/agents/tester.md` | 子代办（由 code 调用） |
| `Kilo/agents/test-writer.md` | `.kilo/agents/test-writer.md` | 子代办（由 architect 调用，负责写测试） |

每个文件：读取完整内容 → 写入目标路径。YAML 头（`---` 到 `---`）必须完整保留。

### 3.4 Skill 文件（Kilo）

将以下 Skill 文件逐一从源复制到目标（已存在则跳过）：

| 源文件 | 目标文件 |
|--------|----------|
| `Kilo/skills/bug-acceptance/SKILL.md` | `.kilo/skills/bug-acceptance/SKILL.md` |
| `Kilo/skills/get-bugs/SKILL.md` | `.kilo/skills/get-bugs/SKILL.md` |
| `Kilo/skills/check-kb/SKILL.md` | `.kilo/skills/check-kb/SKILL.md` |
| `Kilo/skills/get-stage-status/SKILL.md` | `.kilo/skills/get-stage-status/SKILL.md` |
| `Kilo/skills/update-stage-status/SKILL.md` | `.kilo/skills/update-stage-status/SKILL.md` |

---

## 步骤 4：部署 Deep Code CLI 专用文件（`-d`（仅 Deep Code CLI）或不指定（全部））

### 4.1 Skill 文件（Deep Code CLI）

Skill 源文件位于 `adapters/deepcode/skills/`，目标位于 `.agents/skills/`（已存在则跳过）：

| 源文件 | 目标文件 |
|--------|----------|
| `adapters/deepcode/skills/bug-acceptance/SKILL.md` | `.agents/skills/bug-acceptance/SKILL.md` |
| `adapters/deepcode/skills/get-bugs/SKILL.md` | `.agents/skills/get-bugs/SKILL.md` |
| `adapters/deepcode/skills/check-kb/SKILL.md` | `.agents/skills/check-kb/SKILL.md` |
| `adapters/deepcode/skills/get-stage-status/SKILL.md` | `.agents/skills/get-stage-status/SKILL.md` |
| `adapters/deepcode/skills/update-stage-status/SKILL.md` | `.agents/skills/update-stage-status/SKILL.md` |

Deep Code CLI 用户还需要手动配置 `~/.deepcode/settings.json`（详见 `adapters/deepcode/DEEPCODE.md`）。

---

## 步骤 5：配置 .ai/ 工作区（所有工具通用）

### 5.1 创建用户身份文件

若 `.ai/.info.json` 不存在则创建：

```json
{
    "user": ""
}
```

Agent 在首次会话时将自动填入用户名（通过 `git config user.name` 获取）。若用户手动填入也可。

### 5.2 配置 .gitignore

检查目标项目 `.gitignore` 中是否包含以下行，缺失则追加：

```
.ai/.info.json
.ai/users/
.kilo/
```

若目标项目无 `.gitignore` 则创建并写入以上内容。

---

## 步骤 6：验证

检查以下文件是否根据部署的工具全部存在且内容非空。任何遗漏均须在报告中说明。

### 通用文件（所有工具）

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | 核心行为准则 |
| `.ai/.info.json` | 用户身份文件 |

### Kilo 专用（`-k`（仅 Kilo）或不指定（全部））

| 文件 | 说明 |
|------|------|
| `kilo.jsonc` | Kilo 配置 |
| `.kilo/Instructions/kilo_instructions_core.md` | .ai 工作区操作规范 |
| `.kilo/agents/architect.md` | Architect Agent 定义 |
| `.kilo/agents/auto-runner.md` | AutoRunner Agent 定义 |
| `.kilo/agents/code.md` | 代码 Agent 定义 |
| `.kilo/agents/code-worker.md` | CodeWorker Agent 定义 |
| `.kilo/agents/ask.md` | Ask Agent 定义 |
| `.kilo/agents/debug.md` | Debug Agent 定义 |
| `.kilo/agents/review-worker.md` | ReviewWorker Agent 定义 |
| `.kilo/agents/tester.md` | 测试 Agent 定义 |
| `.kilo/agents/test-writer.md` | 测试编写 Agent 定义 |
| `.kilo/skills/bug-acceptance/SKILL.md` | Bug 验收 Skill |
| `.kilo/skills/get-bugs/SKILL.md` | 获取 Bug Skill |
| `.kilo/skills/check-kb/SKILL.md` | 查阅知识库 Skill |
| `.kilo/skills/get-stage-status/SKILL.md` | 获取子计划状态 Skill |
| `.kilo/skills/update-stage-status/SKILL.md` | 更新子计划状态 Skill |

### Deep Code CLI 专用（`-d`（仅 Deep Code CLI）或不指定（全部））

| 文件 | 说明 |
|------|------|
| `.deepcode/AGENTS.md` | 项目级 Agent 指令（deepcode 专用） |
| `.agents/skills/check-kb/SKILL.md` | 查阅知识库 Skill |
| `.agents/skills/get-bugs/SKILL.md` | 获取 Bug Skill |
| `.agents/skills/bug-acceptance/SKILL.md` | Bug 验收 Skill |
| `.agents/skills/get-stage-status/SKILL.md` | 获取子计划状态 Skill |
| `.agents/skills/update-stage-status/SKILL.md` | 更新子计划状态 Skill |

---

## 步骤 7：报告

向用户输出部署报告：

```
部署完成。

工具：{Kilo / Deep Code CLI / Kilo + Deep Code CLI}

{每个文件的状态列表，格式如下：}
- ✅ AGENTS.md （已创建）
- ✅ .ai/.info.json （已创建）
...

共创建 X 个文件，跳过 N 个已存在文件，缺失 M 个源文件。

生效操作：
- Kilo：重启会话后 Subagent 和 Skill 生效
- Deep Code CLI：使用 /skills 查看可用 Skill
- AGENTS.md 即时生效
- .ai/ 工作区目录已就绪，Agent 首次会话时将自动初始化子文件
```
