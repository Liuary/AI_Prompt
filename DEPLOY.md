# 部署指令

本文件供 AI Agent 自动执行部署。请按步骤操作，完成后告知用户结果。

## 环境判定

首先确认目标项目目录结构。如果根目录不存在 `AGENTS.md`、`kilo.jsonc`、`.kilo/` 等文件，说明是首次部署，需要全量初始化。如果部分文件已存在，跳过已有步骤并告知用户已跳过的项。

## 步骤 1：核心约束与流程文件

### 1.1 创建 AGENTS.md

如果目标项目根目录不存在 `AGENTS.md`，则创建并将模板内容写入。

模板内容与当前项目的 `AGENTS.md` 相同。读取当前项目的 `AGENTS.md` 文件内容，写入目标项目的 `AGENTS.md`。

### 1.2 创建 kilo.jsonc

如果目标项目根目录不存在 `kilo.jsonc`，创建并写入：

```jsonc
{
  "instructions": [
    ".kilo/rules/kilo_instructions_core.md",
    ".kilo/rules/coding-agent-addon.md"
  ]
}
```

### 1.3 创建 .kilo/rules/ 目录

```bash
mkdir -p .kilo/rules
```

### 1.4 复制 Instructions 核心文件

读取源文件中 `Kilo/Instructions/kilo_instructions_core.md` 的完整内容，写入目标项目的 `.kilo/rules/kilo_instructions_core.md`。

### 1.5 复制代码 Agent 附加指令

读取源文件中 `Kilo/rules/coding-agent-addon.md` 的完整内容，写入目标项目的 `.kilo/rules/coding-agent-addon.md`。

源文件路径从以下任一位置查找：
- 当前项目 `Kilo/rules/coding-agent-addon.md`
- GitHub 原始文件 `https://raw.githubusercontent.com/huayinghuo/AI_Prompt/main/Kilo/rules/coding-agent-addon.md`

## 步骤 2：Subagent 部署

### 2.1 创建 agent 目录

```bash
mkdir -p .kilo/agents
```

### 2.2 部署 tester Subagent

读取源文件 `Kilo/agents/tester.md` 的完整内容，写入目标项目的 `.kilo/agents/tester.md`。

YAML 头必须完整保留（从 `---` 到 `---`），正文 Prompt 保持原样。

## 步骤 3：Skill 部署

### 3.1 创建 skill 目录

```bash
mkdir -p .kilo/skills
```

### 3.2 逐一部署 Skill 文件

将以下 Skill 文件从源复制到目标：

| 源文件 | 目标文件 |
|--------|----------|
| `Kilo/skills/bug-acceptance.md` | `.kilo/skills/bug-acceptance.md` |
| `Kilo/skills/get-bugs.md` | `.kilo/skills/get-bugs.md` |
| `Kilo/skills/check-kb.md` | `.kilo/skills/check-kb.md` |

每个文件：读取完整内容 → 写入目标路径，保持 Markdown 格式不变。

## 步骤 4：初始化 .ai/ 工作目录

在目标项目根目录创建以下子目录（如已存在则跳过）：

```bash
mkdir -p .ai/dev/note
mkdir -p .ai/log
mkdir -p .ai/plan
mkdir -p .ai/reviews
mkdir -p .ai/bugs
mkdir -p .ai/kb
mkdir -p .ai/tmp
```

## 步骤 5：验证与报告

### 5.1 验证清单

检查以下文件是否全部存在且内容非空：

- [ ] `AGENTS.md`
- [ ] `kilo.jsonc`
- [ ] `.kilo/rules/kilo_instructions_core.md`
- [ ] `.kilo/rules/coding-agent-addon.md`
- [ ] `.kilo/agents/tester.md`
- [ ] `.kilo/skills/bug-acceptance.md`
- [ ] `.kilo/skills/get-bugs.md`
- [ ] `.kilo/skills/check-kb.md`

### 5.2 报告模板

向用户输出部署报告，格式如下：

```
部署完成。共创建/更新 X 个文件，跳过 N 个已存在文件。

生效操作：
- Subagent 和 Skill 需重启 Kilo 会话后生效
- AGENTS.md 和 kilo.jsonc 即时生效
```
