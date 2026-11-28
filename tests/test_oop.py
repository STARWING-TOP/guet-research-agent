"""Day 4 练习的测试。跑法：uv run pytest tests/test_oop.py -q

建议顺序：从下往上不好使，今天要**从上往下**做：
    最上面两条【预习】现在就是绿的，先读懂它们（那条 bug 你以后一定会遇到）；
    然后 A → B → C → D，每做完一组 passed 就会跳一次。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from oop import CALLS, Chunk, EnvFile, EnvParseError, ToolError, call_tool  # noqa: E402

# ======================================================================
# 【预习】下面两条现在就是绿的，不是你的 TODO。
# 它们演示的是"可变类属性"那个 Python 最经典的 bug —— 多花两分钟看懂，
# 比记住语法有用得多（面试也真会问）。
# ======================================================================


class _TrapBag:
    """反例：items 写在类体里 = 类属性 ≈ C++ 的 static 成员，所有实例共享一个 list。"""

    items: list[str] = []

    def add(self, x: str) -> None:
        self.items.append(x)


class _FixedBag:
    """正例：items 在 __init__ 里创建，每个实例一个，互不干扰。"""

    def __init__(self) -> None:
        self.items: list[str] = []

    def add(self, x: str) -> None:
        self.items.append(x)


def test_class_attribute_is_shared_bug() -> None:
    a, b = _TrapBag(), _TrapBag()
    a.add("x")
    assert b.items == ["x"]  # b 一次都没 add 过，却也有 "x" —— 这就是那个 bug
    assert a.items is b.items  # is 为真：根本是同一个 list


def test_instance_attribute_is_per_object() -> None:
    a, b = _FixedBag(), _FixedBag()
    a.add("x")
    assert b.items == []
    assert a.items is not b.items


# ======================================================================
# A 组：Chunk
# ======================================================================
def test_chunk_stores_fields() -> None:
    c = Chunk("你好", "guet.md", 0, 2)
    assert c.text == "你好"
    assert c.source == "guet.md"
    assert c.start == 0
    assert c.end == 2


def test_chunk_len_property() -> None:
    assert isinstance(Chunk.len, property), "len 必须是 @property，不能是普通方法"
    c = Chunk("中文abc", "doc.md", 3, 8)
    assert c.len == 5
    assert c.len == len(c.text)


def test_chunk_repr() -> None:
    c = Chunk("你好", "guet.md", 0, 2)
    assert repr(c) == "Chunk(source='guet.md', start=0, text='你好')"


def test_chunk_str() -> None:
    c = Chunk("你好，世界", "guet.md", 0, 5)
    assert str(c) == "你好，世界"


def test_print_object_uses_str_but_print_list_uses_repr(
    capsys: pytest.CaptureFixture[str],
) -> None:
    c = Chunk("你好", "guet.md", 0, 2)
    print(c)  # 对象本身 -> __str__
    print([c])  # 列表 -> 列表的 repr -> 元素的 __repr__
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "你好"
    assert out[1] == "[Chunk(source='guet.md', start=0, text='你好')]"


def test_chunk_rejects_negative_start() -> None:
    with pytest.raises(ValueError):
        Chunk("x", "guet.md", -1, 0)


def test_chunk_rejects_end_before_start() -> None:
    with pytest.raises(ValueError) as ei:
        Chunk("x", "guet.md", 5, 2)
    assert "end" in str(ei.value) and "start" in str(ei.value)


def test_chunk_eq() -> None:
    a = Chunk("你好", "guet.md", 0, 2)
    b = Chunk("你好", "guet.md", 0, 2)
    other_source = Chunk("你好", "other.md", 0, 2)
    assert a == b
    assert a != other_source
    assert a != "你好"  # 和别的类型比不能崩，结果应是"不相等"


# ======================================================================
# B 组：ToolError / EnvParseError
# ======================================================================
def test_toolerror_fields_and_defaults() -> None:
    e = ToolError("出事了")
    assert e.message == "出事了"
    assert e.tool == "unknown"
    assert e.retryable is False

    e2 = ToolError("除数为 0", tool="calculator", retryable=True)
    assert e2.retryable is True


def test_toolerror_str_has_tool_name() -> None:
    assert str(ToolError("除数为 0", tool="calculator")) == "[calculator] 除数为 0"


def test_envparseerror_is_a_toolerror() -> None:
    e = EnvParseError("坏行")
    assert isinstance(e, ToolError)
    assert isinstance(e, Exception)


def test_envparseerror_default_tool_is_env() -> None:
    assert str(EnvParseError("第 3 行没有等号")) == "[env] 第 3 行没有等号"


# ======================================================================
# C 组：EnvFile
# ======================================================================
def _write_env(tmp_path: Path, body: str) -> Path:
    p = tmp_path / ".env"
    p.write_text(body, encoding="utf-8")
    return p


def test_envfile_parses(tmp_path: Path) -> None:
    p = _write_env(tmp_path, "# 注释\nA=1\nB=hello\n")
    assert EnvFile(p).to_dict() == {"A": "1", "B": "hello"}


def test_envfile_construct_does_not_touch_disk(tmp_path: Path) -> None:
    p = tmp_path / "nope.env"
    e = EnvFile(p)  # 构造时不该读文件，所以不该抛异常
    assert isinstance(e, EnvFile)


def test_envfile_missing_file_raises_toolerror(tmp_path: Path) -> None:
    e = EnvFile(tmp_path / "nope.env")
    with pytest.raises(ToolError) as ei:
        e.load()
    assert isinstance(ei.value, EnvParseError)
    assert "不存在" in str(ei.value)


def test_envfile_bad_line_raises_envparseerror(tmp_path: Path) -> None:
    p = _write_env(tmp_path, "GOOD=1\n这行没有等号\n")
    with pytest.raises(EnvParseError) as ei:
        EnvFile(p).load()
    assert "解析失败" in str(ei.value)
    assert ei.value.__cause__ is not None, "要用 raise ... from e 保留原始异常"


def test_envfile_to_dict_returns_copy(tmp_path: Path) -> None:
    p = _write_env(tmp_path, "A=1\n")
    e = EnvFile(p)
    d = e.to_dict()
    d["HACKED"] = "1"
    assert "HACKED" not in e.to_dict()  # 改副本不能影响对象内部


def test_envfile_keys_is_property(tmp_path: Path) -> None:
    assert isinstance(EnvFile.keys, property), "keys 必须是 @property"
    p = _write_env(tmp_path, "A=1\nB=2\n")
    e = EnvFile(p)
    assert e.keys == ("A", "B")  # 元组：有顺序、不可变
    assert isinstance(e.keys, tuple)


def test_envfile_caches_parsed_result(tmp_path: Path) -> None:
    p = _write_env(tmp_path, "A=1\n")
    e = EnvFile(p)
    assert e.load() is e.load(), "第二次应该拿到同一份缓存，不该重新解析"


def test_envfile_repr(tmp_path: Path) -> None:
    p = tmp_path / "nope.env"
    assert repr(EnvFile(p)) == f"EnvFile({str(p)!r})"


# ======================================================================
# D 组：call_tool（try / except / else / finally）
# ======================================================================
def _add(a: int, b: int) -> int:
    return a + b


def _fails_predictably() -> int:
    raise ToolError("除数为 0", tool="calculator", retryable=True)


def _has_bug() -> int:
    return 1 // 0


def _interrupted() -> int:
    raise KeyboardInterrupt


def test_call_tool_success() -> None:
    CALLS.clear()
    assert call_tool(_add, a=1, b=2) == {"ok": True, "value": 3}
    assert CALLS == ["_add"]  # finally 在成功路径上也执行


def test_call_tool_toolerror_is_retryable() -> None:
    CALLS.clear()
    r = call_tool(_fails_predictably)
    assert r["ok"] is False
    assert r["retryable"] is True
    assert "除数为 0" in r["error"]
    assert CALLS == ["_fails_predictably"]  # 失败路径同样记账


def test_call_tool_unexpected_error_is_not_retryable() -> None:
    CALLS.clear()
    r = call_tool(_has_bug)
    assert r["ok"] is False
    assert r["retryable"] is False
    assert r["error"].startswith("ZeroDivisionError:")  # 真 bug 要留下类型名


def test_call_tool_does_not_swallow_ctrl_c() -> None:
    CALLS.clear()
    with pytest.raises(KeyboardInterrupt):  # except Exception 接不住它，所以能传出去
        call_tool(_interrupted)
    assert CALLS == ["_interrupted"]  # finally 仍然执行了
