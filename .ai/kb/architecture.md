# 架构决策

> 项目架构设计理由、技术选型背景、设计权衡。

## [+] 多工具适配器架构

项目采用工具适配器模式，通过 `deploy/` 包实现一套模板同时支持 Kilo、Claude Code、Deep Code CLI、GitHub Copilot、OpenCode 五种 AI 工具。每个工具适配器负责将通用 Instructions 和 Skills 转换为该工具的原生目录结构和配置格式。通用逻辑（目录创建、文件拷贝、gitignore 配置等）集中在 `deploy/common.py`，各工具适配器通过 `deploy/__init__.py` 统一调度。新增工具时，只需在 `deploy/` 下创建 `{tool}.py` 并在 `TOOLS` 字典中注册即可。

## [+] 知识库文件系统优先原则

知识库 `.ai/kb/` 采用 Markdown 文件系统作为 single source of truth，向量索引存储在 `.ai/tmp/vectors/` 作为可选的语义加速缓存层。Agent 查阅知识库时应先通过 `check-kb` 技能做精确匹配，无结果时回退到 `search-kb` 做语义检索。向量索引可随时从 Markdown 文件重建，不纳入版本管理。
