# AI_Prompt 工作区仪表盘

> 使用 Dataview 插件动态渲染。打开此文件后页面自动刷新数据。

---

## 阶段状态概览

```dataview
TABLE WITHOUT ID
  file.link AS "阶段",
  status AS "状态",
  agent AS "当前 Agent",
  updated AS "更新时间"
FROM "plan"
WHERE file.name = "status.md"
FLATTEN regexreplace(file.folder, ".*/([^/]+)$", "$1") AS stage
SORT stage ASC
```

---

## 审查条目统计

```dataview
TABLE WITHOUT ID
  file.folder AS "阶段",
  length(filter(file.tasks, (t) => contains(t.text, "[pending]"))) AS "待处理",
  length(filter(file.tasks, (t) => contains(t.text, "[fixing]"))) AS "修复中",
  length(filter(file.tasks, (t) => contains(t.text, "[resolved]"))) AS "待验收",
  length(filter(file.tasks, (t) => contains(t.text, "[closed]"))) AS "已关闭"
FROM "users"
WHERE file.name = "REV-"
SORT file.folder ASC
```

---

## 待处理审查条目

```dataview
TASK
FROM "users"
WHERE contains(text, "[pending]") AND file.name = "REV-"
SORT file.ctime DESC
```

---

## Bug 统计（按模块）

```dataview
TABLE WITHOUT ID
  file.folder AS "模块",
  length(filter(file.tasks, (t) => contains(t.text, "[open]"))) AS "待处理",
  length(filter(file.tasks, (t) => contains(t.text, "[fixing]"))) AS "修复中",
  length(filter(file.tasks, (t) => contains(t.text, "[resolved]"))) AS "待验收",
  length(filter(file.tasks, (t) => contains(t.text, "[closed]"))) AS "已关闭"
FROM "users"
WHERE file.name = "BUG-"
SORT file.folder ASC
```

---

## 待处理 Bug

```dataview
TASK
FROM "users"
WHERE contains(text, "[open]") AND file.name = "BUG-"
SORT file.ctime DESC
```

---

## 最近日志

> 公共日志最近 30 条摘要

```dataview
TABLE WITHOUT ID
  file.link AS "日志",
  file.cday AS "日期"
FROM "log"
WHERE file.name != "index" AND file.name != "log"
SORT file.cday DESC
LIMIT 30
```

---

## 知识库索引

```dataview
TABLE WITHOUT ID
  file.link AS "知识库文件",
  file.size AS "大小"
FROM "kb"
WHERE file.name != "index"
SORT file.name ASC
```

---

## 快速链接

- [[../plan/plan|大计划]]
- [[../plan/plan_index|计划索引]]
- [[../kb/index|知识库索引]]
- [[../dev/current|当前进度]]
- [[../dev/dev_core|动态规则]]

---

> 提示：如果 Dataview 查询未显示数据，请在 Obsidian 设置中启用 Dataview 插件（Settings → Community Plugins → Dataview → Enable）。首次打开需要索引项目文件，加载时间取决于项目规模。
