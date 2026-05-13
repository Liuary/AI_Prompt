#!/usr/bin/env python3
# rule_cli.py
# AI_Prompt 规则工具 CLI：编译（DSL → Markdown）和校验（冲突/冗余检测）
#
# 用法：
#   python rule_cli.py compile [rules_file] [--output OUTPUT]
#   python rule_cli.py validate [rules_file] [--verbose]

import argparse
import sys
import os
from pathlib import Path

# 确保 lib/ 在导入路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.rule_engine import load_rules, compile_rules, validate_rules

# ── 命令行参数 ─────────────────────────────────────────────────

def build_parser():
    """构建 argparse 解析器。"""
    parser = argparse.ArgumentParser(
        prog="rule_cli",
        description="AI_Prompt 规则工具：编译和校验规则 DSL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python rule_cli.py compile                          # 编译 rules/rules.yaml 到标准输出
  python rule_cli.py compile -o output/rules.md       # 编译并写出到文件
  python rule_cli.py validate                         # 校验 rules/rules.yaml
  python rule_cli.py validate -v                      # 详细输出校验结果
        """,
    )

    sub = parser.add_subparsers(dest="command", help="子命令")

    # compile 子命令
    cp = sub.add_parser("compile", help="将规则 YAML 编译为 Markdown")
    cp.add_argument(
        "rules_file", nargs="?", default="rules/rules.yaml",
        help="规则文件路径（默认：rules/rules.yaml）",
    )
    cp.add_argument(
        "-o", "--output", default=None,
        help="输出文件路径（默认：标准输出）",
    )

    # validate 子命令
    vp = sub.add_parser("validate", help="校验规则完整性和一致性")
    vp.add_argument(
        "rules_file", nargs="?", default="rules/rules.yaml",
        help="规则文件路径（默认：rules/rules.yaml）",
    )
    vp.add_argument(
        "-v", "--verbose", action="store_true",
        help="显示所有问题（含 info 级别），默认仅显示 error 和 warning",
    )

    return parser


# ── 主函数 ─────────────────────────────────────────────────────

def main():
    # UTF-8 编码
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    # 检查规则文件存在
    rules_path = Path(args.rules_file)
    if not rules_path.exists():
        print(f"错误：规则文件不存在：{rules_path}", file=sys.stderr)
        sys.exit(1)

    try:
        rules = load_rules(str(rules_path))
    except Exception as e:
        print(f"错误：加载规则文件失败：{e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "compile":
        _cmd_compile(rules, args)

    elif args.command == "validate":
        _cmd_validate(rules, args)


def _cmd_compile(rules, args):
    """执行 compile 子命令。"""
    output_path = args.output
    if output_path is not None:
        output_path = str(Path(output_path))

    result = compile_rules(rules, output_path)

    if output_path is None:
        print(result)
    else:
        print(f"编译完成：{len(rules)} 条规则 → {output_path}")


def _cmd_validate(rules, args):
    """执行 validate 子命令。"""
    issues = validate_rules(rules)

    # 按级别筛选
    if not args.verbose:
        issues = [(lvl, rid, desc) for lvl, rid, desc in issues if lvl in ("error", "warning")]

    if not issues:
        print(f"校验通过：{len(rules)} 条规则，无问题。")
        return

    # 分组输出
    error_count = sum(1 for lvl, _, _ in issues if lvl == "error")
    warn_count = sum(1 for lvl, _, _ in issues if lvl == "warning")
    info_count = sum(1 for lvl, _, _ in issues if lvl == "info")

    print(f"校验完成：{len(rules)} 条规则，发现 {error_count} 错误、{warn_count} 告警、{info_count} 提示")
    print()

    for lvl, rid, desc in issues:
        tag = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(lvl, "?")
        print(f"  {tag} [{rid}] {desc}")

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
