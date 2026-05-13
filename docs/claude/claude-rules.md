# Claude Code 规则配置指南

> 记录 Claude Code 各配置文件的加载机制、正确路径及常见陷阱。

---

## [+] 配置文件加载一览 (2026-05-13)

| 组件 | 正确路径 | 自动加载 | 说明 |
|------|----------|----------|------|
| 项目指令 | `./CLAUDE.md` | ✅ 每次会话 | 根目录，最常用 |
| 项目指令（替代） | `./.claude/CLAUDE.md` | ✅ 每次会话 | 与根目录等效，二选一 |
| 本地覆盖 | `./CLAUDE.local.md` | ✅ 每次会话 | 个人覆盖，自动入 .gitignore |
| 规则文件 | `.claude/rules/*.md` | ✅ 每次会话 | 无 paths 前置元数据时无条件加载 |
| 技能文件 | `.claude/skills/<name>/SKILL.md` | ✅ 按需加载 | frontmatter 中声明 name + description |
| 全局指令 | `~/.claude/CLAUDE.md` | ✅ 每次会话 | 跨项目生效 |
| 组织策略 | `/Library/Application Support/ClaudeCode/CLAUDE.md` | ✅ 每次会话 | macOS 专用，IT 强制 |

### 不自动加载的路径（常见陷阱）

| 路径 | 是否加载 | 说明 |
|------|----------|------|
| `.claude/instructions/*.md` | ❌ 不加载 | **非官方路径**，Claude Code 不扫描此目录 |
| `.claude/rules/*.md`（有 paths 前置元数据） | ⏳ 惰性加载 | 仅当匹配文件进入上下文时加载 |
| 子目录 `sub/CLAUDE.md` | ⏳ 惰性加载 | 仅当读取该子树文件时加载 |

---

## [+] 规则文件（rules）详解

### 目录结构

```
.claude/rules/
├── core.md          # 无条件加载（无 paths 前置元数据）
├── api-conventions.md
└── frontend.md      # 惰性加载（有 paths 前置元数据）
```

### 无条件加载 vs 惰性加载

**无条件加载**（无 frontmatter paths）：
```markdown
# API 设计规范

所有 API 端点必须返回 `{ code, data, message }` 结构。
```

**惰性加载**（有 paths 前置元数据）：
```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/handlers/**/*.ts"
---

# API 实现规范

仅当处理 API 相关文件时才注入此规则。
```

### 最佳实践

- 核心约束放 `CLAUDE.md`（< 200 行）
- 专项规则拆分为 `.claude/rules/*.md`
- 大文件规则用 `paths:` 限定加载范围，节省 token
- 不要使用 `.claude/instructions/` 目录

---

## [+] 技能文件（skills）详解

### 目录结构

```
.claude/skills/
└── <skill-name>/
    └── SKILL.md      # 必须命名为 SKILL.md
```

### frontmatter 格式

```markdown
---
name: my-skill           # 必填：技能标识符（kebab-case）
description: 一句话描述   # 必填：用于技能列表展示
---

# Skill: my-skill

## 输入
...

## 执行步骤
...

## 输出
...
```

### 关键约束

- 目录名与 `name` 字段保持一致
- `name` 和 `description` 缺一不可
- 技能通过 `/skill-name` 或 Skill 工具调用
- 系统提示中的 `<skill>` 标签列出了所有已注册技能

---

## [+] CLAUDE.md 加载优先级

从高到低合并，同名字段后者不覆盖前者：

```
1. ./CLAUDE.local.md          （个人本地覆盖）
2. ./CLAUDE.md 或 .claude/CLAUDE.md  （项目级）
3. ../CLAUDE.md 向上递归       （父目录，monorepo 友好）
4. ~/.claude/CLAUDE.md         （用户全局）
5. 组织策略路径                  （IT 强制，macOS 专用）
```

所有层级的内容**拼接合并**到系统提示中。

---

## [+] 本次排查记录 (2026-05-13)

### 问题

`.claude/instructions/core.md` 中的 `.ai/` 工作区规范在会话中未生效。

### 根因

`.claude/instructions/` 不是 Claude Code 的官方自动发现路径。Claude Code 的正确路径是 `.claude/rules/`。

### 修复

```bash
mkdir -p .claude/rules
mv .claude/instructions/core.md .claude/rules/core.md
rmdir .claude/instructions
```

### 验证

- 下次会话启动时，检查系统提示是否包含 `core.md` 内容
- 或观察 Agent 是否主动执行 `.ai/` 目录初始化自检

---

## [+] 快速排错清单

遇到指令/规则/技能不生效时，按以下顺序排查：

1. 文件路径是否在官方自动发现范围（`CLAUDE.md`、`.claude/rules/`、`.claude/skills/`）
2. 技能 frontmatter 是否包含 `name` 和 `description`
3. rules 文件的 `paths:` 前置元数据是否过于狭窄导致未触发
4. 是否有 `CLAUDE.local.md` 覆盖了预期行为
5. 是否在子目录中放置了 `CLAUDE.md`（仅惰性加载）
