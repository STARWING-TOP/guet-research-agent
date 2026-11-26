"""Day 2 练习的测试。跑法：uv run pytest tests/test_chunk.py -q

建议从下往上看：先让三个切片用例变绿（最快），再 top_chars，最后 chunk_text。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from chunk import chunk_text, odd_chars, reverse_str, top_chars, trim_ends  # noqa: E402


# ---------------------------------------------------------------- 切片三兄弟
def test_reverse_str() -> None:
    assert reverse_str("abc") == "cba"
    assert reverse_str("") == ""


def test_odd_chars() -> None:
    assert odd_chars("abcdef") == "ace"
    assert odd_chars("a") == "a"


def test_trim_ends() -> None:
    assert trim_ends("abcdefghij", 3) == "defg"
    assert trim_ends("abcdefghij") == "defg"  # 默认 n=3
    assert trim_ends("ab", 3) == ""           # 切过头就是空字符串


# ---------------------------------------------------------------- top_chars
def test_top_chars_basic() -> None:
    assert top_chars("aabbbcc", 2) == [("b", 3), ("a", 2)]


def test_top_chars_chinese() -> None:
    assert top_chars("你好你好世界", 2) == [("你", 2), ("好", 2)]


def test_top_chars_k_larger_than_unique() -> None:
    # 只有 2 种字符，要 5 个也只返回 2 个
    assert top_chars("aabb", 5) == [("a", 2), ("b", 2)]


# ---------------------------------------------------------------- chunk_text
def test_chunk_basic() -> None:
    assert chunk_text("abcdefghij", 4, 0) == ["abcd", "efgh", "ij"]


def test_chunk_with_overlap() -> None:
    assert chunk_text("abcdefghij", 4, 1) == ["abcd", "defg", "ghij"]


def test_chunk_exact_fit() -> None:
    # 正好 8 个字符、每块 4，刚好两块，不要多出空块
    assert chunk_text("abcdefgh", 4, 0) == ["abcd", "efgh"]


def test_chunk_tail_short() -> None:
    assert chunk_text("abcdefg", 4, 0) == ["abcd", "efg"]


def test_chunk_empty_text() -> None:
    assert chunk_text("", 4, 0) == []


def test_chunk_never_exceeds_size() -> None:
    for c in chunk_text("abcdefghijklmnop", 5, 2):
        assert 0 < len(c) <= 5


def test_chunk_invalid_size() -> None:
    with pytest.raises(ValueError):
        chunk_text("abc", 0, 0)


def test_chunk_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_text("abc", 4, 4)


def test_chunk_negative_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_text("abc", 4, -1)
