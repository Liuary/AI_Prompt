# OpenCode 部署

> 代码：[deploy/opencode.py](opencode.py)  |  标志：`-k` / `--kilo`（与 Kilo 共用标志，部署 OpenCode 适配内容）

## 部署目标

```
{target}/
├── .opencode/
│   ├── agents/           # 9 个 Agent 定义
│   ├── skills/           # 6 个 Skill
│   └── instructions/     # 工作区操作规范
└── opencode.jsonc            # OpenCode 配置
```

## 部署文件

见 [opencode.py](opencode.py) 中的 `OPENCODE_FILES` 字典（10 个源→目标映射）。

## 配置模板

见 [opencode.py](opencode.py) 中的 `OPENCODE_JSONC_CONTENT`。

## 与 Kilo 的关系

OpenCode（anomalyco/opencode）是 Kilo 的上游开源项目。两者使用完全兼容的 Agent 格式和配置系统。
本适配器使用 OpenCode 专用的 Agent 定义（从 Kilo 版派生，已去除不兼容的工具引用），复用 Kilo 的 6 个 Skill，仅配置文件名和目录名不同。
