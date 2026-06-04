# 环境搭建

> 环境搭建、构建流程、依赖管理。

## [+] 前置依赖安装 (2026-06-04)

项目开发环境的前置依赖，包含 [[Agent 体系架构决策]] 运行所需的基础组件。

### Python 依赖

```bash
pip install sentence-transformers pyyaml
```

`sentence-transformers` 用于 [[Vector 索引重建问题]] 中的语义检索能力。模型首次运行时会自动下载 `bge-small-zh-v1.5`（约 100MB）。

### 环境变量

- `HF_ENDPOINT`：HuggingFace 镜像地址，国内环境可设为 `https://hf-mirror.com` 加速模型下载
- `PYTHONIOENCODING`：建议设为 `utf-8`，确保文件读写编码正确

### 验证安装

```bash
python -c "from sentence_transformers import SentenceTransformer; print('OK')"
python scripts/build_kb_index.py --dry-run
python scripts/build_kb_index.py --graph --stats
```

若安装失败或模型下载超时，参考 [[Vector 索引重建问题]] 中的网络配置说明。
