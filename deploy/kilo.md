# Kilo 部署

> 代码：[deploy/kilo.py](kilo.py)  |  标志：`-k` / `--kilo`

## 部署目标

```
{target}/
├── .kilo/
│   ├── agents/           # 9 个 Agent 定义
│   ├── skills/           # 6 个 Skill
│   └── Instructions/     # 工作区操作规范
└── kilo.jsonc            # Kilo 配置
```

## 部署文件

见 [kilo.py](kilo.py) 中的 `KILO_FILES` 字典（15 个源→目标映射）。

## 配置模板

见 [kilo.py](kilo.py) 中的 `KILO_JSONC_CONTENT`。
