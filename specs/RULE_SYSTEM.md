# 规则 DSL 体系规范 (RULE_SYSTEM.md)

> 定义 AI Agent 行为约束从自然语言到结构化 YAML 再到编译/校验的完整体系。

## 一、架构

```
AGENTS.md / dev_core.md（自然语言约束）
        │
        ▼  人工编码
specs/rules.yaml（DSL Schema v1.0）
        │
        ▼  实例化
rules/rules.yaml（结构化规则实例）
        │
        ├──► rule_cli.py compile ──► Markdown 规则文档
        │
        └──► rule_cli.py validate ──► 完整性问题列表
```

## 二、DSL Schema（specs/rules.yaml）

### 规则字段（9 个）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识符（如 CORE-001） |
| `level` | enum | error / warning / info |
| `scope` | enum | all / conversation / code / docs / workflow |
| `condition` | string | 触发条件 |
| `action` | string | 行为要求（must/should/may） |
| `enforcement` | enum | strict / advisory / auto |
| `rationale` | string | 规则理由 |
| `source` | string | 来源追溯 |
| `relations` | array | 关联规则（hierarchy/dependency/conflict/redundancy） |

### 分类前缀

| 前缀 | 章节 |
|------|------|
| CORE | 核心约束 |
| BEH | 行为准则 |
| OPS | 操作规范 |
| STYLE | 编码风格 |
| CMT | 注释规范 |
| META | 元规则/体系规则 |
| DEV | 开发期动态规则 |
| INST | Instructions 规则 |

## 三、编译输出

`rule_cli.py compile` 将规则按 category → level → id 排序输出 Markdown：
- 🔴 MUST（error 级）
- 🟡 SHOULD（warning 级）
- 🔵 MAY（info 级）

## 四、校验能力

`rule_cli.py validate` 自动检测：
1. **字段完整性**：9 字段缺失检查
2. **格式合法性**：ID 格式、枚举值
3. **关系检测**：hierarchy/dependency/conflict/redundancy
4. **死规则**：空 condition、过度覆盖、无效引用

## 五、知识库自动写入

通过 dev_last.md 中转：
1. 会话结束 → 经验暂存 dev_last.md
2. 下次启动 → 提醒用户确认
3. 确认后 → 归档 kb/ 分类文件
4. 更新 kb/index.md + 公共日志
