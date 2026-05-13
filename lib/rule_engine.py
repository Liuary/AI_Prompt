# lib/rule_engine.py
# AI_Prompt 规则引擎：YAML 加载、Markdown 编译、冲突/冗余/依赖/死规则校验
#
# 本模块提供规则 DSL 的核心处理逻辑：
#   - load_rules()          从 YAML 加载规则实例
#   - compile_rules()       将规则编译为 Markdown 输出
#   - validate_rules()      校验规则的完整性和一致性
#   - _detect_conflicts()   按 specs 定义检测 action 矛盾
#   - _detect_dependencies() 检测 rationale 中的规则引用链
#   - _detect_redundancies() 检测高度相似的规则对
#   - _detect_dead_rules()  检测空 condition / 过度覆盖 / 无效引用

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# ── Schema 常量加载 ─────────────────────────────────────────────

def _load_schema_constants():
    """从 specs/rules.yaml 加载枚举常量，避免硬编码。

    返回 (valid_levels, valid_scopes, valid_enforcements, valid_relations)
    """
    schema_path = Path(__file__).resolve().parent.parent / "specs" / "rules.yaml"
    try:
        import yaml
        with open(schema_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except Exception:
        # 无法加载 schema 时回退到硬编码默认值
        return (
            {"error", "warning", "info"},
            {"all", "conversation", "code", "docs", "workflow"},
            {"strict", "advisory", "auto"},
            {"hierarchy", "dependency", "conflict", "redundancy"},
        )

    fields = spec.get("rule_fields", {})
    levels = set(fields.get("level", {}).get("values", []))
    scopes = set(fields.get("scope", {}).get("values", []))
    enforcements = set(fields.get("enforcement", {}).get("values", []))
    # relations types 在顶层 relations 章节
    relations_data = spec.get("relations", {}).get("types", [])
    if isinstance(relations_data, list) and relations_data and isinstance(relations_data[0], dict):
        relations = {t.get("description", "").split("：")[1].strip() if "：" in t.get("description", "") else "" for t in relations_data}
        # 实际从类型名提取
        relations = set()
        for t in relations_data:
            name = list(t.keys())[0] if isinstance(t, dict) and t else ""
            if name:
                relations.add(name.split(":")[0].strip())
    elif isinstance(relations_data, list):
        relations = set()
        for t in relations_data:
            if isinstance(t, str):
                relations.add(t.split(":")[0].strip())
    else:
        relations = {"hierarchy", "dependency", "conflict", "redundancy"}

    return levels, scopes, enforcements, relations


# 模块初始化时加载
_VALID_LEVELS, _VALID_SCOPES, _VALID_ENFORCEMENTS, _VALID_RELATIONS = _load_schema_constants()
ID_PATTERN = re.compile(r"^[A-Z]{2,6}-\d{3}$")
ID_REF_PATTERN = re.compile(r"[A-Z]{2,6}-\d{3}")


# ── YAML 加载 ──────────────────────────────────────────────────

def load_rules(path):
    """从 YAML 文件加载规则列表。依赖 pyyaml，不可用时报错终止。"""
    try:
        import yaml
    except ImportError:
        print("错误：缺少 pyyaml 库。请运行：pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"错误：解析 YAML 文件失败：{path}\n{e}", file=sys.stderr)
        sys.exit(1)

    if data is None:
        raise ValueError(f"文件为空或格式错误：{path}")

    rules = data.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError(f"rules 字段应为列表：{path}")
    return rules


# ── 编译 ────────────────────────────────────────────────────────

CATEGORY_MAP = {
    "CORE": "核心约束",
    "BEH": "行为准则",
    "STYLE": "编码风格",
    "OPS": "操作规范",
    "CMT": "注释规范",
    "META": "元规则/体系规则",
    "DEV": "开发期动态规则",
    "INST": "操作规则",
}

LEVEL_MARK = {
    "error": "🔴 MUST",
    "warning": "🟡 SHOULD",
    "info": "🔵 MAY",
}

SCOPE_CN = {
    "all": "全部活动",
    "conversation": "对话交互",
    "code": "代码编写",
    "docs": "文档编写",
    "workflow": "工作流操作",
}


def _extract_prefix(rule_id):
    """从规则 ID 中提取分类前缀（如 CORE-001 → CORE，STYLE-003 → STYLE）。"""
    if not rule_id:
        return "UNK"
    match = ID_PATTERN.match(rule_id)
    if match:
        # 从匹配的 ID 格式中提取前缀部分（- 之前）
        return rule_id.split("-")[0]
    return "UNK"


def compile_rules(rules, output_path=None):
    """将规则列表编译为 Markdown 字符串，可写出到文件。"""
    grouped = defaultdict(list)
    for rule in rules:
        prefix = _extract_prefix(rule.get("id", ""))
        grouped[prefix].append(rule)

    lines = [
        "# AI Agent 行为约束（编译自 rules/rules.yaml）",
        "",
        f"> 共 {len(rules)} 条规则，编译时间：自动生成",
        "",
    ]

    cat_order = ["CORE", "BEH", "OPS", "STYLE", "CMT", "META", "DEV", "INST"]
    for cat in cat_order:
        if cat not in grouped:
            continue
        cat_rules = grouped[cat]
        cat_title = CATEGORY_MAP.get(cat, cat)

        lines.append(f"## {cat_title}")
        lines.append("")

        # 按级别排序：error > warning > info，同级别内按 id 字典序
        level_order = {"error": 0, "warning": 1, "info": 2}
        cat_rules.sort(key=lambda r: (level_order.get(r.get("level", "info"), 3), r.get("id", "ZZZ-000")))

        for i, rule in enumerate(cat_rules, 1):
            rid = rule.get("id", "???")
            level = rule.get("level", "info")
            scope = rule.get("scope", "all")
            condition = rule.get("condition", "").strip()
            action = rule.get("action", "").strip()
            rationale = rule.get("rationale", "").strip()
            source = rule.get("source", "")

            mark = LEVEL_MARK.get(level, "")
            scope_label = SCOPE_CN.get(scope, scope)

            lines.append(f"### {i}. {rid} {mark}")
            lines.append(f"- **适用范围**：{scope_label}")
            lines.append(f"- **触发条件**：{condition}")
            lines.append(f"- **行为要求**：{action}")
            if rationale:
                lines.append(f"- **理由**：{rationale}")
            if source:
                lines.append(f"- **来源**：{source}")

            relations = rule.get("relations", [])
            if relations:
                lines.append(f"- **关联规则**：")
                for rel in relations:
                    if isinstance(rel, dict):
                        lines.append(f"  - [{rel.get('type', '?')}] → {rel.get('target', '?')}：{rel.get('description', '')}")
                    else:
                        lines.append(f"  - {rel}")

            lines.append("")

    result = "\n".join(lines)

    if output_path is not None:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

    return result


# ── 校验 ────────────────────────────────────────────────────────

def validate_rules(rules):
    """校验规则列表，返回问题列表 [(严重程度, 规则ID, 描述), ...]。"""
    issues = []
    all_ids = {r.get("id") for r in rules if r.get("id")}

    # 逐规则字段检查
    for rule in rules:
        rid = rule.get("id", "???")
        for field in ["id", "level", "scope", "condition", "action", "enforcement", "rationale", "source"]:
            if field not in rule or not rule[field]:
                issues.append(("error", rid, f"缺少必要字段：{field}"))

        if not ID_PATTERN.match(str(rid).strip()):
            issues.append(("error", rid, f"ID 格式无效（应为 大写前缀-三位数字）：{rid}"))

        if rule.get("level") not in _VALID_LEVELS:
            issues.append(("error", rid, f"level 值无效：{rule.get('level')}（有效值：{', '.join(_VALID_LEVELS)}）"))

        if rule.get("scope") not in _VALID_SCOPES:
            issues.append(("error", rid, f"scope 值无效：{rule.get('scope')}（有效值：{', '.join(_VALID_SCOPES)}）"))

        if rule.get("enforcement") not in _VALID_ENFORCEMENTS:
            issues.append(("error", rid, f"enforcement 值无效：{rule.get('enforcement')}（有效值：{', '.join(_VALID_ENFORCEMENTS)}）"))

        # relations 引用检查
        relations = rule.get("relations", [])
        if isinstance(relations, list):
            for rel in relations:
                if isinstance(rel, dict):
                    target = rel.get("target", "")
                    if target and target not in all_ids:
                        issues.append(("warning", rid, f"relations 引用了不存在的规则：{target}"))
                    if rel.get("type") not in _VALID_RELATIONS:
                        issues.append(("warning", rid, f"relations 类型无效：{rel.get('type')}"))

    # 重复 id
    id_counts = defaultdict(int)
    for rule in rules:
        id_counts[rule.get("id")] += 1
    for rid, count in id_counts.items():
        if count > 1:
            issues.append(("error", rid, f"重复 ID，出现 {count} 次"))

    # 冲突、依赖、冗余、死规则检测
    issues.extend(_detect_conflicts(rules))
    issues.extend(_detect_dependencies(rules))
    issues.extend(_detect_redundancies(rules))
    issues.extend(_detect_dead_rules(rules, all_ids))

    return issues


def _detect_conflicts(rules):
    """按 specs 定义：同一 scope+condition 下 action 矛盾的规则。

    specs/rules.yaml: 「按 scope + condition 分组后对比 action」
    """
    issues = []
    # 按 (scope, simplified_condition) 分组
    groups = defaultdict(list)
    for r in rules:
        cond = r.get("condition", "").strip()
        # 简化 condition：去标点、取前 30 字符做粗略分组
        simple = re.sub(r"[、。，；：\s]+", "", cond)[:30].lower()
        key = (r.get("scope", "all"), simple)
        groups[key].append(r)

    for (scope, _), group in groups.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                ri, rj = group[i], group[j]
                if ri.get("id") == rj.get("id"):
                    continue
                # 检查是否有 hierarchy 关系标注解决冲突
                has_resolution = False
                for rel in ri.get("relations", []):
                    if isinstance(rel, dict) and rel.get("type") == "hierarchy" and rel.get("target") == rj.get("id"):
                        has_resolution = True
                for rel in rj.get("relations", []):
                    if isinstance(rel, dict) and rel.get("type") == "hierarchy" and rel.get("target") == ri.get("id"):
                        has_resolution = True
                if not has_resolution:
                    issues.append(("info", f"{ri.get('id')}↔{rj.get('id')}",
                                   f"同一 scope+condition ({scope}) 下可能存在 action 冲突，且无 hierarchy 关系标注"))
    return issues


def _detect_dependencies(rules):
    """检测 rationale 中引用的规则 ID 是否有对应的 relations 标注。

    specs/rules.yaml: 「rationale 字段中提及其他规则 ID」
    """
    issues = []
    all_ids = {r.get("id") for r in rules if r.get("id")}

    for rule in rules:
        rid = rule.get("id", "???")
        rationale = rule.get("rationale", "")
        # 提取 rationale 中引用的规则 ID
        refs = set(ID_REF_PATTERN.findall(rationale))
        # 排除自我引用
        refs.discard(rid)

        declared_targets = set()
        for rel in rule.get("relations", []):
            if isinstance(rel, dict):
                declared_targets.add(rel.get("target", ""))

        # 引用但未声明的
        for ref in refs:
            if ref not in declared_targets:
                issues.append(("info", rid,
                               f"rationale 引用了规则 {ref}，但未在 relations 中声明 dependency 关系"))
            # 检查目标规则是否存在
            if ref not in all_ids:
                issues.append(("warning", rid, f"rationale 引用了不存在的规则：{ref}"))

    return issues


def _tokenize(text):
    """将文本拆分为 token 集合，兼顾英文分词和中文单字切分。"""
    tokens = set()
    # 英文/数字词
    for word in re.findall(r"[a-zA-Z0-9_]+", text.lower()):
        tokens.add(word)
    # 中文字符（单字切分，兼顾 n-gram）
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
    for i in range(len(chinese_chars) - 1):
        tokens.add(chinese_chars[i] + chinese_chars[i + 1])  # 二元组
    return tokens


def _detect_redundancies(rules):
    """检测高度相似的规则对（scope + level + enforcement 相同，action 相似度 > 70%）。"""
    issues = []
    for i in range(len(rules)):
        for j in range(i + 1, len(rules)):
            ri, rj = rules[i], rules[j]
            if (ri.get("scope") == rj.get("scope") and
                    ri.get("level") == rj.get("level") and
                    ri.get("enforcement") == rj.get("enforcement")):
                tokens_i = _tokenize(ri.get("action", ""))
                tokens_j = _tokenize(rj.get("action", ""))
                if tokens_i and tokens_j:
                    intersection = tokens_i & tokens_j
                    union = tokens_i | tokens_j
                    similarity = len(intersection) / len(union) if union else 0
                    if similarity > 0.7:
                        issues.append(("warning", f"{ri.get('id')}↔{rj.get('id')}",
                                       f"高度相似（相似度 {similarity:.0%}），可能存在冗余"))
    return issues


def _detect_dead_rules(rules, all_ids):
    """检测死规则：
    1. condition 为空或仅空白
    2. 被 hierarchy 标注完全覆盖（scope 相同 + 上级已覆盖）
    3. relations 引用不存在的目标规则（补充检查）
    """
    issues = []

    # 检测 1：空 condition
    for rule in rules:
        rid = rule.get("id", "???")
        cond = rule.get("condition", "").strip()
        if not cond:
            issues.append(("warning", rid, "死规则：condition 为空或仅空白，规则永不会被触发"))

    # 检测 2：被 hierarchy 完全覆盖
    # 收集所有 hierarchy 覆盖关系
    covered = defaultdict(set)  # rule_id → {被其覆盖的 rule_id...}
    for rule in rules:
        for rel in rule.get("relations", []):
            if isinstance(rel, dict) and rel.get("type") == "hierarchy":
                covered[rule.get("id")].add(rel.get("target"))

    for parent_id, children in covered.items():
        parent = next((r for r in rules if r.get("id") == parent_id), None)
        if parent is None:
            continue
        parent_scope = parent.get("scope")
        # scope=all 的 hierarchy 是元规则覆盖，不视为死规则
        if parent_scope == "all":
            continue
        for child_id in children:
            child = next((r for r in rules if r.get("id") == child_id), None)
            if child is None:
                continue
            if child.get("scope") == parent_scope:
                issues.append(("info", child_id,
                               f"可能为死规则：被 hierarchy 上级 {parent_id} 覆盖（scope={parent_scope}），"
                               f"永不会独立触发（除非作为例外条件）"))

    # 检测 3：relations 引用无效目标
    for rule in rules:
        rid = rule.get("id", "???")
        for rel in rule.get("relations", []):
            if isinstance(rel, dict):
                target = rel.get("target", "")
                if target and target not in all_ids:
                    issues.append(("error", rid, f"relations 引用了不存在的目标规则：{target}"))

    return issues
