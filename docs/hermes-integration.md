# Hermes-3 Model Integration Guide

> Complete workflow for integrating a local Hermes-3 model (via Ollama) into the AI_Prompt project.
## I. Architecture Overview
AI_Prompt supports three model backends:
```
┌─────────────────────────────────────┐
│      Agent Layer (tool-agnostic)    │
│  .ai/agents/definitions/*.yaml     │
│  Agent roles, permissions, tools   │
├─────────────────────────────────────┤
│   Model Config (.ai/config.yaml)   │
│  models:                           │
│    default: { provider, model }    │
│    roles: { architect, code... }   │
│    agents: { code: {...} }         │
├──────────┬──────────┬──────────────┤
│ OpenAI   │Anthropic │  Ollama      │
│ (gpt-4o) │(claude)  │  (hermes)    │
└──────────┴──────────┴──────────────┘
```

## II. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed (or native Ollama)
- GPU drivers (NVIDIA GPU + CUDA 12+ recommended; CPU mode works but slower)
- At least 8 GB RAM (8B model), 16 GB recommended

## III. Quick Setup
### Step 1: Start Ollama Container

```bash
# Option A: Docker Compose (recommended)
cd adapters/hermes
docker-compose up -d

# Option B: Native Ollama (if already installed)
ollama serve
```

### Step 2: Pull Hermes-3 Model

```bash
# Docker environment
docker exec -it hermes-ollama ollama pull hermes-3:8b

# Native Ollama
ollama pull hermes-3:8b
```

### Step 3: Create Custom Ollama Model (recommended)
Use the project-provided Modelfile to create a model instance with system prompts:

```bash
ollama create hermes-3 -f adapters/hermes/Modelfile
```

### Step 4: Verify Model Availability
```bash
# Install dependencies
pip install requests

# Run verification script
python scripts/verify_hermes.py --base-url http://localhost:11434/v1 --model hermes-3:8b
```

Expected output on success:
```
✓ All verifications passed — Hermes-3 model is operational with function calling.
```

## IV. Project Configuration
### 4.1 Specify Backend During Deployment
```bash
# Deploy project with Hermes as backend
cd /path/to/AI_Prompt && python deploy.py /path/to/my-project --model-backend ollama
```

The generated `.ai/config.yaml` will contain:
```yaml
models:
  default:
    provider: ollama
    model_name: hermes-3:8b
    base_url: http://localhost:11434/v1
    api_key_env: ""
  roles: {}
  agents: {}
```

### 4.2 Manual Configuration (Existing Projects)

Add the following to `.ai/config.yaml`:

```yaml
models:
  default:
    provider: ollama
    model_name: hermes-3:8b
    base_url: http://localhost:11434/v1
    api_key_env: ""
```

## V. Model Configuration Rules
### 5.1 Matching Priority
When an agent session starts, model configuration is matched by the following priority:
1. `models.agents.{agent_id}` — Agent instance-level override (highest)
2. `models.roles.{agent_id}` — Role-level override
3. `models.default` — Default configuration (fallback)

### 5.2 Role-Based Model Assignment
```yaml
models:
  default:
    provider: openai
    model_name: gpt-4o
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
  roles:
    architect:
      provider: anthropic
      model_name: claude-sonnet-4-20250514
      base_url: https://api.anthropic.com
      api_key_env: ANTHROPIC_API_KEY
    code:
      provider: ollama
      model_name: hermes-3:8b
      base_url: http://localhost:11434/v1
      api_key_env: ""
```

In the above configuration: Architect uses Claude, the Code agent uses local Hermes-3, and all other agents use GPT-4o.
### 5.3 Environment Variable Configuration

- `OPENAI_API_KEY`: OpenAI API key (used when provider=openai)
- `ANTHROPIC_API_KEY`: Anthropic API key (used when provider=anthropic)
- Local models (ollama) typically do not require an API key; leave `api_key_env` blank.

## VI. Function Calling Compatibility
Hermes-3 must support the following function calling features:

| Feature | Description | Verified By |
|------|------|----------|
| Tool Definition Reception | Accepts a JSON Schema format tool list | verify_hermes.py test 3 |
| tool_calls Generation | Generates standard `tool_calls` array | verify_hermes.py test 3 |
| Streaming Output | Returns SSE format incremental responses | verify_hermes.py test 4 |
| finish_reason | Correctly returns `tool_calls` / `stop` | test 3 output |

See [specs/FUNCTION_CALL_SPEC.md](../specs/FUNCTION_CALL_SPEC.md) for detailed specification.
## VII. Docker Compose Customization
`adapters/hermes/docker-compose.yml` can be customized:
### Memory / CPU Limits

```yaml
services:
  ollama:
    deploy:
      resources:
        limits:
          memory: 16G
          cpus: '4'
```

### Custom Model Volume Mount
```yaml
services:
  ollama:
    volumes:
      - ./my-models:/root/.ollama
```

### Disabling GPU (CPU Only)
Remove the `deploy.resources.reservations.devices` block.
## VIII. Troubleshooting
### Model Not Loaded
```
Error: model hermes-3:8b not loaded
```

Solution:
```bash
# Docker
docker exec -it hermes-ollama ollama pull hermes-3:8b
# Native
ollama pull hermes-3:8b
```

### API Connection Failed

```
Error: connection failed — please verify Ollama is running
```

Solution:
```bash
# Check container status
docker ps | grep hermes-ollama
# Check endpoint
curl http://localhost:11434/api/tags
```

### Function Calling Not Working
```
Error: model did not use tool call, but replied with plain text
```

Possible causes:
1. Model does not support function calling → Confirm using Hermes-3 (`nousresearch/hermes3:8b`)
2. System prompt not correctly guiding the model → Use the provided Modelfile to create the model
3. Model version is outdated → `ollama pull hermes-3:8b` to update

### Response Too Slow

1. Use GPU acceleration: verify GPU is visible via `nvidia-smi`
2. Adjust `num_predict` parameter (in Modelfile) to reduce token limit
3. Use a smaller model: `hermes-3:3b` instead of `8b`

## IX. Environment Variable Reference
| Variable | Description | Example |
|------|------|------|
| `OLLAMA_HOST` | Ollama listen address | `0.0.0.0` |
| `OLLAMA_KEEP_ALIVE` | Model memory retention duration | `24h` or `5m` |
| `OLLAMA_NUM_PARALLEL` | Concurrent request limit | `1` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API key | `sk-ant-...` |
