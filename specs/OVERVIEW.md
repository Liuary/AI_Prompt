# AI_Prompt 规范体系概览

> 最后更新：2026-05-13

## 规范清单

| 编号 | 文件 | 说明 |
|------|------|------|
| SPEC-01 | `rules.yaml` | 规则 DSL Schema v1.0 — 9 字段 + 4 关系类型 |
| SPEC-02 | `WORKSPACE.md` | .ai/ 工作区规范 — 公域/私域结构、日志/审查/Bug 流程 |
| SPEC-03 | `AGENT_ROLES.md` | Agent 角色规范 — 9 个 Agent 的职责、权限、流转 |
| SPEC-04 | `STATE_MACHINE.md` | 状态机规范 — status.md 生命周期 |
| SPEC-05 | `RULE_SYSTEM.md` | 规则 DSL 体系 — 编译/校验/自动写入 |
| — | `AIPACK.md` | .aipack 模板打包格式设计 |

## 阅读顺序

1. **新成员**：先读 `WORKSPACE.md` 了解项目结构，再读 `AGENT_ROLES.md` 了解分工
2. **开发者**：先读 `RULE_SYSTEM.md` 和 `rules.yaml` 了解规则引擎
3. **Architect**：先读 `STATE_MACHINE.md` 了解状态流转

## 实现状态

| 规范 | 状态 | 核心产物 |
|------|------|----------|
| SPEC-01 | ✅ | `specs/rules.yaml` + `rules/rules.yaml` |
| SPEC-02 | ✅ | `Kilo/Instructions/kilo_instructions_core.md` + `AGENTS.md` |
| SPEC-03 | ✅ | `Kilo/agents/` 下 9 个 Agent 定义文件 |
| SPEC-04 | ✅ | `status.md` 状态机 + `plan/` 计划体系 |
| SPEC-05 | ✅ | `rule_cli.py` + `lib/rule_engine.py` + `tests/` |
