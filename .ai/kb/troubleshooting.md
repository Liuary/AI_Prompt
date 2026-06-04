# 常见问题排查

> 常见问题、调试流程、已知坑位。

## [+] Vector 索引重建问题 (2026-06-04)

当向量索引文件损坏或与知识库内容不一致时，需要重建索引。

### 症状

- `search-kb` 返回空结果但知识库中有匹配条目
- 索引文件 JSON 解析失败（`json.JSONDecodeError`）
- `--dry-run` 显示文件变更但增量索引未更新

### 解决步骤

1. 删除 `.ai/tmp/vectors/` 目录
2. 确认 [[环境搭建#前置依赖安装]] 中的 `sentence-transformers` 已正确安装
3. 运行 `python scripts/build_kb_index.py --full` 全量重建
4. 运行 `python scripts/build_kb_index.py --graph` 同步重建图谱

### 预防措施

定期运行 `dry-run` 检查索引与知识库文件的一致性。索引文件是缓存层，遵循 [[Wikilink 双向链接设计]] 中定义的设计原则：Markdown 文件是 single source of truth。

## [+] 知识图谱构建流程 (2026-06-04)

构建 [[Wikilink 双向链接设计]] 所定义的图谱索引的完整流程。

### 构建步骤

1. 确保所有 [[Wikilink 写作模式]] 中的链接引用合法（目标在 `index.md` 注册表中）
2. 运行 `python scripts/build_kb_index.py --graph` 生成 `.ai/tmp/graph.json`
3. 运行 `python scripts/build_kb_index.py --graph --stats` 检查孤立节点
4. 使用 `python scripts/kb_graph.py --format mermaid` 可视化验证

### 常见问题

- 条目未被识别为节点：检查对应文件中是否有 `[+]` 标记的条目
- 链接未生成边：检查 `[[条目名]]` 中的名称是否与 `index.md` 注册表完全一致
- 图谱为空：确认知识库中存在至少一条 `[+]` 条目
