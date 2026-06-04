# Hermes-3 妯″瀷闆嗘垚鎸囧崡

> 灏嗘湰鍦?Hermes-3 妯″瀷锛堥€氳繃 Ollama锛夋帴鍏?AI_Prompt 椤圭洰鐨勫畬鏁存祦绋嬨€?
## 涓€銆佹灦鏋勬瑙?
AI_Prompt 鏀寔涓夌妯″瀷鍚庣锛?
```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                  Agent 灞傦紙宸ュ叿鏃犲叧锛?           鈹?鈹? .ai/agents/definitions/*.yaml                  鈹?鈹? Agent 瑙掕壊銆佹潈闄愩€佸伐鍏烽渶姹?                      鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?             妯″瀷閰嶇疆灞?(.ai/config.yaml)         鈹?鈹? models:                                        鈹?鈹?   default: { provider, model_name, ... }       鈹?鈹?   roles: { architect: {...}, code: {...} }     鈹?鈹?   agents: { code: {...} }                      鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?  OpenAI API     鈹?Anthropic API    鈹?Ollama    鈹?鈹?  (gpt-4o)       鈹?(claude-sonnet)  鈹?(hermes)  鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

## 浜屻€佸墠缃潯浠?
- [Docker](https://docs.docker.com/get-docker/) 宸插畨瑁咃紙鎴栧師鐢?Ollama锛?- GPU 椹卞姩锛堟帹鑽?NVIDIA GPU + CUDA 12+锛孋PU 妯″紡涔熷彲杩愯浣嗚緝鎱級
- 鑷冲皯 8GB RAM锛?B 妯″瀷锛夛紝16GB 鎺ㄨ崘

## 涓夈€佸揩閫熼儴缃?
### 姝ラ 1锛氬惎鍔?Ollama 瀹瑰櫒

```bash
# 鏂瑰紡 A锛欴ocker Compose锛堟帹鑽愶級
cd adapters/hermes
docker-compose up -d

# 鏂瑰紡 B锛氬師鐢?Ollama锛堝宸插畨瑁咃級
ollama serve
```

### 姝ラ 2锛氭媺鍙?Hermes-3 妯″瀷

```bash
# Docker 鐜
docker exec -it hermes-ollama ollama pull hermes-3:8b

# 鍘熺敓 Ollama
ollama pull hermes-3:8b
```

### 姝ラ 3锛氬垱寤?Ollama 鑷畾涔夋ā鍨嬶紙鎺ㄨ崘锛?
浣跨敤椤圭洰鎻愪緵鐨?Modelfile 鍒涘缓甯︾郴缁熸彁绀鸿瘝鐨勬ā鍨嬪疄渚嬶細

```bash
ollama create hermes-3 -f adapters/hermes/Modelfile
```

### 姝ラ 4锛氶獙璇佹ā鍨嬪彲鐢ㄦ€?
```bash
# 瀹夎渚濊禆
pip install requests

# 杩愯楠岃瘉鑴氭湰
python scripts/verify_hermes.py --base-url http://localhost:11434/v1 --model hermes-3:8b
```

楠岃瘉閫氳繃鍚庤緭鍑猴細
```
鉁?鍏ㄩ儴楠岃瘉閫氳繃 鈥?Hermes-3 妯″瀷鍙甯镐娇鐢?function calling銆?```

## 鍥涖€侀」鐩厤缃?
### 4.1 閮ㄧ讲鏃舵寚瀹氬悗绔?
```bash
# 閮ㄧ讲椤圭洰鏃舵寚瀹?Hermes 浣滀负鍚庣
cd /path/to/AI_Prompt && python deploy.py /path/to/my-project --model-backend ollama
```

鐢熸垚鐨?`.ai/config.yaml` 灏嗗寘鍚細
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

### 4.2 鎵嬪姩閰嶇疆锛堝凡鏈夐」鐩級

鍦?`.ai/config.yaml` 涓坊鍔狅細

```yaml
models:
  default:
    provider: ollama
    model_name: hermes-3:8b
    base_url: http://localhost:11434/v1
    api_key_env: ""
```

## 浜斻€佹ā鍨嬮厤缃鍒?
### 5.1 鍖归厤浼樺厛绾?
Agent 浼氳瘽鍚姩鏃讹紝鎸変互涓嬩紭鍏堢骇鍖归厤妯″瀷閰嶇疆锛?
1. `models.agents.{agent_id}` 鈥?Agent 瀹炰緥绾ц鐩栵紙鏈€楂橈級
2. `models.roles.{agent_id}` 鈥?瑙掕壊绾ц鐩?3. `models.default` 鈥?榛樿閰嶇疆锛堝厹搴曪級

### 5.2 鎸夎鑹插垎閰嶄笉鍚屾ā鍨?
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

浠ヤ笂閰嶇疆涓細Architect 浣跨敤 Claude锛屼唬鐮?Agent 浣跨敤鏈湴 Hermes-3锛屽叾浠?Agent 浣跨敤 GPT-4o銆?
### 5.3 鐜鍙橀噺閰嶇疆

- `OPENAI_API_KEY`锛歄penAI API 瀵嗛挜锛坧rovider=openai 鏃朵娇鐢級
- `ANTHROPIC_API_KEY`锛欰nthropic API 瀵嗛挜锛坧rovider=anthropic 鏃朵娇鐢級
- 鏈湴妯″瀷锛坥llama锛夐€氬父涓嶉渶瑕?API 瀵嗛挜锛宍api_key_env` 鐣欑┖鍗冲彲

