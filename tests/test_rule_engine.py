# tests/test_rule_engine.py
# AI_Prompt 规则引擎测试
#
# 运行：pytest tests/ -v 或 python -c "..."  直接调用测试函数
# 依赖：pip install pyyaml

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.rule_engine import (
    _extract_prefix,
    _detect_conflicts,
    _detect_dependencies,
    _detect_redundancies,
    _detect_dead_rules,
    validate_rules,
    compile_rules,
    _VALID_LEVELS,
    _VALID_SCOPES,
    _VALID_ENFORCEMENTS,
    _VALID_RELATIONS,
)

# ── 前缀提取测试（REV-010）─────────────────────────────────────

def test_extract_prefix_4char():
    assert _extract_prefix("CORE-001") == "CORE"

def test_extract_prefix_5char():
    assert _extract_prefix("STYLE-003") == "STYLE"

def test_extract_prefix_invalid_id():
    assert _extract_prefix("") == "UNK"
    assert _extract_prefix("bad") == "UNK"


# ── 冲突检测测试（REV-011）─────────────────────────────────────

def test_detect_conflicts_same_scope_condition():
    rules = [
        {"id": "CORE-001", "scope": "code", "condition": "when writing code", "action": "must do A", "relations": []},
        {"id": "CORE-002", "scope": "code", "condition": "when writing code", "action": "must do B", "relations": []},
    ]
    issues = _detect_conflicts(rules)
    assert len(issues) == 1
    assert "CORE-001" in issues[0][1] and "CORE-002" in issues[0][1]

def test_detect_conflicts_with_hierarchy_resolved():
    rules = [
        {"id": "CORE-001", "scope": "code", "condition": "when writing code", "action": "must do A",
         "relations": [{"type": "hierarchy", "target": "CORE-002"}]},
        {"id": "CORE-002", "scope": "code", "condition": "when writing code", "action": "must do B", "relations": []},
    ]
    issues = _detect_conflicts(rules)
    assert len(issues) == 0


# ── 依赖检测测试（REV-012）─────────────────────────────────────

def test_detect_dependencies_rationale_ref():
    rules = [
        {"id": "CORE-001", "rationale": "参见 CORE-002 的规定", "relations": []},
        {"id": "CORE-002", "rationale": "...", "relations": []},
    ]
    issues = _detect_dependencies(rules)
    assert any("rationale 引用了规则 CORE-002" in issue[2] for issue in issues)


# ── 死规则检测测试（REV-013）───────────────────────────────────

def test_dead_rule_empty_condition():
    rules = [{
        "id": "XXX-001", "level": "warning", "scope": "code",
        "condition": "", "action": "...", "enforcement": "strict",
        "rationale": "...", "source": "..."
    }]
    all_ids = {r["id"] for r in rules}
    issues = _detect_dead_rules(rules, all_ids)
    assert any("condition 为空" in issue[2] for issue in issues)

def test_dead_rule_invalid_ref():
    rules = [{
        "id": "XXX-001", "level": "warning", "scope": "code",
        "condition": "...", "action": "...", "enforcement": "strict",
        "rationale": "...", "source": "...",
        "relations": [{"type": "hierarchy", "target": "MISS-999"}]
    }]
    all_ids = {r["id"] for r in rules}
    issues = _detect_dead_rules(rules, all_ids)
    assert any("不存在的目标规则" in issue[2] for issue in issues)


# ── Schema 常量加载测试（REV-014）──────────────────────────────

def test_valid_levels_from_schema():
    assert "error" in _VALID_LEVELS
    assert "warning" in _VALID_LEVELS
    assert "info" in _VALID_LEVELS

def test_valid_scopes_from_schema():
    assert "all" in _VALID_SCOPES
    assert "code" in _VALID_SCOPES
    assert "conversation" in _VALID_SCOPES

def test_valid_enforcements_from_schema():
    assert "strict" in _VALID_ENFORCEMENTS
    assert "advisory" in _VALID_ENFORCEMENTS
    assert "auto" in _VALID_ENFORCEMENTS

def test_valid_relations_from_schema():
    assert "hierarchy" in _VALID_RELATIONS
    assert "dependency" in _VALID_RELATIONS


# ── 编译输出测试（REV-017）─────────────────────────────────────

def test_compile_output_sorted():
    rules = [
        {"id": "CORE-003", "level": "warning", "scope": "code", "condition": "...", "action": "...", "rationale": "...", "source": "...", "relations": []},
        {"id": "CORE-001", "level": "error", "scope": "code", "condition": "...", "action": "...", "rationale": "...", "source": "...", "relations": []},
        {"id": "CORE-002", "level": "error", "scope": "code", "condition": "...", "action": "...", "rationale": "...", "source": "...", "relations": []},
    ]
    result = compile_rules(rules)
    # error 级别的应该在前面
    pos_001 = result.index("CORE-001")
    pos_002 = result.index("CORE-002")
    pos_003 = result.index("CORE-003")
    assert pos_001 < pos_002  # 同 error 级按 id 排序
    assert pos_002 < pos_003  # error 在 warning 前


# ── 完整校验测试 ───────────────────────────────────────────────

def test_validate_valid_rules():
    rules = [
        {"id": "CORE-001", "level": "error", "scope": "conversation", "condition": "when user makes request", "action": "must analyze", "enforcement": "strict", "rationale": "防止误解", "source": "AGENTS.md § 1", "relations": []},
    ]
    issues = validate_rules(rules)
    assert len(issues) == 0

def test_validate_missing_field():
    rules = [
        {"id": "CORE-001", "level": "error", "scope": "conversation", "condition": "when", "action": "do", "enforcement": "strict", "rationale": "because", "source": ""},
    ]
    issues = validate_rules(rules)
    assert any("source" in issue[2] for issue in issues)

def test_validate_duplicate_id():
    rules = [
        {"id": "CORE-001", "level": "error", "scope": "code", "condition": "a", "action": "a", "enforcement": "strict", "rationale": "a", "source": "a"},
        {"id": "CORE-001", "level": "error", "scope": "code", "condition": "b", "action": "b", "enforcement": "strict", "rationale": "b", "source": "b"},
    ]
    issues = validate_rules(rules)
    assert any("重复" in issue[2] for issue in issues)


# ── 冗余检测测试 ───────────────────────────────────────────────

def test_detect_redundancy_similar_actions():
    rules = [
        {"id": "A-001", "scope": "code", "level": "warning", "enforcement": "strict",
         "action": "must check and verify then report to user", "rationale": "...", "source": "...", "condition": "...", "relations": []},
        {"id": "A-002", "scope": "code", "level": "warning", "enforcement": "strict",
         "action": "must check and verify then report to user promptly", "rationale": "...", "source": "...", "condition": "...", "relations": []},
    ]
    issues = _detect_redundancies(rules)
    assert len(issues) >= 1
    assert "高度相似" in issues[0][2]
