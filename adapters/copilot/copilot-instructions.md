# Copilot 项目指令

> 本文件为 GitHub Copilot 适配层。全局行为约束见根目录 `AGENTS.md`（唯一规则源头）。

## 约束来源

Copilot 同时读取 `AGENTS.md`（项目根）和本文件。所有通用约束在 AGENTS.md 中维护，本文件仅补充 Copilot 特有的配置说明。

## 可用资源

- `.github/instructions/` — 文件级规则（按文件类型/目录触发）
- `.github/skills/` — 可复用技能（按需触发）
- `.github/agents/` — 自定义 Agent（独立角色，子任务委派）
