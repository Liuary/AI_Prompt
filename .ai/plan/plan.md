# 项目规划

> 制定时间：2026-05-13
> 版本：v2.0（五阶段）+ v3.0（三阶段扩展）
> 状态：stage-09 ready_for_review（v3.0 收官阶段）

## 一、项目定位

AI_Prompt 是**跨 AI 工具的 Agent 开发治理框架**，为 AI 辅助软件开发提供：一致性约束、记忆持久化、多人协作支持、多工具适配。

## 二、核心目标（按优先级排序）

| # | 目标 | 优先级 | 一句话描述 |
|---|------|--------|-----------|
| 1 | **约束与记忆持久化** | 🥇 最高 | 规则 DSL + 编译器/校验器 + 知识库自动写入 + 跨会话记忆 |
| 2 | **多人/多Agent协作** | 🥈 高 | 同一项目内多人+多AI的任务归属、冲突检测、进度同步 |
| 3 | **多Agent工具支持** | 🥉 中高 | 扩展适配器至 Claude Code + GitHub Copilot，标准化适配器接口 |
| 4 | **统一规范整理** | 🏅 持续 | 规范文档体系化、模板市场储备 |

## 三、技术架构（目标态）

```
┌─────────────────────────────────────────────────┐
│                  CLI 工具层                       │
│  deploy.py (-k/-d/-c/-p/-o)  rule compile/validate  │
├─────────────────────────────────────────────────┤
│                 适配器层                          │
│  kilo/  deepcode/  claude-code/  copilot/  opencode/│
│  ── 标准化适配器接口 (ADAPTER_SPEC.md) ──        │
├─────────────────────────────────────────────────┤
│                 核心层（工具无关）                  │
│  AGENTS.md         .ai/ 工作区                    │
│  规则 DSL (YAML)   知识库 (kb/)                   │
│  状态机 (status.md)  计划/审查/Bug 链路           │
├─────────────────────────────────────────────────┤
│                 规范层                            │
│  specs/  (OVERVIEW/WORKSPACE/AGENT_ROLES/        │
│           STATE_MACHINE/RULE_SYSTEM)             │
└─────────────────────────────────────────────────┘
```

## 四、阶段划分

### 阶段一：约束引擎 + 记忆系统

> 优先级：🥇  |  状态：review_passed  |  详见：stage-01/

- **规则 DSL**：结构化约束定义（YAML Schema），取代纯自然语言
- **规则编译器**：DSL → 各工具原生格式（AGENTS.md / CLAUDE.md / instructions.md）
- **规则校验器**：冲突检测、冗余检测、死规则检测
- **知识库自动化**：会话结束时自动将经验写入 kb/
- **跨会话记忆**：增强 dev_last.md，启动时自动恢复上下文

### 阶段二：多人协作基础

> 优先级：🥈  |  状态：review_passed  |  详见：stage-02/

- **任务归属**：current.md 格式增强，Agent 接手前声明模块
- **冲突检测**：多人/多Agent 修改同一文件前的预警
- **进度同步**：sync_status Skill，聚合所有成员任务视图
- **跨项目预留**：namespace 字段预留，不实现

### 阶段三：多工具适配扩展

> 优先级：🥉  |  状态：review_passed  |  详见：stage-03/

- **Claude Code 适配器**：CLAUDE.md + .claude/commands/
- **GitHub Copilot 适配器**：copilot-instructions.md
- **适配器接口标准化**：ADAPTER_SPEC.md，支持第三方扩展

### 阶段四：规范体系整理

> 优先级：🏅  |  状态：done  |  详见：stage-04/

- **规范文档**：specs/ 目录，5 个核心规范文档
- **模板市场储备**：打包格式设计 + 示例模板

### 阶段五：并行支持改造

> 优先级：🥈  |  状态：ready_for_review  |  详见：stage-05/

- **依赖图**：`deps.yaml` 声明阶段拓扑依赖（hard/soft/mutual_exclusion）
- **多 WorkTree 并行**：Architect 按依赖分批启动 AutoRunner
- **AutoRunner 内部并行**：审查+测试编写可并行，多 Bug 可并行修复

## 五、当前状态

已完成（基线）：
- ✅ 三层约束体系（AGENTS.md + Instructions + dev_core.md）
- ✅ .ai/ 工作区（规划/日志/审查/Bug/知识库）
- ✅ 9 Agent 角色（人工/自动双轨）+ status.md 状态机
- ✅ Kilo + Deep Code CLI 适配器
- ✅ deploy.py 多工具部署（-k/-d 标志）
- ✅ 多工具架构（核心层 + 适配器层）

### 阶段九：AI 驻留能力 / Claudian 方向（v3.0 收官）

> 优先级：🥉  |  状态：ready_for_review  |  详见：stage-09/

- **Obsidian Vault 模板**：将 .ai/ 工作区变为可视化 Vault，支持 wikilink 双向链接和图谱视图
- **Dataview 仪表盘**：动态渲染阶段状态、审查统计和 Bug 列表
- **--obsidian 部署支持**：一键部署 Obsidian 配置到目标项目
- **VS Code 工作区**：推荐插件 + 便捷任务配置
- **统一 CLI 工具**：`ai status/review/bugs/log/kb search` 命令行入口

## 六、下一步

v2.0 五阶段 + v3.0 三阶段（stage-07/08/09）全部完成。后续方向：
- 模板市场生态化
- 向量化知识库增强搜索
- 更多 AI 工具适配器（Cursor、Windsurf 等）

---
> 本计划为 大计划，更改须经团队沟通确认。各阶段的具体任务分解见对应 `stage-*/` 子目录。
