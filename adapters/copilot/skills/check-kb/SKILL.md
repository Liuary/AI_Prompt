---
name: check-kb
description: 查阅 .ai/kb/ 项目知识库，按当前任务返回最相关的参考信息
---

# Skill: check-kb

## 输入
无（按当前任务上下文推断阅读范围）

## 执行步骤
1. 读取 `.ai/kb/index.md` 总索引
2. 根据任务特征匹配相关分类（architecture/patterns/troubleshooting/setup）
3. 提取相关条目并输出摘要

## 输出
知识库查阅结果：分类、相关条目、与当前任务的相关性
