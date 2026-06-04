# Obsidian Vault — AI_Prompt 工作区

本目录包含 Obsidian 的配置和仪表盘模板。将 `.ai/` 目录在 Obsidian 中打开为 Vault，即可获得以下能力：

- **双向链接**：`[[wiki-link]]` 语法在计划、日志、审查、Bug 文件之间自由跳转
- **图谱视图**：可视化工作区文件之间的关系网络
- **Dataview 仪表盘**：通过 `dashboard.md` 动态查询阶段状态、审查条目和 Bug 列表
- **全局搜索**：跨所有 .ai/ 文件的全文本搜索

## 前置条件

1. 安装 [Obsidian](https://obsidian.md/)（桌面版）
2. 安装社区插件（推荐）：
   - **Dataview** — 动态数据查询，驱动仪表盘
   - **Obsidian Mind Map** — 计划脑图可视化
   - **Tag Wrangler** — 标签管理

## 在 Obsidian 中打开工作区

### 方法一：打开为 Vault

1. 启动 Obsidian 桌面客户端
2. 点击左下角「打开其他 Vault」→「打开文件夹作为 Vault」
3. 选择项目根目录下的 `.ai/` 文件夹
4. Obsidian 自动读取 `.ai/obsidian/.obsidian/` 中的配置，启用 wikilink、图谱等核心插件

### 方法二：从 VS Code 启动

如果已配置 `AI_Prompt.code-workspace`，可在 VS Code 内直接右键 `.ai/` 目录 → 「在 Obsidian 中打开」（需安装 obsidian-local-rest-api 插件）。

## 仪表盘使用

打开 `.ai/obsidian/dashboard.md` 后，Dataview 插件会自动渲染以下面板：

| 面板 | 说明 |
|------|------|
| 阶段状态 | 读取所有 `stage-*/status.md`，展示每个阶段的状态、责任 Agent、更新时间 |
| 审查条目 | 从私域 `code_review/` 统计 pending/fixing/resolved/closed 数量 |
| Bug 列表 | 从私域 `bugs/` 统计 open/fixing/resolved/closed 数量 |

## 配置说明

`.obsidian/obsidian.json` 已预置以下配置：

- **`newLinkFormat: "relative"`** — wikilink 使用相对路径，确保跨项目可移植
- **`useMarkdownLinks: false`** — 使用 `[[wikilink]]` 而非 `[text](url)`，保持 Obsidian 原生体验
- **核心插件**：backlink（反向链接）、graph（图谱）、outgoing-link（出链）等均已开启
- **社区插件**：dataview（仪表盘引擎）、obsidian-mind-map（脑图）、tag-wrangler（标签）

## 自定义

- 修改 `.obsidian/obsidian.json` → 在 Obsidian 中重新加载 Vault
- 修改 `dashboard.md` → 仪表盘实时更新（Dataview 自动刷新）
- 添加新的 `.md` 文件 → `[[wikilink]]` 自动建立链接
