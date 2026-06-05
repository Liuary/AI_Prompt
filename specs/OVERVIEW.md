# AI_Prompt Specification System Overview

> Last updated: 2026-05-13

## Specification List

| No. | File | Description |
|------|------|------|
| SPEC-01 | `rules.yaml` | Rule DSL Schema v1.0 — 9 fields + 4 relationship types |
| SPEC-02 | `WORKSPACE.md` | .ai/ workspace specification — public/private domain structure, log/review/bug workflows |
| SPEC-03 | `AGENT_ROLES.md` | Agent roles specification — 9 Agents' responsibilities, permissions, workflows |
| SPEC-04 | `STATE_MACHINE.md` | State machine specification — status.md lifecycle |
| SPEC-05 | `RULE_SYSTEM.md` | Rule DSL system — compile/validate/auto-write |
| — | `AIPACK.md` | .aipack template packaging format design |

## Reading Order

1. **New members**: read `WORKSPACE.md` first to understand project structure, then `AGENT_ROLES.md` to understand role division
2. **Developers**: read `RULE_SYSTEM.md` and `rules.yaml` first to understand the rule engine
3. **Architect**: read `STATE_MACHINE.md` first to understand state transitions

## Implementation Status
| Spec | Status | Core Artifacts |
|------|------|----------|
| SPEC-01 | ✓ | `specs/rules.yaml` + `rules/rules.yaml` |
| SPEC-02 | ✓ | `instructions/core.md` + `AGENTS.md` |
| SPEC-03 | ✓ | 9 Agent definition files in `adapters/kilo/agents/` |
| SPEC-04 | ✓ | `status.md` state machine + `plan/` planning system |
| SPEC-05 | ✓ | `rule_cli.py` + `lib/rule_engine.py` + `tests/` |
