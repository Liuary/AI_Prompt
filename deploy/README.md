# 部署模块

> AI_Prompt 框架的部署工具。代码逻辑见 `deploy.py` + `deploy/` 包。

## 文件结构

```
deploy.py              # CLI 入口（薄包装）
deploy/
├── README.md          # 本索引
├── __init__.py        # 主入口（参数解析 + 工具分发）
├── common.py          # 通用逻辑（目录/文件/配置）
├── kilo.py            # Kilo 适配器
├── deepcode.py        # Deep Code CLI 适配器
├── claude.py          # Claude Code 适配器
└── copilot.py         # GitHub Copilot 适配器
```

## 部署文档

| 工具 | 文档 | 标志 |
|------|------|------|
| 全部 | [DEPLOY.md](../DEPLOY.md) | (不指定) |
| Kilo | [kilo.md](kilo.md) | `-k` / `--kilo` |
| Deep Code CLI | [deepcode.md](deepcode.md) | `-d` / `--deepcode` |
| Claude Code | [claude.md](claude.md) | `-c` / `--claude` |
| GitHub Copilot | [copilot.md](copilot.md) | `-p` / `--copilot` |

## 新增工具指南

1. 在 `deploy/` 下创建 `{tool}.py`
   - 定义 `{TOOL}_FILES`（源→目标映射）
   - 定义 `{TOOL}_DIRS`（需创建的目录）
   - 实现 `deploy_{tool}(source, target) → list[str]`
2. 在 `__init__.py` 的 `TOOLS` 字典中注册
3. 在 `build_parser()` 中添加互斥组标志
4. 创建 `deploy/{tool}.md` 部署文档
5. 更新本 `README.md` 索引
6. 运行 `python deploy.py --list` 验证
