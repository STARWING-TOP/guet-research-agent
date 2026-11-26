"""Day 2 练习：容器、切片、文本分块。

今天不要求你从零写逻辑，只填 5 个 TODO。
建议顺序：先做最下面三个一行的切片练习（最快出结果），再做 top_chars，最后做 chunk_text。

跑测试：
    uv run pytest tests/test_chunk.py -q
"""

from __future__ import annotations

from collections import Counter


# ======================================================================
# 练习 1：字符频率 top K（练 dict + Counter）
# ======================================================================
def top_chars(text: str, k: int = 5) -> list[tuple[str, int]]:
    """返回出现次数最多的前 k 个字符，格式 [(字符, 次数), ...]，按次数降序。

    例：
        top_chars("aabbbcc", 2) -> [('b', 3), ('a', 2)]
        top_chars("你好你好世界", 2) -> [('你', 2), ('好', 2)]

    提示：
        Counter("aabbbcc")            -> Counter({'b': 3, 'a': 2, 'c': 2})
        Counter("aabbbcc").most_common(2) -> [('b', 3), ('a', 2)]

        most_common 返回的元组列表，正好就是要求的格式，
        所以整个函数可以写成 1 行：直接 return。
    """
    # TODO(你): 1 行
    raise NotImplementedError("top_chars 还没写")


# ======================================================================
# 练习 2：文本分块（W4 检索要用，今天的重点）
# ======================================================================
def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """把长文本切成固定长度的块，相邻块之间有 overlap 个字符重叠。

    例（size=4, overlap=1，步长 = 3）：
        text = "abcdefghij"
        chunk[0] = text[0:4]  = "abcd"
        chunk[1] = text[3:7]  = "defg"
        chunk[2] = text[6:10] = "ghij"
        -> ["abcd", "defg", "ghij"]

    规则：
    1. size <= 0          -> raise ValueError
    2. overlap >= size    -> raise ValueError（重叠不能大于等于块长，否则原地打转）
    3. overlap < 0        -> raise ValueError
    4. 步长 step = size - overlap
    5. 从 0 开始，每次跳 step，取 text[i : i+size]
    6. 最后一块允许短于 size（tail），只要非空就保留
    7. 已经取到末尾就停（i + size >= len(text) 时取完这块就 break）

    提示：
        for i in range(0, len(text), step):
            piece = text[i:i+size]
            ...
            if i + size >= len(text):
                break

    Args:
        text:    原文
        size:    每块的目标长度
        overlap: 相邻块重叠的字符数

    Returns:
        块的列表，保持原文顺序
    """
    if size <= 0:
        raise ValueError(f"size 必须大于 0，收到 {size}")
    if overlap < 0:
        raise ValueError(f"overlap 不能为负，收到 {overlap}")
    if overlap >= size:
        raise ValueError(f"overlap({overlap}) 必须小于 size({size})")

    step = size - overlap
    chunks: list[str] = []

    # TODO(你): 大约 6 行。照着上面的提示写 for 循环。
    raise NotImplementedError("chunk_text 还没写")

    return chunks


# ======================================================================
# 练习 3：三个切片小练习（每个 1 行）
# ======================================================================
def reverse_str(s: str) -> str:
    """反转字符串。reverse_str("abc") -> "cba"

    提示：切片的第三个参数是步长，-1 表示从后往前。
    """
    # TODO(你): 1 行
    raise NotImplementedError("reverse_str 还没写")


def odd_chars(s: str) -> str:
    """取出所有下标为偶数的字符（0, 2, 4...）。odd_chars("abcdef") -> "ace"

    提示：s[起始:结束:步长]，步长 2 就是每隔一个取一个。
    """
    # TODO(你): 1 行
    raise NotImplementedError("odd_chars 还没写")


def trim_ends(s: str, n: int = 3) -> str:
    """去掉首尾各 n 个字符。trim_ends("abcdefghij", 3) -> "defg"

    提示：负数下标表示从末尾倒数。
    """
    # TODO(你): 1 行
    raise NotImplementedError("trim_ends 还没写")
