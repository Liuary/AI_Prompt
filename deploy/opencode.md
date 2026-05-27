# OpenCode 部署

> 代码：[deploy/opencode.py](kilo.py)  |  标志：`-k` / `--kilo`

## 部署目标

```
{target}/
├── .opencode/
│   ├── agents/           # 9 个 Agent 定义
│   ├── skills/           # 6 个 Skill
│   └── Instructions/     # 工作区操作规范
└── opencode.jsonc            # OpenCode 配置
```

## 部署文件

见 [kilo.py](kilo.py) 中的 `OPENCODE_FILES` 字典（15 个源→目标映射）。

## 配置模板

见 [kilo.py](kilo.py) 中的 `OPENCODE_JSONC_CONTENT`。

## 与 Kilo 的关系

OpenCode（anomalyco/opencode）是 Kilo 的上游开源项目。两者使用完全兼容的 Agent 格式和配置系统。
本适配器复用 Kilo 的全部 9 个 Agent 定义和 6 个 Skill，仅配置文件名和目录名不同。
