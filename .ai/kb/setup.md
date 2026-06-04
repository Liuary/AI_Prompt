# 环境搭建

> 环境搭建、构建流程、依赖管理。

## [+] Python 环境配置

项目使用 Python 3.12+，推荐使用虚拟环境。部署脚本依赖标准库（argparse, json, shutil, pathlib），无需额外安装。向量化检索功能可选安装 sentence-transformers（`pip install sentence-transformers`），模型使用 bge-small-zh-v1.5。首次运行时会自动下载模型文件（约 100MB），建议在网络畅通时执行。

## [+] 部署命令速查

- 部署全部工具：`python deploy.py <目标路径>`
- 仅部署 Kilo：`python deploy.py <目标路径> -k`
- 同时部署向量化检索：`python deploy.py <目标路径> --with-vectors`
- 列出支持工具：`python deploy.py --list`
- 查看帮助：`python deploy.py --help`
