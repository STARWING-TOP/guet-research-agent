"""Day 1 练习的测试：12 个用例覆盖 parse_env 的全部规则。

跑法：
    uv run pytest tests/test_env_parse.py -v

全绿就说明你写对了。测试就是"需求说明书"，看不懂哪个用例就来问我。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# scripts/ 不是包，所以手动把它加进模块搜索路径。
# 等你学到 Day 6「模块」时，会明白 sys.path 是什么。
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from env_parse import mask_secrets, parse_env  # noqa: E402


def test_basic() -> None:
    assert parse_env("A=1\nB=2") == {"A": "1", "B": "2"}


def test_empty_text() -> None:
    assert parse_env("") == {}


def test_skip_comment_and_blank_lines() -> None:
    text = "# 这是注释\n\nA=1\n   \n# 又一条注释\nB=2\n"
    assert parse_env(text) == {"A": "1", "B": "2"}


def test_only_first_equals_splits() -> None:
    assert parse_env("URL=https://x.com/?a=1&b=2") == {"URL": "https://x.com/?a=1&b=2"}


def test_strip_whitespace_around_key_and_value() -> None:
    assert parse_env("  A  =  1  ") == {"A": "1"}


def test_strip_double_quotes() -> None:
    assert parse_env('A="hello"') == {"A": "hello"}


def test_strip_single_quotes() -> None:
    assert parse_env("A='hello'") == {"A": "hello"}


def test_unpaired_quote_is_kept() -> None:
    assert parse_env('A="hello') == {"A": '"hello'}


def test_empty_value() -> None:
    assert parse_env("A=") == {"A": ""}


def test_duplicate_key_last_wins() -> None:
    assert parse_env("A=1\nA=2") == {"A": "2"}


def test_line_without_equals_raises() -> None:
    with pytest.raises(ValueError):
        parse_env("A=1\n这行没有等号\nB=2")


def test_empty_key_raises() -> None:
    with pytest.raises(ValueError):
        parse_env("=1")


def test_inline_hash_is_part_of_value() -> None:
    # 今天故意不处理行内注释，保持简单；等你学到 Day 5 可以回来改进
    assert parse_env("A=v # c") == {"A": "v # c"}


def test_mask_secrets() -> None:
    assert mask_secrets({"A": "1", "B": "secret"}) == {"A": "***", "B": "***"}


def test_mask_does_not_touch_input() -> None:
    original = {"A": "1"}
    mask_secrets(original)
    assert original == {"A": "1"}  # 不能原地修改
