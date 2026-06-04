#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scripts/kb_graph.py
# 知识图谱可视化导出工具：从 graph.json 生成 Mermaid flowchart
#
# 用法：
#   python scripts/kb_graph.py --format mermaid         # Mermaid 格式输出
#   python scripts/kb_graph.py --format mermaid --depth 2  # 限制遍历深度
#   python scripts/kb_graph.py --from "条目名"            # 仅输出指定节点的子图
#
# 依赖：无外部依赖，仅需 graph.json 已生成（python scripts/build_kb_index.py --graph）

import json
import sys
from pathlib import Path
from collections import deque


# ── 路径常量 ────────────────────────────────────────────────────

GRAPH_FILE = Path(__file__).resolve().parent.parent / ".ai" / "tmp" / "graph.json"


def load_graph(graph_path: Path = None) -> dict:
    """加载图谱文件。"""
    src = graph_path if graph_path else GRAPH_FILE
    if not src.exists():
        print(f"错误: 图谱文件不存在: {src}")
        print("请先运行: python scripts/build_kb_index.py --graph")
        sys.exit(1)
    try:
        return json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: 图谱文件格式无效: {e}")
        sys.exit(1)


def build_adjacency(graph: dict) -> tuple[dict, dict]:
    """构建邻接表（正向 + 反向）。
    返回 (forward: {node -> [targets]}, backward: {node -> [sources]})
    """
    forward = {}
    backward = {}

    for node in graph.get("nodes", []):
        nid = node["id"]
        forward.setdefault(nid, [])
        backward.setdefault(nid, [])

    for edge in graph.get("edges", []):
        f = edge["from"]
        t = edge["to"]
        if f not in forward:
            forward[f] = []
        if t not in backward:
            backward[t] = []
        forward[f].append(t)
        backward[t].append(f)

    return forward, backward


def traverse_subgraph(graph: dict, seed_id: str, depth: int = 1) -> dict:
    """从指定节点出发，遍历 depth 层邻接子图。
    返回子图 {nodes, edges}，包含前向引用和反向被引用。
    """
    forward, backward = build_adjacency(graph)
    node_map = {n["id"]: n for n in graph.get("nodes", [])}

    if seed_id not in node_map:
        print(f"错误: 节点 '{seed_id}' 不在图谱中")
        sys.exit(1)

    visited = set()
    sub_nodes = []
    sub_edges = []
    sub_edge_set = set()
    queue = deque([(seed_id, 0)])
    visited.add(seed_id)

    while queue:
        current, d = queue.popleft()
        if d >= depth:
            continue

        for neighbor in forward.get(current, []):
            edge_key = (current, neighbor)
            if edge_key not in sub_edge_set:
                sub_edges.append({"from": current, "to": neighbor})
                sub_edge_set.add(edge_key)
            if neighbor not in visited:
                visited.add(neighbor)
                if d + 1 < depth:
                    queue.append((neighbor, d + 1))

        for neighbor in backward.get(current, []):
            edge_key = (neighbor, current)
            if edge_key not in sub_edge_set:
                sub_edges.append({"from": neighbor, "to": current})
                sub_edge_set.add(edge_key)
            if neighbor not in visited:
                visited.add(neighbor)
                if d + 1 < depth:
                    queue.append((neighbor, d + 1))

    for nid in visited:
        if nid in node_map:
            sub_nodes.append(node_map[nid])

    return {"nodes": sub_nodes, "edges": sub_edges}


def sanitize_mermaid_id(name: str) -> str:
    """将条目名转换为安全的 Mermaid 节点 ID。
    保留中文字符，替换空白和特殊符号为下划线。
    """
    sanitized = ""
    for ch in name:
        if ch.isalnum() or '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf':
            sanitized += ch
        elif ch in ('-', '_'):
            sanitized += ch
        else:
            sanitized += '_'
    return sanitized or "node"


def render_mermaid(graph: dict, indent: int = 4) -> str:
    """将图谱渲染为 Mermaid flowchart LR 格式。"""
    lines = ["flowchart LR"]
    prefix = " " * indent

    node_ids = {}
    for node in graph.get("nodes", []):
        nid = sanitize_mermaid_id(node["id"])
        suffix = ""
        count = 0
        base = nid
        while nid in node_ids:
            count += 1
            nid = f"{base}_{count}"
        node_ids[node["id"]] = nid
        display = node.get("title", node["id"]).replace('"', "'")
        lines.append(f'{prefix}{nid}["{display}"]')

    edge_set = set()
    for edge in graph.get("edges", []):
        f = node_ids.get(edge["from"])
        t = node_ids.get(edge["to"])
        if f and t:
            key = (f, t)
            if key not in edge_set:
                lines.append(f"{prefix}{f} --> {t}")
                edge_set.add(key)

    return "\n".join(lines)


def render_mermaid_raw(graph: dict) -> str:
    """直接将条目名作为 Mermaid 节点 ID 输出（无前缀缩进）。
    用于需要最短输出时的格式。
    """
    lines = ["flowchart LR"]

    node_ids = {}
    for node in graph.get("nodes", []):
        nid = sanitize_mermaid_id(node["id"])
        count = 0
        base = nid
        while nid in node_ids:
            count += 1
            nid = f"{base}_{count}"
        node_ids[node["id"]] = nid
        title = node.get("title", node["id"]).replace('"', "'")
        lines.append(f"    {nid}[\"{title}\"]")

    edge_set = set()
    for edge in graph.get("edges", []):
        f = node_ids.get(edge["from"])
        t = node_ids.get(edge["to"])
        if f and t:
            key = (f, t)
            if key not in edge_set:
                lines.append(f"    {f} --> {t}")
                edge_set.add(key)

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="知识图谱可视化导出工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python scripts/kb_graph.py --format mermaid              # 全图 Mermaid 输出
  python scripts/kb_graph.py --format mermaid --depth 1    # 仅一度关联（默认）
  python scripts/kb_graph.py --from "OAuth2 登录流程"        # 指定节点子图（深度默认 1）
  python scripts/kb_graph.py --from "状态机模式" --depth 2   # 二度关联子图
        """,
    )
    parser.add_argument(
        "--format",
        choices=["mermaid"],
        default="mermaid",
        help="输出格式（目前仅支持 mermaid）",
    )
    parser.add_argument(
        "--graph-file",
        default=None,
        help=f"图谱文件路径（默认: {GRAPH_FILE}）",
    )
    parser.add_argument(
        "--from",
        dest="seed_node",
        default=None,
        help="指定起始节点，仅输出该节点的子图",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="遍历深度，控制子图展开层数（默认: 1，仅直接关联）",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="原始模式：直接输出无缩进 Mermaid 代码",
    )
    args = parser.parse_args()

    graph_path = Path(args.graph_file).resolve() if args.graph_file else None
    graph = load_graph(graph_path)

    if args.seed_node:
        graph = traverse_subgraph(graph, args.seed_node, args.depth)
        if not graph["nodes"]:
            print(f"节点 '{args.seed_node}' 在指定深度内无关联节点")
            return

    if args.format == "mermaid":
        if args.raw:
            output = render_mermaid_raw(graph)
        else:
            output = render_mermaid(graph)
        print(output)


if __name__ == "__main__":
    main()
