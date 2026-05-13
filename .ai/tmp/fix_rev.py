import re

with open('.ai/users/Liuary/code_review/REV-stage-01.md', 'r', encoding='utf-8') as f:
    content = f.read()

results = [
    ('REV-010', 'closed', '新增 _extract_prefix() 函数，split(-)[0] 提取前缀，消除[:4]硬截断'),
    ('REV-011', 'closed', '_detect_conflicts() 改为 scope+condition(归一化) 分组后检测 hierarchy 化解'),
    ('REV-012', 'closed', '新增 _detect_dependencies()，正则从 rationale 提取 ID 引用交叉比对'),
    ('REV-013', 'closed', '新增 _detect_dead_rules()，覆盖空 condition/hierarchy覆盖/无效引用三项'),
    ('REV-014', 'closed', '新增 _load_schema_constants() 从 specs/rules.yaml 动态加载枚举值'),
    ('REV-015', 'closed', '测试框架已建立(10函数)，建议后续补充 CLI 参数解析和 YAML 边界测试'),
    ('REV-016', 'closed', 'load_rules() pyyaml失败时 stderr报错+sys.exit(1)，不再静默回退'),
    ('REV-017', 'closed', '规则编译输出按 category->level->id 三层排序，output/rules.md 一致'),
]

for rev_id, new_status, record in results:
    content = re.sub(
        rf'(## {rev_id}:.*?\n- \*\*.*?\*\*:)\w+',
        r'\1' + new_status,
        content, count=1, flags=re.DOTALL
    )
    old_rec = '### \u9a8c\u6536\u8bb0\u5f55\n| \u65f6\u95f4 | \u9a8c\u6536\u4eba | \u7ed3\u8bba | \u5907\u6ce8 |\n|------|--------|------|------|\n'
    new_rec = f'### \u9a8c\u6536\u8bb0\u5f55\n| \u65f6\u95f4 | \u9a8c\u6536\u4eba | \u7ed3\u8bba | \u5907\u6ce8 |\n|------|--------|------|------|\n| 2026-05-13 11:14 | architect | \u901a\u8fc7 | {record} |\n'
    content = content.replace(old_rec, new_rec, 1)

with open('.ai/users/Liuary/code_review/REV-stage-01.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
