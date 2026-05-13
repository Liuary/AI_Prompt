# 跨项目 Namespace 预留设计

> 优先级：低  |  状态：设计完成，暂不实现  |  详见：plan.md § 阶段二

## 背景

当前 `.ai/` 工作区为单项目设计。在多项目场景（如 monorepo）中，需要一个 `namespace` 字段来隔离不同子项目的计划、审查、Bug 记录。

## 字段设计

```json
{
  "project": "my-app",
  "namespace": "backend"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `project` | string | 项目名，默认取目录名 |
| `namespace` | string | 子项目标识，单项目为空 |

## 影响范围

若有 namespace，以下路径追加 `{namespace}/` 前缀：

```
.ai/plan/{namespace}/           → 子项目独立计划（含 status.md）
.ai/plan/{namespace}/status.md  → Skill 引用路径变更：
                                    get-stage-status / update-stage-status
                                    需适配 namespace 参数
.ai/bugs/{namespace}/           → 子项目独立 Bug
.ai/code_review/{namespace}/    → 子项目独立审查
.ai/dev/current.md              → 仍为全局（成员跨 namespace 可见）
.ai/kb/                         → 仍为全局（知识共享）
```

> **注意**：`status.md` 路径变更会影响 `.kilo/skills/` 中引用该路径的 Skill，实现时需同步更新 Skill 中的路径解析逻辑。

## 存储位置

- 写入 `.ai/.info.json`，与 `user` 字段并列
- 单项目时字段可省略

## 实现时机

当前项目为单项目，暂不实现。当以下条件满足时启动：
- 同一仓库内存在 2 个以上可独立开发的子项目
- 不同子项目有不同 Agent 团队或不同的开发周期
