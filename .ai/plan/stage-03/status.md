# stage-03 状态

- **执行模式**：manual
- **自动推进**：disabled
- **状态**：planned
- **当前责任 Agent**：architect
- **上一责任 Agent**：none
- **更新时间**：2026-05-13 00:47

## 当前任务
新增 Claude Code + GitHub Copilot 适配器，标准化适配器接口。

## 任务清单
- [ ] 创建 adapters/claude-code/ 目录和 CLAUDE.md
- [ ] 创建 .claude/commands/ 命令文件
- [ ] 创建 adapters/copilot/ 目录和 copilot-instructions.md
- [ ] 编写 ADAPTER_SPEC.md 标准化接口
- [ ] deploy.py 添加 -c/--claude 和 -p/--copilot 标志
- [ ] 编写各适配器使用指南

## 阻塞 / 暂停原因
依赖阶段一完成（规则编译器的输出格式需要适配 Claude Code 和 Copilot）

## 状态记录
| 时间 | Agent | 状态变化 | 说明 |
|------|-------|----------|------|
| 2026-05-13 00:47 | architect | none → planned | 大计划与阶段创建，等待用户确认 |
