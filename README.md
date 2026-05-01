# AI_Prompt

Kilo Code AI Agent 约束文件与工作目录规划仓库，提供单人协作和多人团队协作两套核心约束模板，并定义标准化的 `.ai` 目录结构用于管理开发计划、操作日志和团队经验。

## 目录结构

```
AI_Prompt/
├── Kilo/Instructions/          # Kilo Code 核心约束文件
│   ├── kilo_instructions_core.md       # 单人协作版
│   └── kilo_instructions_core_team.md  # 多人协作版
├── .ai/                        # AI 工作目录（公共域，纳入版本管理）
│   ├── dev/                    # 核心规则与开发笔记
│   ├── log/                    # 操作日志
│   ├── plan/                   # 项目计划
│   └── tmp/                    # 临时文件
└── .gitignore
```

## 核心约束

两份约束文件定义了 Kilo Code Agent 的行为准则，包含以下共同模块：

- **核心约束**：需求分析确认、避免过度设计、修改范围控制、多方案对比选优、元规则冲突仲裁
- **操作规范**：编码规范、文件拆分策略、偏差记录、版本管理建议

### 单人版 vs 多人版

| 特性 | 单人版 | 多人协作版 |
|------|--------|-----------|
| `.ai` 目录 | 统一共享 | 分为公共域 + 私域（`users/{username}/`） |
| 用户身份 | 无 | `.ai/.info.json` 自动识别 |
| 操作状态 | `dev/dev_last.md` | `users/{username}/dev_last.md` |
| 日志命名 | `yyyy-mm-dd-NNN.md` | `yyyy-mm-dd-{username}-NNN.md` |
| 笔记归属 | 单份 | 公共笔记 + 个人笔记分离 |

## 私域与公共域（多人协作版）

- **公共域**：`.ai/dev/`、`.ai/log/`、`.ai/plan/`、`.ai/tmp/` — 项目级共享，纳入 Git
- **私域**：`.ai/users/{username}/` — 个人状态、笔记、临时文件，Git 忽略
