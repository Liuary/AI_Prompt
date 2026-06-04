# 知识库索引

> 渐进式查阅入口。Agent 根据任务特征读取对应分类文件获取参考信息。

## 分类概览

| 文件 | 说明 | 最后更新 |
|------|------|----------|
| `architecture.md` | 架构决策、设计理由、技术选型 | 2026-06-04 |
| `patterns.md` | 代码模式、项目约定、最佳实践 | 2026-06-04 |
| `troubleshooting.md` | 常见问题、调试流程、已知坑位 | 2026-06-04 |
| `setup.md` | 环境搭建、构建流程、依赖管理 | 2026-06-04 |

## 最近更新

| 日期 | 分类 | 条目 | 关联条目 |
|------|------|------|----------|
| 2026-06-04 | architecture | Agent 体系架构决策 | [[状态机模式约定]]、[[环境搭建#前置依赖]] |
| 2026-06-04 | architecture | Wikilink 双向链接设计 | [[状态机模式约定]]、[[知识图谱构建流程]] |
| 2026-06-04 | patterns | 状态机模式约定 | [[Agent 体系架构决策]]、[[Wikilink 双向链接设计]] |
| 2026-06-04 | patterns | Wikilink 写作模式 | [[Wikilink 双向链接设计]]、[[知识图谱构建流程]] |
| 2026-06-04 | troubleshooting | Vector 索引重建问题 | [[环境搭建#前置依赖]]、[[知识图谱构建流程]] |
| 2026-06-04 | setup | 前置依赖安装 | [[Vector 索引重建问题]]、[[Agent 体系架构决策]] |

## 知识图谱

本知识库支持基于 [[Wikilink 写作模式]] 的图谱化能力，条目之间通过 `[[条目名]]` 语法建立双向链接：

- **构建图谱**：`python scripts/build_kb_index.py --graph` — 解析所有知识条目中的 `[[wikilink]]`，生成有向图（前向引用 + 反向引用），存储于 `.ai/tmp/graph.json`
- **图谱统计**：`python scripts/build_kb_index.py --graph --stats` — 输出节点数、边数、孤立节点等信息
- **可视化导出**：`python scripts/kb_graph.py --format mermaid` — 输出 Mermaid flowchart 格式，可在支持 Mermaid 的编辑器中渲染
- **子图遍历**：`python scripts/kb_graph.py --from "条目名" --depth 2` — 从指定节点出发，遍历一度和二度关联
- **关联检索**：`search-kb` 技能在命中条目时自动遍历图谱，返回直接关联和间接关联的条目
- **设计原则**：Markdown 文件中的 `[[wikilink]]` 是 single source of truth，图谱 JSON 是索引缓存，可随时重建

## 向量化检索（可选）

本知识库支持基于语义的向量化检索能力，可与渐进式查阅配合使用：

- **构建索引**：`python scripts/build_kb_index.py` — 读取所有 `[+]` 条目生成向量索引，存储于 `.ai/tmp/vectors/`
- **语义搜索**：`python scripts/search_kb.py "查询文本"` — 语义相似度 + 精确匹配 + 时间衰减融合检索
- **技能入口**：Agent 可通过 `check-kb` 技能的自动回退机制使用语义检索（当精确匹配无结果时自动触发），或直接调用 `search-kb` 技能进行语义搜索
- **增量更新**：索引构建支持文件哈希增量更新，仅重新编码变化条目
- **依赖**：`pip install sentence-transformers`（模型：bge-small-zh-v1.5）
- **设计原则**：文件系统是 single source of truth，向量索引是加速缓存层，可随时重建
