# stage-10 状态 — 项目审计修复

- **执行模式**：manual
- **自动推进**：disabled
- **状态**：coding
- **当前责任 Agent**：architect
- **上一责任 Agent**：none
- **更新时间**：2026-06-05 11:14
- **前置依赖**：无
- **依赖状态**：satisfied

## Worktree / Session

- **工作模式**：manual
- **分支名**：-
- **并行批次**：-
- **并行阶段**：-
- **Session 名称**：-
- **合并状态**：not_started
- **清理策略**：manual

## 当前任务

全项目审计发现的 18 项问题，按优先级分批修复。

### P0：状态一致性（Architect 直接修复）

1. [x] 修正 `current.md` — 去掉 "v3.0全部完成" 的错误声明，逐阶段填写真实状态
2. [x] 补全 `plan_index.md` — 补上 stage-06/07/08 表行
3. [x] 更新 `plan.md` — v3.0 阶段状态从 planned 更新为实际值
4. [x] 补全 `deps.yaml` — 添加 stage-06/07/09 依赖定义
5. [x] 补全 `plan_log.md` — 补充 2026-06-04 v3.0 变更记录
6. [x] 修复 `stage-06/status.md` 和 `stage-09/status.md` 中文编码

### P1：部署同步与适配器修复（需 Code Agent）

7. [ ] 更新 `deploy/kilo.py` — 模板 KILO_JSONC_CONTENT 添加 search-kb skill
8. [ ] 补全 Hermes 适配器 — 创建 `deploy/hermes.py` + 指令文件 + 在 `deploy/__init__.py` 注册
9. [ ] 修复 `deploy/common.py` 中文注释编码损坏
10. [ ] 更新各适配器 skill 覆盖 — DeepCode 补 sync-status/search-kb，Copilot 补 get-stage-status/update-stage-status/search-kb
11. [ ] 补全 `.kilo/agents/` — 添加缺失的 4 个 Agent（auto-runner/code-worker/review-worker/test-writer）

### P2：目录与结构整理

12. [ ] 统一 `log/` 目录格式 — `2026-05-16/` 移到 `2026/05/16/`
13. [ ] 补充 `log/2026/06/04/day_index.md`
14. [ ] 清理 `output/rules.md` 加入 .gitignore
15. [ ] 清理空目录或补内容
16. [ ] `scripts/kb_graph.py` 加入 deploy 系统引用

### P3：根目录整理（需讨论）

17. [ ] 整理根目录 25 个条目 — 将 deploy.py/rule_cli.py/ADAPTER_SPEC.md 等归类
18. [ ] 明确 Kilo/agents/ 与 .kilo/agents/ 职责边界

## 阻塞 / 暂停原因

P0 由 Architect 直接处理；P1-P3 需移交 Code Agent

## 状态记录

| 时间 | Agent | 状态变化 | 说明 |
|------|-------|----------|------|
| 2026-06-05 11:14 | architect | 创建 → coding | 制定修补计划并开始 P0 |