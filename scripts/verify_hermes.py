#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hermes-3 模型 Function Calling 验证脚本。

用法:
    python scripts/verify_hermes.py [--base-url http://localhost:11434/v1] [--model hermes-3:8b]
    python scripts/verify_hermes.py --help

功能:
    1. 检查 Ollama 服务连通性
    2. 验证模型支持 function calling（tool_calls 格式）
    3. 验证模型流式响应正确性
    4. 输出验证结果报告

依赖:
    pip install requests
"""

import argparse
import json
import sys
import time
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(description="Hermes-3 模型 Function Calling 验证")
    parser.add_argument("--base-url", default="http://localhost:11434/v1",
                        help="Ollama API 地址（默认 http://localhost:11434/v1）")
    parser.add_argument("--model", default="hermes-3:8b",
                        help="模型名称（默认 hermes-3:8b）")
    parser.add_argument("--timeout", type=int, default=30,
                        help="请求超时秒数（默认 30）")
    return parser


try:
    import requests
except ImportError:
    sys.exit("缺少依赖: pip install requests")


def check_connectivity(base_url: str, timeout: int) -> bool:
    """检查 Ollama 服务连通性。"""
    url = f"{base_url.rstrip('/')}/../api/tags"
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("name", "?") for m in data.get("models", [])]
            print(f"  [✓] Ollama 服务可达，已加载模型: {', '.join(models) if models else '(空)'}")
            return True
        print(f"  [✗] API 返回状态码: {resp.status_code}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"  [✗] 连接失败 — 请确认 Ollama 已启动: ollama serve")
        return False
    except requests.exceptions.Timeout:
        print(f"  [✗] 连接超时 ({timeout}s)")
        return False


def check_model_loaded(base_url: str, model: str, timeout: int) -> bool:
    """检查指定模型是否已加载。"""
    url = f"{base_url.rstrip('/')}/../api/tags"
    try:
        resp = requests.get(url, timeout=timeout)
        data = resp.json()
        for m in data.get("models", []):
            if m.get("name", "") == model:
                print(f"  [✓] 模型 {model} 已加载")
                return True
        print(f"  [✗] 模型 {model} 未加载 — 执行: ollama pull {model}")
        return False
    except Exception as e:
        print(f"  [✗] 检查模型失败: {e}")
        return False


def test_function_calling(base_url: str, model: str, timeout: int) -> dict:
    """发送 function calling 测试请求，验证模型工具调用能力。

    返回: {"success": bool, "reason": str, "response": dict|None}
    """
    chat_url = f"{base_url.rstrip('/')}/chat/completions"

    tools = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "读取指定文件的内容",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "要读取的文件路径"
                        }
                    },
                    "required": ["path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "写入内容到文件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "目标文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "要写入的内容"
                        }
                    },
                    "required": ["path", "content"]
                }
            }
        }
    ]

    messages = [
        {
            "role": "system",
            "content": "你是一个代码助手，只能通过工具调用与文件交互。不要直接回复文本，必须使用工具。"
        },
        {
            "role": "user",
            "content": "读取 /tmp/test.txt 文件的内容"
        }
    ]

    payload = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "temperature": 0.1,
        "max_tokens": 512,
    }

    try:
        resp = requests.post(chat_url, json=payload, timeout=timeout)
        if resp.status_code != 200:
            return {"success": False, "reason": f"HTTP {resp.status_code}: {resp.text[:200]}",
                    "response": None}

        data = resp.json()
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        finish_reason = choice.get("finish_reason", "")

        # 检查是否有 tool_calls
        tool_calls = message.get("tool_calls")
        if tool_calls:
            tc = tool_calls[0]
            fn_name = tc.get("function", {}).get("name", "")
            fn_args = tc.get("function", {}).get("arguments", "{}")
            return {
                "success": True,
                "reason": f"工具调用成功: {fn_name}({fn_args[:100]})",
                "tool_calls": tool_calls,
                "finish_reason": finish_reason,
            }

        # 如果没有 tool_calls，检查是否在 content 中嵌入了调用
        content = message.get("content", "")
        if content:
            if "<tool_call>" in content or "read_file" in content.lower():
                return {
                    "success": True,
                    "reason": "工具调用嵌入在文本中（非标准 tool_calls 格式）",
                    "content": content[:300],
                    "finish_reason": finish_reason,
                }
            return {
                "success": False,
                "reason": f"模型未使用工具调用，而是直接回复文本: {content[:200]}",
                "content": content[:300],
                "finish_reason": finish_reason,
            }

        return {
            "success": False,
            "reason": "模型未返回 tool_calls 或文本内容",
            "finish_reason": finish_reason,
        }

    except requests.exceptions.Timeout:
        return {"success": False, "reason": f"请求超时 ({timeout}s)", "response": None}
    except requests.exceptions.ConnectionError:
        return {"success": False, "reason": "连接失败", "response": None}
    except Exception as e:
        return {"success": False, "reason": str(e), "response": None}


def test_streaming(base_url: str, model: str, timeout: int) -> dict:
    """测试模型流式响应。

    返回: {"success": bool, "reason": str}
    """
    chat_url = f"{base_url.rstrip('/')}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "回答: 什么是函数调用？用一句话回答。"}
        ],
        "stream": True,
        "temperature": 0.1,
        "max_tokens": 128,
    }

    try:
        resp = requests.post(chat_url, json=payload, stream=True, timeout=timeout)
        if resp.status_code != 200:
            return {"success": False, "reason": f"HTTP {resp.status_code}"}

        full_content = ""
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            data_str = line[len("data: "):]
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")
                full_content += content
            except json.JSONDecodeError:
                continue

        if full_content:
            return {"success": True, "reason": f"流式响应正常 ({len(full_content)} 字符)"}
        return {"success": False, "reason": "流式响应为空"}

    except Exception as e:
        return {"success": False, "reason": str(e)}


def main():
    parser = build_parser()
    args = parser.parse_args()

    base_url = args.base_url
    model = args.model
    timeout = args.timeout

    print(f"Hermes-3 Function Calling 验证")
    print(f"  服务地址: {base_url}")
    print(f"  模型名称: {model}")
    print(f"  超时:     {timeout}s")
    print()

    results = []

    # 测试 1：连通性
    print("[1/4] 检查连通性…")
    r1 = check_connectivity(base_url, timeout)
    results.append(("连通性", r1))
    if not r1:
        print("\n验证失败: 无法连接到 Ollama 服务。")
        print("请确认:")
        print("  1. Docker: docker-compose up -d")
        print("  2. 原生:  ollama serve")
        sys.exit(1)
    print()

    # 测试 2：模型加载
    print("[2/4] 检查模型加载…")
    r2 = check_model_loaded(base_url, model, timeout)
    results.append(("模型加载", r2))
    if not r2:
        print(f"\n请先拉取模型: ollama pull {model}")
        sys.exit(1)
    print()

    # 测试 3：Function Calling
    print("[3/4] Function Calling 测试…")
    r3 = test_function_calling(base_url, model, timeout)
    results.append(("Function Calling", r3["success"]))
    if r3["success"]:
        print(f"  [✓] {r3['reason']}")
        if "tool_calls" in r3:
            print(f"  [✓] finish_reason: {r3.get('finish_reason', 'N/A')}")
    else:
        print(f"  [✗] {r3['reason']}")
        if "content" in r3:
            print(f"  模型回复: {r3['content']}")
    print()

    # 测试 4：流式响应
    print("[4/4] 流式响应测试…")
    r4 = test_streaming(base_url, model, timeout)
    results.append(("流式响应", r4["success"]))
    if r4["success"]:
        print(f"  [✓] {r4['reason']}")
    else:
        print(f"  [✗] {r4['reason']}")
    print()

    # 汇总报告
    print("=" * 50)
    print("验证结果汇总")
    print("=" * 50)
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  [{status}] {name}")

    all_passed = all(r for _, r in results)
    if all_passed:
        print("\n✓ 全部验证通过 — Hermes-3 模型可正常使用 function calling。")
        print(f"  配置 .ai/config.yaml models 中指定该模型:")
        print(f"    provider: ollama")
        print(f"    model_name: {model}")
        print(f"    base_url: {base_url}")
        sys.exit(0)
    else:
        print("\n✗ 存在未通过的验证项，请检查上述输出。")
        sys.exit(1)


if __name__ == "__main__":
    main()
