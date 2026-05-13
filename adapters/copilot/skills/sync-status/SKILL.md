---
name: sync-status
description: 聚合所有成员的任务进度视图，快速了解项目整体协作状态
---

# Skill: sync-status

## 输入
无（从 `.ai/dev/current.md` 提取）

## 执行步骤
1. 读取 `.ai/dev/current.md` 提取所有 @username 条目
2. 按状态分组（进行中 / 阻塞 / 已完成）
3. 检查文件锁定情况
4. 检测同一模块多人活跃冲突

## 输出
格式化进度摘要，按状态分组
