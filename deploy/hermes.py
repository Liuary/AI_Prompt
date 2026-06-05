# deploy/hermes.py
# AI_Prompt 部署脚本 — Hermes (Ollama) 适配器

from pathlib import Path
from .common import report, copy_files

HERMES_FILES = {
    "adapters/hermes/docker-compose.yml": "adapters/hermes/docker-compose.yml",
    "adapters/hermes/Modelfile": "adapters/hermes/Modelfile",
    "adapters/hermes/instructions.md": "adapters/hermes/instructions.md",
}

HERMES_DIRS = [
    "adapters/hermes",
]


def deploy_hermes(source: Path, target: Path) -> list[str]:
    """部署 Hermes (Ollama)：复制 docker-compose、Modelfile 与使用说明。"""
    lines = []
    lines.append("\n[Hermes (Ollama)]")

    lines.append("  [适配器资源 → adapters/hermes/]")
    h_lines, copied, skipped, missing = copy_files(source, target, HERMES_FILES)
    lines.extend(h_lines)
    lines.append(report("info", f"总计: 复制 {copied}, 跳过 {skipped}" + (f", 缺失 {missing}" if missing else "")))
    return lines
