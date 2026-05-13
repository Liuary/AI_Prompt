# .aipack 模板打包格式设计

> 优先级：低  |  状态：设计完成，暂不实现

## 格式

`.aipack` 是一个 tar.gz 压缩包，内含 AI_Prompt 框架的最小部署单元。

```
my-template.aipack
├── aipack.json          # 模板元信息（必需）
├── AGENTS.md            # 主约束文件（必需）
├── .ai/                 # 工作区模板（必需）
│   ├── dev/
│   ├── kb/
│   └── plan/
├── adapters/            # 适配器文件（可选）
│   ├── claude-code/
│   └── copilot/
└── rules/               # 规则实例（可选）
    └── rules.yaml
```

## aipack.json 格式

```json
{
  "name": "startup-template",
  "version": "1.0.0",
  "description": "适用于初创项目的 AI_Prompt 最小模板",
  "author": "AI_Prompt",
  "tags": ["startup", "minimal"],
  "tools": ["kilo"],
  "requires": {
    "ai_prompt": ">=2.0"
  }
}
```

## 示例模板

| 模板 | 内容 | 适用场景 |
|------|------|----------|
| `startup-template` | 核心约束 + minimal 工作区 | 3-5人小团队 |
| `enterprise-template` | 完整规范 + 9 Agent + 审查/Bug 全流程 | 10+人团队 |

## 部署方式

```bash
python deploy.py /path/to/target --source ./my-template.aipack
```

deploy.py 自动解包并部署。

## 实现时机

当前 deploy.py 已支持本地目录部署。.aipack 打包在以下条件满足时实现：
- 用户需要通过远程分发模板
- 模板市场需要标准化分发格式
