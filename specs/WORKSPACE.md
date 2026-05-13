# .ai/ 工作区规范 (WORKSPACE.md)

> 本规范定义 `.ai/` 目录的完整结构、各子目录的职责、操作流程和约束。

## 一、设计原则

.ai 目录分为**公共域**与**私域**：
- **公共域** (`.ai/` 直接子目录)：项目级共享内容，纳入版本管理
- **私域** (`.ai/users/{username}/`)：个人操作状态，`.gitignore` 排除

## 二、目录结构

```
.ai/
├── .info.json              # 用户身份（gitignore）
├── dev/                    # 开发目录
│   ├── dev_core.md         # 动态规则（[+]/[-] 开关）
│   ├── current.md          # 当前进度（成员任务归属）
│   └── note/               # 团队共享笔记
├── log/                    # 公共日志（年/月/日分层）
├── code_review/            # 公共审查摘要
├── bugs/                   # 公共 Bug 摘要
├── plan/                   # 计划体系
│   ├── plan.md             # 大计划
│   ├── plan_index.md       # 计划索引
│   ├── plan_log.md         # 变更日志
│   └── {stage}/            # 子计划目录
│       └── status.md       # 阶段状态机
├── kb/                     # 知识库
│   ├── index.md            # 总索引
│   ├── architecture.md     # 架构决策
│   ├── patterns.md         # 代码模式
│   ├── troubleshooting.md  # 排查经验
│   └── setup.md            # 环境配置
└── tmp/                    # 临时文件
```

## 三、关键约束

- `current.md` 中的 🔒 标记：修改文件前必须检查，被锁定文件不得直接修改
- 日志分层：公共日志仅记录团队级重要事件，日常操作记录在私域日志
- 审查/Bug 闭环：pending/open → fixing → resolved → closed
- 计划 status.md 默认 manual 模式，auto 需用户明确开启

## 四、Agent 操作流程

1. 会话启动：读取 `.ai/.info.json` → 自检目录 → check-kb → 回读 dev_last.md
2. 任务执行：更新 current.md 声明任务 → 锁定文件 → 编码
3. 会话结束：更新 dev_last.md → 经验暂存 → 提醒用户归档 kb/

## 五、相关文档

- 详细操作规则：`Kilo/Instructions/kilo_instructions_core.md`
- 任务归属规范：`.ai/dev/task_claim.md`
- 状态机规范：`specs/STATE_MACHINE.md`
