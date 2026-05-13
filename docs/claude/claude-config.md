# Claude Code 团队配置操作文档

## 目标
在 Claude Code 项目中共享团队级规范、可复用技能和子代理，所有配置纳入 Git 版本控制，成员拉取即用。

## 配置层级总览

| 文件 | 是否提交 Git | 用途 |
|------|--------------|------|
| `CLAUDE.md` | ✅ 是 | 团队共享的编码约束、指令、Skill |
| `.claude/settings.json` | ✅ 是 | 项目级模型、权限、钩子设置 |
| `.claude/mcp.json` | ✅ 是 | MCP 工具服务器定义 |
| `.claude/agents/*.json` | ✅ 是 | 自定义子代理配置 |
| `.claude/settings.local.json` | ❌ 否（加入 .gitignore） | 个人 API Key、本地路径等私密信息 |

## 1. 团队约束与内置 Skill（CLAUDE.md）

**文件位置**：项目根目录下的 `CLAUDE.md`（或 `.claude/CLAUDE.md`）

该文件在每次对话启动时被自动注入，AI 会将其作为最高优先级的上下文。

### 模板内容
```markdown
# 团队开发规范与约束

## 代码风格
- 所有 Python 代码必须使用 Python 3.10+ 语法。
- 遵循 PEP 8，严格禁止使用 `eval()` 或 `exec()`。
- 提交信息必须符合 Conventional Commits 格式：`type(scope): description`。
- 禁止修改 `.env` 文件，所有环境变量变更需同步更新 `env.example`。

## 安全限制
- 永远不要执行未经用户确认的数据库迁移命令。
- 在操作生产环境数据库时，必须先备份。
- 访问外部 API 前，必须询问用户并获得明确许可。

## 文件处理约定
- 修改任何 `.py` 文件后，必须运行 `black` 和 `isort` 进行格式化。
- 新增模块后，必须更新 `README.md` 中的架构图示。

## 内置 Skill 定义
### 代码审查 (cr)
当用户请求“审查最近一次提交”时：
1. 执行 `git diff HEAD~1` 获取变更。
2. 对照 `docs/REVIEW_CHECKLIST.md` 逐项检查。
3. 只输出不符合项及改进建议，不要重复正确代码。

### 生成单元测试 (gentest)
当用户指定一个文件并要求生成单元测试时：
1. 分析目标文件的所有公共函数。
2. 使用 `pytest` 框架生成测试骨架。
3. 覆盖正常场景、边界条件和异常情况。
4. 将测试代码写入 `tests/test_<原模块名>.py`。
```

**操作步骤**：
1. 在项目根目录创建 `CLAUDE.md`，写入上述内容并按需修改。
2. 执行 `git add CLAUDE.md && git commit -m "chore: add team CLAUDE.md"`。
3. 团队成员拉取后重启 Claude Code 即可生效。

## 2. 外部 Skill（MCP 工具集成）

如果技能需要调用数据库、内部 API 或自定义脚本，通过 MCP (Model Context Protocol) 服务器实现。

**配置文件**：`.claude/mcp.json`

### 示例：集成团队 Issue 追踪工具
```json
{
  "mcpServers": {
    "team-issue-tracker": {
      "command": "npx",
      "args": ["-y", "@company/mcp-issue-tracker"],
      "env": {
        "API_KEY": "${env:ISSUE_TRACKER_KEY}"
      }
    },
    "code-linter": {
      "command": "python",
      "args": ["./scripts/mcp_linter.py"],
      "env": {}
    }
  }
}
```

**注意**：
- 敏感信息（如 API Key）不能硬编码，使用 `${env:变量名}` 引用环境变量。
- 每个成员需在自己的 `settings.local.json` 或系统环境变量中设置对应 API Key。
- 将 `mcp.json` 提交到 Git 仓库，工具对所有成员可用。

## 3. 团队 Agent（自定义子代理）

Claude Code 支持创建多个子代理，每个代理可承担特定角色（如代码审查、安全审计等），并可指定允许使用的工具。

**配置目录**：`.claude/agents/`  
每个 Agent 一个 JSON 文件，文件名即为 Agent 名称。

