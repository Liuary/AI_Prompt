---
name: get-bugs
description: 获取当前模块下状态为 open 或 fixing 的 Bug 列表
---

# Skill: get-bugs

## 输入
无（自动从 `.ai/users/{username}/bugs/index.md` 提取）

## 执行步骤
1. 读取 `.ai/users/{username}/bugs/index.md`
2. 筛选状态为 `open` 或 `fixing` 的 Bug
3. 按优先级排序输出

## 输出
格式化 Bug 列表：编号、标题、状态、优先级
