"""Day 3 练习的测试。跑法：uv run pytest tests/test_retry.py -q

注意：这里的测试都有一个"计数器"，用来确认函数到底被调用了几次——
      这是测"重试次数对不对"的标准做法。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from retry import find_first, log_call, retry  # noqa: E402


# ---------------------------------------------------------------- retry
def test_retry_returns_immediately_on_success() -> None:
    calls = {"n": 0}

    @retry(times=3, delay=0.01)
    def ok() -> str:
        calls["n"] += 1
        return "ok"

    assert ok() == "ok"
    assert calls["n"] == 1          # 一次就成功，不该重试


def test_retry_succeeds_on_third_attempt() -> None:
    calls = {"n": 0}

    @retry(times=3, delay=0.01)
    def flaky() -> str:
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("还没好")
        return "终于成功了"

    assert flaky() == "终于成功了"
    assert calls["n"] == 3


def test_retry_raises_after_all_attempts() -> None:
    calls = {"n": 0}

    @retry(times=3, delay=0.01)
    def always_fail() -> None:
        calls["n"] += 1
        raise ValueError("永远失败")

    with pytest.raises(ValueError):     # 必须是原来的异常类型
        always_fail()
    assert calls["n"] == 3              # 总共试了 3 次


def test_retry_passes_arguments_through() -> None:
    @retry(times=2, delay=0.01)
    def add(a: int, b: int = 0) -> int:
        return a + b

    assert add(1, b=2) == 3


def test_retry_keeps_name_and_doc() -> None:
    @retry(times=2, delay=0.01)
    def documented() -> int:
        """我的文档字符串"""
        return 1

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "我的文档字符串"


# ---------------------------------------------------------------- log_call
def test_log_call_forwards_positional_and_keyword() -> None:
    def add(a: int, b: int = 0) -> int:
        return a + b

    assert log_call(add, 1, b=2) == 3


def test_log_call_prints(capsys: pytest.CaptureFixture[str]) -> None:
    def add(a: int, b: int = 0) -> int:
        return a + b

    log_call(add, 1, b=2)
    out = capsys.readouterr().out
    assert "add" in out
    assert "(1,)" in out
    assert "'b': 2" in out


# ---------------------------------------------------------------- find_first
def test_find_first_found() -> None:
    assert find_first([1, 2, 3], lambda x: x > 1) == 2


def test_find_first_not_found() -> None:
    assert find_first([1, 2, 3], lambda x: x > 9) is None


def test_find_first_empty() -> None:
    assert find_first([], lambda x: True) is None
