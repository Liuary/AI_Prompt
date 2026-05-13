---
description: .ai/ 工作区操作规范。仅当读取或编辑 .ai/ 目录下文件时触发。
applyTo:
  - ".ai/**"
---

# .ai/ 工作区操作规范

## 目录结构
- `.ai/dev/` — 开发期动态规则和当前进度
- `.ai/log/` — 操作日志
- `.ai/code_review/` — 审查条目
- `.ai/bugs/` — Bug 追踪
- `.ai/plan/` — 计划体系
- `.ai/kb/` — 项目知识库
- `.ai/users/` — 成员私域（gitignore）

## 关键操作
- 修改 `.ai/dev/current.md` 声明任务和文件锁定
- 每次操作后同步更新 `.ai/log/` 和 `dev_last.md`
- 知识库写入遵循 `instructions/core.md` 中的规范
