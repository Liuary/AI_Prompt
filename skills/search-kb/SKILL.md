---
name: search-kb
description: 语义检索 .ai/kb/ 项目知识库。当精确匹配无结果或任务描述模糊时，通过向量相似度搜索语义相关的知识条目。
---

# 语义检索知识库

## 输入

- `query`（必需）：查询文本，描述当前任务需求、遇到的问题或想要查找的知识点。
- `top_k`（可选）：返回结果数量，默认 10。
- `min_score`（可选）：最低分数阈值，默认 0.1。分数低于此值的结果将被过滤。

## 前置条件

- 向量索引已构建（运行 `python scripts/build_kb_index.py`）
- 已安装 `sentence-transformers`（`pip install sentence-transformers`）
- 索引文件 `.ai/tmp/vectors/index.json` 存在

## 执行步骤

### 1. 检查索引就绪

确认 `.ai/tmp/vectors/index.json` 文件存在。若不存在，拒绝执行并提示先运行 `build_kb_index.py`。

### 2. 执行语义检索

执行 `python scripts/search_kb.py "<query>" --top-k <top_k> --min-score <min_score> --verbose`。

### 3. 解析结果

输出格式化的检索结果摘要：

```
🔍 语义检索结果（共 {N} 条）

  #{1} [architecture] OAuth2 登录流程设计
    文件: architecture.md | 得分: 0.87
    内容: 采用 Authorization Code Grant 流程...

  #{2} [patterns] 状态机模式使用约定
    文件: patterns.md | 得分: 0.72
    内容: 项目中所有状态流转统一使用 Switch + Enum...
```

### 4. 智能解读

结合当前任务上下文解读检索结果：
- 标注与当前任务高度相关的条目
- 标注可能需要进一步查阅的条目
- 若所有结果得分均低于 0.3，建议用户优化查询词或确认知识库覆盖范围

## 输出格式

```
## 语义检索结果

查询: "{query}"
结果数: {N}

{格式化结果列表}

### 解读
- 相关条目（得分 ≥ 0.5）: {count} 条，可直接参考
- 弱相关条目（0.3 ≤ 得分 < 0.5）: {count} 条，建议进一步确认
- 低相关条目（得分 < 0.3）: {count} 条，可能不适用
```

## 注意事项

- 向量索引是缓存层，文件系统始终是 single source of truth。若检索结果与预期不符，检查索引是否过期（运行 `--dry-run` 查看变更文件）
- 语义检索适合模糊查询和探索性搜索，精确关键词匹配优先使用 `check-kb`
- 此技能是 `check-kb` 的回退方案——当 `check-kb` 精确匹配无结果时可自动调用
