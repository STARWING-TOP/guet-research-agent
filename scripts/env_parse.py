"""Day 1 练习：.env 解析器。

用法：
    uv run python scripts/env_parse.py
    uv run python scripts/env_parse.py --path .env --mask
    uv run python scripts/env_parse.py --json

你需要实现两个函数：parse_env 和 mask_secrets。
main() 我已经写好了，你只要看懂它在做什么。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_env(text: str) -> dict[str, str]:
    """把 .env 文本解析成字典。

    规则（按顺序执行）：
    1. 空行（去掉空白后为空）跳过
    2. 以 # 开头的行是注释，跳过（注意：只看行首，行中间的 # 不处理）
    3. 其他行必须包含 =，否则抛 ValueError，消息里带上行号和原文
    4. 按**第一个** = 切分：key, value = line.split("=", 1)
       —— 这样 URL=a=b 才能得到 {"URL": "a=b"}
    5. key 和 value 都要 .strip() 掉两侧空白
    6. key 为空（比如 "=1"）抛 ValueError
    7. value 如果被**成对**的 ' 或 " 包住，去掉最外那一层引号
       "hello" -> hello      'hello' -> hello      "hello -> "hello（不成对，保持原样）
    8. key 重复时，后面的覆盖前面的（dict 赋值天然就是这样）

    提示：你会用到的字符串方法
        line.strip()           去掉两侧空白
        line.startswith("#")   判断注释
        "=" in line            判断是否含等号
        line.split("=", 1)     只切一刀
        s[1:-1]                去掉首尾各一个字符
        len(s) >= 2 and s[0] == s[-1]

    Args:
        text: .env 文件的完整内容

    Returns:
        键值都是 str 的字典，保持文件里的原始顺序
    """
    # TODO(你): 大约 15 行。先写 for 循环，再逐条实现上面的规则。
    raise NotImplementedError("parse_env 还没写")


def mask_secrets(env: dict[str, str]) -> dict[str, str]:
    """把所有 value 替换成 "***"，用来打印真实的 .env 而不泄露密钥。

    mask_secrets({"A": "1", "B": "secret"}) -> {"A": "***", "B": "***"}

    提示：字典推导式，一行就能写完。
    """
    # TODO(你): 1 行
    raise NotImplementedError("mask_secrets 还没写")


def main() -> int:
    parser = argparse.ArgumentParser(description="解析 .env 文件并打印")
    parser.add_argument("--path", default=".env.example", help="要解析的文件路径")
    parser.add_argument("--mask", action="store_true", help="把 value 换成 ***")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"文件不存在: {path}", file=sys.stderr)
        return 1

    try:
        env = parse_env(path.read_text(encoding="utf-8"))
    except ValueError as e:
        print(f"解析失败: {e}", file=sys.stderr)
        return 1

    if args.mask:
        env = mask_secrets(env)

    if args.json:
        print(json.dumps(env, ensure_ascii=False, indent=2))
    else:
        width = max((len(k) for k in env), default=0)
        for k, v in env.items():
            print(f"{k:<{width}} = {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
