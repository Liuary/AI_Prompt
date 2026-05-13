# Claude Code 项目配置规范

> 团队级约束、规则、技能和子代理的完整配置指南。所有配置纳入 Git 版本控制，成员拉取即用。

---

## 一、配置层级总览

| 文件 | 是否提交 Git | 用途 |
|------|-------------|------|
| `CLAUDE.md` 或 `.claude/CLAUDE.md` | ✅ | 团队共享的编码约束与指令 |
| `.claude/rules/*.md` | ✅ | 专项规则文件，无条件加载或惰性加载 |
| `.claude/skills/<name>/SKILL.md` | ✅ | 可复用技能，通过 frontmatter 注册 |
| `.claude/agents/<name>.md` | ✅ | 自定义子代理，Markdown + YAML frontmatter |
| `.claude/settings.json` | ✅ | 项目级权限和钩子设置 |
| `.claude/mcp.json` | ✅ | MCP 工具服务器定义 |
| `.claude/settings.local.json` | ❌（.gitignore） | 个人 API Key、本地路径 |
| `CLAUDE.local.md` | ❌（.gitignore） | 个人指令覆盖 |

---

## 二、CLAUDE.md — 项目指令

**位置**：`./CLAUDE.md` 或 `./.claude/CLAUDE.md`（等效，二选一）

每次会话启动时自动注入。建议 < 200 行，过长会被截断。核心约束放此文件，专项规则拆分为 `.claude/rules/*.md`。

**加载优先级**（高→低，同名字段后者不覆盖前者）：
1. `./CLAUDE.local.md`（个人覆盖）
2. `./CLAUDE.md` 或 `.claude/CLAUDE.md`（项目级）
3. `../CLAUDE.md` 向上递归（monorepo 友好）
4. `~/.claude/CLAUDE.md`（用户全局）

---

## 三、Rules — 规则文件

**位置**：`.claude/rules/<name>.md`

| 类型 | 条件 | 说明 |
|------|------|------|
| 无条件加载 | 无 frontmatter 或无 `paths` 字段 | 每次会话自动注入 |
| 惰性加载 | frontmatter 含 `paths:` 字段 | 仅匹配文件进入上下文时加载 |

**示例 — 无条件加载**：
```markdown
# API 设计规范
所有 API 端点必须返回 `{ code, data, message }` 结构。
```

**示例 — 惰性加载**：
```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API 实现规范
仅当处理 API 相关文件时才注入此规则。
```

> ❌ `.claude/instructions/` 不是官方路径，Claude Code 不扫描此目录。

---

## 四、Skills — 技能文件

**位置**：`.claude/skills/<name>/SKILL.md`

必须包含 frontmatter 声明 `name` 和 `description`，目录名与 `name` 字段一致。

```markdown
---
name: my-skill
description: 一句话描述
---

# Skill: my-skill

## 输入
...

## 执行步骤
...

## 输出
...
```

技能通过 `/skill-name` 或 Skill 工具调用，启动时自动注册到系统提示的 `<skill>` 标签。

---

## 五、Agents — 自定义子代理

**位置**：`.claude/agents/<name>.md`

### 格式

Claude Code v2.0+ 使用 Markdown + YAML frontmatter（**不是 JSON**）。文件名即 Agent 名称。

```markdown
---
name: agent-name
description: 一句话描述
model: inherit
color: blue
memory: project
---

系统提示词正文，Markdown 格式。
```

### frontmatter 字段

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `name` | 是 | string | 与文件名一致（不含 `.md`） |
| `description` | 是 | string | 在 `/agents` 列表中展示 |
| `model` | 否 | string | `inherit` / `sonnet` / `opus` / `haiku` |
| `color` | 否 | string | `blue` `green` `red` `yellow` `orange` `purple` `gray` |
| `memory` | 否 | string | `user` 跨项目共享；`project` 仅当前项目 |

### systemPrompt 规范

无需在 frontmatter 中声明 `tools`，Claude Code 根据 systemPrompt 自动提供对应工具集。

必须包含：身份声明 → 核心原则 → 工作流程 → 输出格式。

### 调用方式

```
> 请 architect 审查最近一次提交
```

或在 `/agents` 界面选择 Agent 进行切换。

---

## 六、Task vs Agent — 何时用哪个

| 场景 | Task | Agent |
|------|------|-------|
| 拆分当前会话步骤 | ✅ | — |
| 跟踪多步进度 | ✅ | — |
| 独立上下文执行 | — | ✅ |
| 不同角色定位 | — | ✅ |
| 并行执行 | — | ✅ |
| ≥3 步骤有依赖 | ✅ | — |

**Task 工具**：`TaskCreate` → `TaskUpdate`（in_progress）→ `TaskUpdate`（completed）

```typescript
TaskCreate({ subject: "修复登录 Bug", description: "..." })
TaskUpdate({ taskId: "1", status: "in_progress" })
TaskUpdate({ taskId: "1", status: "completed" })
```

---

## 七、快速部署清单

1. 创建 `CLAUDE.md`（或 `.claude/CLAUDE.md`）
2. 创建 `.claude/rules/` 放入规则文件
3. 创建 `.claude/skills/` 放入技能
4. 创建 `.claude/agents/` 放入子代理（.md 格式）
5. 加入 `.gitignore`：`.claude/settings.local.json`、`CLAUDE.local.md`
6. 成员 `git pull` 后重启 Claude Code 即生效

---

## 八、排错清单

规则/技能/Agent 不生效时检查：
1. 文件路径是否在官方自动发现范围
2. 技能 frontmatter 是否含 `name` + `description`
3. Agent 是否使用 `.md` 格式（非 `.json`）
4. rules 的 `paths:` 是否过于狭窄导致未触发
5. 是否有 `CLAUDE.local.md` 覆盖了预期行为
