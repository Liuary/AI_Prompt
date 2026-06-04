# stage-08 状态 — 多模型后端解耦

- **执行模式**：auto
- **自动推进**：enabled
- **状态**：ready_for_code
- **当前责任 Agent**：auto-runner
- **上一责任 Agent**：architect
- **更新时间**：2026-06-04 12:43
- **前置依赖**：无
- **依赖状态**：satisfied

## Worktree / Session

- **工作模式**：worktree
- **分支名**：auto-stage-08
- **并行批次**：batch-2026-06-04-001
- **并行阶段**：stage-06
- **Session 名称**：-
- **合并状态**：not_started
- **清理策略**：auto

## 当前任务

将 Agent 能力描述与具体模型后端解耦，支持配置不同 LLM 后端，并提供 Hermes 本地模型部署支持。

### 任务清单

1. **模型配置层**：`.ai/config.yaml` 增加 models 节
2. **Agent 角色标准化**：创建 `.ai/agents/definitions/`，工具无关 YAML 格式
3. **Function Calling 标准格式**：写入 `specs/FUNCTION_CALL_SPEC.md`
4. **Hermes 适配器**：`adapters/hermes/`，Ollama 部署配置模板
5. **模型路由逻辑**：Agent 会话启动时按角色匹配模型
6. **部署集成**：`deploy.py --model-backend`
7. **文档与验证**：云端 API vs 本地 Hermes 对比

## 阻塞 / 暂停原因

无

## 状态记录

| 时间 | Agent | 状态变化 | 说明 |
|------|-------|----------|------|
| 2026-06-04 12:08 | architect | 创建 → planned | v3.0 阶段八计划制定 |
| 2026-06-04 12:43 | architect | planned → ready_for_code | 切换为自动模式，移交 auto-runner |