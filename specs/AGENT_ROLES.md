# Agent Roles Specification (AGENT_ROLES.md)

> AI_Prompt defines 9 Agent roles covering the full Plan → Code → Review → Test → Bug lifecycle.

## 1. Role Overview

| Agent | Type | Responsibility | Permission Scope |
|-------|------|------|----------|
| **Architect** | Main | Plan management, code review (submit/verify) | `.ai/` readonly source |
| **Code** | Main | Bug fixing, review issue handling | `*` all files |
| **CodeWorker** | Sub | Coding implementation in auto-loop | `*` all files |
| **Ask** | Main | Answer technical questions, look up references | Read-only |
| **Debug** | Sub | Defect investigation and root cause analysis | Read-only source |
| **ReviewWorker** | Sub | Code review in auto-loop | `.ai/` readonly source |
| **Tester** | Sub | Bug submission and fix verification | Read-only source |
| **TestWriter** | Sub | Test writing in auto-loop | `*` all files |
| **AutoRunner** | Sub | Single worktree auto-loop scheduling | `*` |

## 2. Manual Workflow
```
User → Architect (Planning / Review submission)
     → Code (Coding / Fixing)
     → Tester (Verification)
```

## 3. Automated Workflow
```
Architect → AutoRunner (Serial within worktree)
          → CodeWorker (Coding)
          → ReviewWorker (Review)
          → TestWriter (Testing)
          → Tester (Verification)
          → Debug (Debugging)
```

## 4. Key Constraints
- **Separation of Finder and Fixer**: Review issues submitted by Architect / Bugs submitted by Tester must not be self-fixed
- **Code/CodeWorker distinction**: Manual workflow uses Code, automated workflow uses CodeWorker, responsibilities are isolated
- **AutoRunner sole launcher**: Architect launches AutoRunner; AutoRunner must not create new worktrees internally
- Two consecutive verification failures → `paused`, responsibility transfers to `user`
- Unplanned architecture change → `paused`

## 5. Agent Definition Location

All Agent prompts are located in `adapters/kilo/agents/`, permissions declared in YAML header `permission` field.
