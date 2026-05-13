# 部署指令

> 详情见 [deploy/README.md](deploy/README.md)。部署代码已模块化拆分到 `deploy/` 包。

## 快速开始

```bash
python deploy.py /path/to/target           # 部署全部工具
python deploy.py /path/to/target -k        # 仅 Kilo
python deploy.py /path/to/target -d        # 仅 Deep Code CLI
python deploy.py /path/to/target -c        # 仅 Claude Code
python deploy.py /path/to/target -p        # 仅 GitHub Copilot
python deploy.py --help                    # 完整帮助
```

## 支持的 AI 工具

| 工具 | 标志 | 部署目标 | 详细文档 |
|------|------|----------|----------|
| **全部** | 不指定 | 四工具全部 + AGENTS.md + .ai/ 工作区 | — |
| Kilo | `-k` | `.kilo/`（agent/skill/instructions）+ `kilo.jsonc` | [deploy/kilo.md](deploy/kilo.md) |
| Deep Code CLI | `-d` | `.agents/skills/` + `.deepcode/AGENTS.md` | [deploy/deepcode.md](deploy/deepcode.md) |
| Claude Code | `-c` | `CLAUDE.md` + `.claude/commands/` | [deploy/claude.md](deploy/claude.md) |
| GitHub Copilot | `-p` | `.github/copilot-instructions.md` | [deploy/copilot.md](deploy/copilot.md) |

> AGENTS.md 为通用项，不指定工具时默认部署标准版；Deep Code CLI 使用合并版到 `.deepcode/AGENTS.md`。

## 手动部署（AI Agent）

若通过 AI Agent 部署（非 deploy.py），参见各工具的详细文档，按步骤操作。

## 代码结构

```
deploy.py              # CLI 入口（20行薄包装）
deploy/
├── __init__.py        # 参数解析 + TOOLS 注册表 + 工具分发
├── common.py          # 通用：目录创建、文件复制、gitignore、info.json
├── kilo.py            # Kilo 部署（Agent/Skill/Instructions/kilo.jsonc）
├── deepcode.py        # Deep Code CLI 部署
├── claude.py          # Claude Code 部署
└── copilot.py         # Copilot 部署
```
