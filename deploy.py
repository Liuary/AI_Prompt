#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI_Prompt 模板项目一键部署脚本（多工具支持）。

用法: python deploy.py <目标路径> [-k|-d|-c|-p] [--source <路径>]
      python deploy.py --help 查看完整帮助

部署逻辑已拆分到 deploy/ 包：
  deploy/__init__.py  — 命令行入口 + 工具分发
  deploy/common.py    — 通用逻辑（目录/文件/配置）
  deploy/kilo.py      — Kilo 适配器
  deploy/deepcode.py  — Deep Code CLI 适配器
  deploy/claude.py    — Claude Code 适配器
  deploy/copilot.py   — GitHub Copilot 适配器

新增工具：在 deploy/ 下创建 {tool}.py（定义 DIRS + deploy_{tool} 函数），
然后在 __init__.py 的 TOOLS 字典中注册。
"""

from deploy import main

if __name__ == "__main__":
    main()
