# 项目规划

> 制定时间：2026-05-13
> 版本：v2.0
> 状态：done（全部 5 阶段完成）

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

## 六、下一步

阶段五（并行支持改造）进行中，改造目标：
- 支持无依赖阶段多 WorkTree 并行
- AutoRunner 内部任务级并行调度
- 依赖声明体系（deps.yaml）

---
> 本计划为 大计划，更改须经团队沟通确认。各阶段的具体任务分解见对应 `stage-*/` 子目录。

---

## 七、v3.0：环境型 Agent 治理（新增）

> 制定时间：2026-06-04
> 版本：v3.0
> 状态：planned

### v3.0 定位

v2.0 解决了"AI Agent 该怎么做事"（约束、角色、流程、状态机）。v3.0 解决"AI Agent 如何记住事、理解事、嵌入环境"——从工具型 Agent 演进为环境型 Agent。

详见研究文档：[docs/research/v3-direction-analysis.md](../docs/research/v3-direction-analysis.md)

### 核心目标

| # | 目标 | 优先级 | 一句话描述 |
|---|------|--------|-----------|
| 6 | **向量化知识库** | 🥇 最高 | `.ai/kb/` + 可选语义检索层，文件系统仍是主存储 |
| 7 | **知识图谱化记忆** | 🥈 高 | Wikilink 双向引用，Agent 沿链接图遍历相关知识 |
| 8 | **多模型后端解耦** | 🥉 中高 | Agent 能力描述与模型后端分离，支持 Hermes 本地模型 |
| 9 | **AI 驻留能力** | 🏅 持续 | Obsidian/VS Code 深度集成，AI 驻留于工作环境 |

### 核心理念延续

- 文件系统仍然是 single source of truth，向量索引/图谱索引是加速缓存
- 约束优先于赋能：新能力是为了"更高效地找到约束"
- 人工控制点不丢失：记忆检索是辅助决策，最终审批仍保留在人工流程
- 声明式优于程序式：新增配置以 YAML/Markdown 声明式文件驱动

### 阶段六：向量化知识库

> 优先级：🥇  |  状态：planned  |  详见：stage-06/

- **嵌入模型集成**：bge-small-zh-v1.5 本地嵌入，约 130MB
- **索引生成脚本**：`scripts/build_kb_index.py`，增量哈希更新
- **混合检索接口**：语义相似度 + 文件名匹配 + 时间衰减
- **search-kb Skill**：在 check-kb 精确匹配不足时回退语义检索

### 阶段七：知识图谱化记忆

> 优先级：🥈  |  状态：planned  |  详见：stage-07/

- **Wikilink 格式规范**：`[[条目名]]` 语法，Obsidian 兼容
- **自动链接生成**：Agent 写入时扫描已有条目，建议链接
- **图谱索引**：有向图构建，支持前向/后向遍历
- **图谱可视化**：Mermaid 格式导出

### 阶段八：多模型后端解耦

> 优先级：🥉  |  状态：planned  |  详见：stage-08/

- **模型配置层**：`.ai/config.yaml` 中 models 节
- **Agent 角色标准化**：工具无关的 YAML 能力描述
- **Function Calling 标准化**：对齐 OpenAI 格式
- **Hermes 适配器**：本地模型部署配置模板

### 阶段九：AI 驻留能力（Claudian 方向）

> 优先级：🏅  |  状态：planned  |  详见：stage-09/

- **Obsidian Vault 集成**：`.ai/` 目录即 Obsidian vault
- **Dataview 仪表盘**：计划状态、审查、Bug 面板
- **统一 CLI 工具**：`ai status` / `ai review` / `ai bugs` / `ai log`