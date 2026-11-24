"""环境自检：配置是否加载、key 是否正常、工具是否注册、模型是否可达。

用法：uv run python scripts/doctor.py
"""

from __future__ import annotations

import sys

from agent.config import settings
from agent.llm import get_llm
from agent.tools import REGISTRY

PLACEHOLDER = "sk-your-key-here"


def main() -> int:
    key = settings.deepseek_api_key
    stripped = key.strip()

    print(f"模型       : {settings.model}")
    print(f"base_url   : {settings.deepseek_base_url}")
    print(f"key 长度   : {len(key)}")
    preview = f"{stripped[:6]}…{stripped[-4:]}" if len(stripped) > 12 else "(太短)"
    print(f"key 预览   : {preview}")

    problems: list[str] = []
    if not stripped or stripped == PLACEHOLDER:
        problems.append("key 还是占位符，.env 没填或没保存")
    if key != stripped:
        problems.append("key 首尾有空格/换行，pydantic 不会自动 strip")
    if stripped[:1] in "\"'":
        problems.append("key 被引号包住了，去掉引号")
    if 0 < len(stripped) < 20:
        problems.append(f"key 长度只有 {len(stripped)}，明显不对")

    if problems:
        print()
        for p in problems:
            print(f"  ✗ {p}")
        return 1

    print(f"工具       : {', '.join(REGISTRY)}")

    llm = get_llm()
    resp = llm.chat(
        [{"role": "user", "content": "只回复两个字：正常"}],
        max_tokens=16,
    )
    print(f"连通性     : OK -> {resp.choices[0].message.content!r}")
    print(f"用量       : {llm.usage}")
    print("\n全部通过，可以开始写代码了。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
