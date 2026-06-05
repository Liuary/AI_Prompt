# Hermes (Ollama) 适配器

使用 AI_Prompt 配合本地 Hermes-3 模型（通过 Ollama 运行）。

## 快速开始

```bash
# 1. 启动 Ollama 容器
docker-compose -f adapters/hermes/docker-compose.yml up -d

# 2. 拉取并创建模型
docker exec -it hermes-ollama ollama pull hermes-3:8b
ollama create hermes-3 -f adapters/hermes/Modelfile

# 3. 验证模型可用
pip install requests
python scripts/verify_hermes.py --base-url http://localhost:11434/v1 --model hermes-3:8b

# 4. 部署项目（指定 ollama 后端）
python deploy.py /path/to/my-project --model-backend ollama
```

## 配置示例

`.ai/config.yaml` 中指定 Hermes 作为模型后端：

```yaml
models:
  default:
    provider: ollama
    model_name: hermes-3:8b
    base_url: http://localhost:11434/v1
    api_key_env: ""
```

## 详细文档

完整的集成指南、故障排查与高级配置参见 [docs/hermes-integration.md](../../docs/hermes-integration.md)。
