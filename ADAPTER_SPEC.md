# 适配器接口规范 (ADAPTER_SPEC.md)

> AI_Prompt 框架的多工具适配器标准化接口，供第三方扩展。

## 一、适配器定义

适配器将 AI_Prompt 的通用约束体系（AGENTS.md + Instructions + `.ai/` 工作区）转换为特定 AI 工具的原生格式。

```
                    ┌──────────────────┐
  specs/rules.yaml  │  规则编译器       │
  ─────────────────►│  rule_cli compile │──► Markdown 规则文本
                    └──────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Kilo    │   │ Claude   │   │ Copilot  │
        │ .kilo/   │   │ CLAUDE.md│   │ .github/ │
        └──────────┘   └──────────┘   └──────────┘
```

## 二、适配器必须提供的文件

| 文件 | 目标工具 | 说明 |
|------|----------|------|
| `AGENTS.md` | Kilo / 通用 | 全局行为约束（AGENTS.md 写入规范见项目 AGENTS.md） |
| `.kilo/` 目录 | Kilo | Agent / Skill / Instructions |
| `CLAUDE.md` | Claude Code | 项目级指令文件 |
| `.claude/commands/` | Claude Code | 自定义斜杠命令 |
| `.github/copilot-instructions.md` | GitHub Copilot | Copilot 自定义指令 |
| `.agents/` 目录 | Deep Code CLI | 合并版 AGENTS.md + Skills |

## 三、接口约定

### 3.1 指令文件

每个适配器必须提供一个指令文件，格式遵循目标工具规范：

| 工具 | 指令文件路径 | 格式 |
|------|-------------|------|
| Kilo | `AGENTS.md` | Markdown，`.kilo/command/*.md` 引用 |
| Claude Code | `CLAUDE.md` | Markdown |
| Copilot | `.github/copilot-instructions.md` | Markdown |
| Deep Code | `AGENTS.md` (合并版) | Markdown + Skill 引用 |

### 3.2 公共内容

指令文件应包含以下公共章节（从规则编译器输出注入）：

- **核心约束**：CORE-001~006
- **操作规范**：编码、文件管理、同步更新、冲突检测
- **编码风格**：嵌套、大括号、空值、异步
- **注释规范**：类、方法、分支、错误路径

### 3.3 工具特定内容

各适配器可追加工具特定的章节（如 Claude Code 的斜杠命令说明、Copilot 的 `.github/` 约定）。

## 四、deploy.py 集成

新增适配器时需在 `deploy.py` 中：

1. 定义 `{TOOL}_FILES` 字典（源路径 → 目标路径映射）
2. 定义 `{TOOL}_DIRS` 列表（需创建的目录）
3. 在 `argparse` 中新增互斥组标志（如 `-c` / `--claude`）
4. 在 `main()` 中添加工具分发逻辑

## 五、第三方扩展指南

1. 在 `adapters/` 下创建 `{tool_name}/` 目录
2. 实现上述 3.1 中的指令文件
3. 如需自定义命令，在工具对应目录创建命令文件
4. 更新 `deploy.py` 添加部署逻辑
5. 在 `DEPLOY.md` 中补充使用说明

## 六、已有适配器

| 适配器 | 目录 | 状态 |
|--------|------|------|
| Kilo | `Kilo/` + `AGENTS.md` | ✅ 完成 |
| Deep Code CLI | `adapters/deepcode/` | ✅ 完成 |
| Claude Code | `adapters/claude-code/` | ✅ 完成 |
| GitHub Copilot | `adapters/copilot/` | ✅ 完成 |