## 鍏€丗unction Calling 鍏煎鎬?
Hermes-3 蹇呴』鏀寔浠ヤ笅 function calling 鐗规€э細

| 鐗规€?| 璇存槑 | 楠岃瘉鏂瑰紡 |
|------|------|----------|
| 宸ュ叿瀹氫箟鎺ユ敹 | 鎺ユ敹 JSON Schema 鏍煎紡鐨勫伐鍏峰垪琛?| verify_hermes.py 娴嬭瘯3 |
| tool_calls 鐢熸垚 | 鐢熸垚鏍囧噯 `tool_calls` 鏁扮粍 | verify_hermes.py 娴嬭瘯3 |
| 娴佸紡杈撳嚭 | SSE 鏍煎紡澧為噺杩斿洖 | verify_hermes.py 娴嬭瘯4 |
| finish_reason | 姝ｇ‘杩斿洖 `tool_calls` / `stop` | 娴嬭瘯3 杈撳嚭 |

璇︾粏瑙勮寖瑙?[specs/FUNCTION_CALL_SPEC.md](../specs/FUNCTION_CALL_SPEC.md)銆?
## 涓冦€丏ocker Compose 鑷畾涔?
`adapters/hermes/docker-compose.yml` 鍙嚜瀹氫箟锛?
### 鍐呭瓨/CPU 闄愬埗

```yaml
services:
  ollama:
    deploy:
      resources:
        limits:
          memory: 16G
          cpus: '4'
```

### 鑷畾涔夋ā鍨嬫寕杞?
```yaml
services:
  ollama:
    volumes:
      - ./my-models:/root/.ollama
```

### 绂佺敤 GPU锛堜粎 CPU锛?
鍒犻櫎 `deploy.resources.reservations.devices` 鍧楀嵆鍙€?
## 鍏€佹晠闅滄帓鏌?
### 妯″瀷鏈姞杞?
```
閿欒: 妯″瀷 hermes-3:8b 鏈姞杞?```

瑙ｅ喅锛?```bash
# Docker
docker exec -it hermes-ollama ollama pull hermes-3:8b
# 鍘熺敓
ollama pull hermes-3:8b
```

### API 杩炴帴澶辫触

```
閿欒: 杩炴帴澶辫触 鈥?璇风‘璁?Ollama 宸插惎鍔?```

瑙ｅ喅锛?```bash
# 妫€鏌ュ鍣ㄧ姸鎬?docker ps | grep hermes-ollama
# 妫€鏌ョ鍙?curl http://localhost:11434/api/tags
```

### Function Calling 涓嶅伐浣?
```
閿欒: 妯″瀷鏈娇鐢ㄥ伐鍏疯皟鐢紝鑰屾槸鐩存帴鍥炲鏂囨湰
```

鍙兘鍘熷洜锛?1. 妯″瀷涓嶆敮鎸?function calling 鈫?纭浣跨敤 Hermes-3 (`nousresearch/hermes3:8b`)
2. 绯荤粺鎻愮ず璇嶆湭姝ｇ‘寮曞 鈫?浣跨敤鎻愪緵鐨?Modelfile 鍒涘缓妯″瀷
3. 妯″瀷鐗堟湰杩囨棫 鈫?`ollama pull hermes-3:8b` 鏇存柊

### 鍝嶅簲杩囨參

1. 浣跨敤 GPU 鍔犻€燂細纭 `nvidia-smi` 鍙 GPU
2. 璋冩暣 `num_predict` 鍙傛暟锛圡odelfile 涓級鍑忓皬 token 涓婇檺
3. 浣跨敤鏇村皬鐨勬ā鍨嬶細`hermes-3:3b` 鏇夸唬 `8b`

## 涔濄€佺幆澧冨彉閲忓弬鑰?
| 鍙橀噺 | 璇存槑 | 绀轰緥 |
|------|------|------|
| `OLLAMA_HOST` | Ollama 鐩戝惉鍦板潃 | `0.0.0.0` |
| `OLLAMA_KEEP_ALIVE` | 妯″瀷椹荤暀鍐呭瓨鏃堕棿 | `24h` 鎴?`5m` |
| `OLLAMA_NUM_PARALLEL` | 骞惰璇锋眰鏁?| `1` |
| `OPENAI_API_KEY` | OpenAI 瀵嗛挜 | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic 瀵嗛挜 | `sk-ant-...` |