### 示例：创建代码审查代理
**文件**：`.claude/agents/code-reviewer.json`
```json
{
  "description": "专业代码审查代理，严格遵循团队规范",
  "systemPrompt": "你是一名资深审查员，只关注安全漏洞、性能问题和风格违规。参考 CLAUDE.md 中定义的约束。审查结果必须简洁，给出严重等级（高/中/低）。",
  "tools": ["Read", "Grep", "Glob", "Bash"],
  "model": "inherit"
}
```

**使用方式**：
在对话中输入：
```
> 请 code-reviewer 审查 app/api/ 目录下的最新变更
```

### 示例：创建 API 文档生成代理
**文件**：`.claude/agents/api-doc-bot.json`
```json
{
  "description": "根据代码自动生成 OpenAPI 文档",
  "systemPrompt": "你是一名 API 文档专家。从给定代码中提取所有端点、参数和响应，生成符合 OpenAPI 3.0 规范的 YAML 片段。",
  "tools": ["Read", "Glob", "Write"],
  "model": "inherit"
}
```

**操作步骤**：
1. 创建 `.claude/agents/` 目录。
2. 根据需要添加若干个 `.json` 文件，每个代表一个 Agent。
3. 提交到 Git 仓库：
   ```bash
   git add .claude/agents/
   git commit -m "feat: add team agents (code-reviewer, api-doc-bot)"
   ```
4. 其他成员拉取后，即可使用 `@agent名称` 调用。

## 4. 项目级 settings.json 配置

**文件位置**：`.claude/settings.json`

用于存放项目级别的通用设置，例如权限策略、钩子函数等。

### 示例：限制可执行命令并添加钩子
```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(pytest:*)",
      "Bash(black:*)",
      "Bash(git:diff)",
      "Bash(git:log)"
    ],
    "deny": ["Bash(rm:*)", "Bash(sudo:*)", "Bash(dropdb:*)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/log_writes.py"
          }
        ]
      }
    ]
  }
}
```

**关键点**：
- `permissions.deny` 中的规则全局生效且不可被本地配置放宽。
- 钩子脚本应当是项目内的版本化文件（如 `.claude/hooks/log_writes.py`），确保团队行为一致。

## 5. 成员个人配置（settings.local.json）

**文件位置**：`.claude/settings.local.json`  
**版本控制**：必须加入 `.gitignore`，**严禁提交**。

该文件仅存储个人敏感信息，如自己分发的 API Key、本地专属路径等。它与 `settings.json` 合并，但无法覆盖安全限制。

### 示例内容
```json
{
  "env": {
    "ISSUE_TRACKER_KEY": "sk-personal-xxxxxxxx",
    "LOCAL_DB_PATH": "/home/me/dev_data/"
  }
}
```

团队成员克隆仓库后，需自行创建此文件并填写个人凭证。

## 6. 快速部署清单

1. **初始化团队配置**：
   - 在项目根目录创建 `CLAUDE.md`，写入约束和 Skill。
   - 创建 `.claude/settings.json`，设置权限和钩子。
   - 创建 `.claude/agents/` 并放入 Agent 配置文件。
   - 如需外部工具，创建 `.claude/mcp.json`。
2. **加入版本控制**：
   ```bash
   git add CLAUDE.md .claude/settings.json .claude/agents/ .claude/mcp.json
   git commit -m "chore: add team Claude Code configs"
   git push
   ```
3. **成员接入**：
   - 克隆仓库。
   - 在 `.gitignore` 中确认 `.claude/settings.local.json` 已被忽略。
   - 创建 `.claude/settings.local.json`，填入个人 API Key 或路径。
   - 启动 Claude Code，所有团队配置自动生效。

## 7. 常见问题

- **问：CLAUDE.md 太长会影响性能吗？**  
  答：内容会被压缩为上下文，建议控制在 1000 行以内。过长的内容可能被截断或稀释关键指令。
- **问：如何确保 Agent 只能使用指定工具？**  
  答：在 Agent 的 JSON 中定义 `tools` 数组，仅列出允许的工具。未列出的工具该 Agent 无法调用。
- **问：如果某个成员想禁用某个团队 Skill 怎么办？**  
  答：不建议在团队共享配置中提供“禁用”选项。如有特殊需求，可在 `settings.local.json` 中通过钩子屏蔽，但安全限制无法覆盖。
