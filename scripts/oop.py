"""Day 4 练习：类与异常。

跑法：
    uv run python scripts/oop.py            # 看 demo 的【预期】输出
    uv run pytest tests/test_oop.py -q      # 只跑今天的测试
    uv run pytest -q                        # 全量：写完应该是 73 passed

你只需要填 11 个 TODO，每个 1~4 行。按 A → B → C → D 的顺序做，
每完成一组，passed 的数量会跳一次（这就是进度数字，盯着它走）：

    起点（骨架原样）                                    54 passed / 19 failed
    A 组 Chunk（类、__repr__/__str__、@property）      54 → 60 passed
    B 组 ToolError / EnvParseError（自定义异常）        60 → 66 passed
    C 组 EnvFile（封装 + 封装异常 + 缓存）              66 → 69 passed
    D 组 call_tool（try/except/else/finally）           69 → 73 passed

（骨架里已经有 7 条今天是绿的：2 条预习 + 5 条"已写好"的代码自带的测试。
 它们不是白送的，是让你先确认"环境没问题、文件存盘了、跑的是我这版"。）

两个"看起来像错误、其实不用管"的现象：
    * `uv run python scripts/oop.py` 会在打印第一行数据前停住，最后一行是
      `NotImplementedError: A2: 还没写 __repr__` —— 它就是下一步该做的事，不是环境坏了。
    * `uv run ruff check .` 会报 `parse_env 未使用` / `text 未使用` 两条 ——
      TODO 还没填所以"没用上"，你填完 C1 就自动消失。全绿后 ruff 应该 0 error。

C++ 对照（你唯一的参照系）：
    C++ 的 this                  → Python 必须显式写 self（语法要求，不是可选）
    C++ 构造函数（分配 + 初始化）  → __init__ 只做"初始化"，对象此时已经存在了
    C++ static 成员变量           → 类属性（所有实例共享同一个）
    C++ int len() const           → @property def len（访问时不加括号）
    C++ operator<< / to_string    → __str__（给用户）/ __repr__（给开发者）
    C++ throw / catch (const X&)  → raise / except X as e
    C++ throw;（重新抛出）        → raise（裸 raise，保留原始 traceback）

三条铁律（今天的自测题就考这三条，答案都写在下面的代码注释里）：
    1. __repr__ 给开发者（调试、列表、日志），__str__ 给用户（print）。
       print 一个对象 → 用 __str__；print 一个**列表** → 列表的 repr → 元素的 __repr__。
       所以只写 __str__ 的话，列表里还是一堆 <Chunk object at 0x...>。
    2. 绝不裸 except:。裸的连 KeyboardInterrupt / SystemExit（Ctrl+C、sys.exit）一起吞，
       Ctrl+C 都停不下来。except Exception: 就够用，它不接 BaseException 那两支。
    3. class A: items = [] 是**类属性**，所有实例共享同一个 list；
       要每个实例自己的，必须在 __init__ 里写 self.items = []。
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

# 复用 Day 1 写的解析器：EnvFile 只负责"读文件 + 把异常包装好"，不重复写解析逻辑
from env_parse import parse_env


# ======================================================================
# A 组：Chunk —— W4 检索层的核心数据结构
# ======================================================================
class Chunk:
    """一个文本片段：正文 + 出处 + 它在原文里的字符区间。

    W4 做 RAG 时，检索返回的就是一组 Chunk；答案末尾的 [1][2] 引用
    就是靠 source / start / end 反查回原文的。所以这四个字段一个都不能少。
    """

    def __init__(self, text: str, source: str, start: int, end: int) -> None:
        # 这条已经写好，当模板用
        if start < 0:
            raise ValueError(f"start 不能为负：{start}")

        # TODO(你·A1): 2 行 —— 校验 end 不能小于 start，抛 ValueError
        #   照上面那行写，消息格式：end({end}) 不能小于 start({start})

        # 存字段（已写好。注意每个都要带 self.，漏了 self. 就只是个局部变量，对象上什么都没有）
        self.text = text
        self.source = source
        self.start = start
        self.end = end

    # TODO(你·A2): 1 行
    def __repr__(self) -> str:
        """开发者的眼睛：调试时能看出出处、起点、正文。

        期望（tests 里是精确比对，格式别改）：
            Chunk(source='guet.md', start=0, text='你好')

        提示：
            return f"Chunk(source={self.source!r}, start={self.start}, text={self.text!r})"
            {x!r} 就是 repr(x)，会让字符串自动带上引号 —— 调试时靠这个区分
            '123'（字符串）和 123（数字）。
        """
        raise NotImplementedError("A2: 还没写 __repr__")

    # TODO(你·A3): 1 行
    def __str__(self) -> str:
        """用户的输出：只要正文，不要一堆字段名。

        期望：str(Chunk("你好", "guet.md", 0, 2)) == "你好"
        """
        raise NotImplementedError("A3: 还没写 __str__")

    # TODO(你·A4): 1 行
    @property
    def len(self) -> int:
        """片段长度。用 c.len 访问，**不加括号**（它不是方法）。

        提示：return len(self.text)

        这里有个容易想歪的点：方法体里的 len 找到的是**内置函数**，
        不是这个属性 —— 类里的名字不会自动进入方法的作用域（不像 C++ 的成员函数），
        所以不会自己调自己造成递归。C++ 里你写 this->len() 才叫成员，Python 不这样找。
        """
        raise NotImplementedError("A4: 还没写 len")

    # TODO(你·A5): 3 行
    def __eq__(self, other: object) -> bool:
        """两个 Chunk 怎样算相等？出处、起点、正文都相同才算。

        提示：
            if not isinstance(other, Chunk):
                return NotImplemented
            return (self.source, self.start, self.text) == (
                other.source, other.start, other.text,
            )

        为什么先 isinstance 再比较：别人可能拿 Chunk 和字符串比，
        直接 other.source 会 AttributeError。返回 NotImplemented 的意思是
        "我不认识这种类型，你（Python）自己决定"，比较结果最终是 False，但不会崩。

        坑：定义了 __eq__ 之后，__hash__ 会被自动设成 None，这个类就
        不能放进 set、也不能当 dict 的 key 了。真实项目要用 set 去重时得补 __hash__。
        """
        raise NotImplementedError("A5: 还没写 __eq__")


# ======================================================================
# B 组：自定义异常 —— ToolError / EnvParseError
# ======================================================================
class ToolError(Exception):
    """工具层的"可预期失败"：参数不对、文件不存在、上游接口 5xx。

    为什么要自建一个异常，而不是到处 raise ValueError？
        因为调用方要能区分两种失败：
          ValueError  -> 我代码写错了，应该崩，去看 stack trace
          ToolError   -> 环境/输入不对，可以转成一句人话交给模型，让它换个方式重试
        本项目的 src/agent/tools/base.py 正是这么干的：捕获工具异常，
        包成 {"error": "..."} 的 JSON 返回给模型，agent 主循环不会因此崩掉。
    """

    def __init__(self, message: str, tool: str = "unknown", retryable: bool = False) -> None:
        # 已写好。super().__init__ 这行不能省 —— 省了以后 e.args 是空的，
        # logging / traceback / pytest 报告里只会显示类名，看不到具体消息。
        super().__init__(message)
        self.message = message
        self.tool = tool
        self.retryable = retryable

    # TODO(你·B1): 1 行
    def __str__(self) -> str:
        """期望：
            str(ToolError("除数为 0", tool="calculator")) == "[calculator] 除数为 0"

        为什么值得重写：日志里同时出现十几种异常时，"是哪个工具炸的"是最缺的信息。

        提示：return f"[{self.tool}] {self.message}"
        """
        raise NotImplementedError("B1: 还没写 ToolError.__str__")


class EnvParseError(ToolError):
    """解析 .env 失败。

    继承 ToolError 的收益：调用方写 except ToolError 就能一把兜住
    "tool 层的一切可预期失败"，不用逐个记住子类名。这就是继承在异常体系里的用法。
    """

    # TODO(你·B2): 2 行
    def __init__(self, message: str) -> None:
        """期望：
            str(EnvParseError("第 3 行没有等号")) == "[env] 第 3 行没有等号"

        提示（2 行）：
            super().__init__(message, tool="env")
            # 这一句就是在调 ToolError.__init__，tool 固定成 "env"

        注意 super() 不能换成 ToolError.__init__ 写死 —— 以后要是中间插一层
        子类，写死的那行会绕过它；super() 是按 MRO 找的。
        """
        raise NotImplementedError("B2: 还没写 EnvParseError.__init__")


# ======================================================================
# C 组：EnvFile —— 把"读文件 + 解析 + 异常"封装成一个对象
# ======================================================================
class EnvFile:
    """一个 .env 文件：懒加载 + 解析 + 只读访问。

    Day 1 的 parse_env 是纯函数（文本进，字典出）。现在给它加一层类，
    把 path 这个状态挂到对象上，用的人就不用每次都自己读文件、自己包异常。
    这就是"类"最实际的用处：把一组数据和操作数据的方式绑在一起。
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._data: dict[str, str] | None = None
        # 下划线开头是"私有"的约定（不是语法强制，Python 没有 private）。
        # None 表示"还没读过"，这是本项目的懒加载约定：别人 new 出来不读文件也不报错。

    def load(self) -> dict[str, str]:
        """读文件并解析，结果缓存起来（第二次调用直接返回，不重复读盘）。"""
        if self._data is not None:
            return self._data  # 已经读过，直接给缓存

        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            # raise ... from e 会保留原始异常：traceback 里会多打印一段
            # "The above exception was the direct cause of the following exception"。
            # 排查时不会丢掉"到底是哪个文件没找到"的线索。这条已写好，当模板。
            raise EnvParseError(f"文件不存在：{self.path}") from e

        # TODO(你·C1): 4 行 —— 用 parse_env 解析，并把 ValueError 换成 EnvParseError
        #   照上面的模板：
        #       try:
        #           data = parse_env(text)
        #       except ValueError as e:
        #           raise EnvParseError(f"{self.path.name} 解析失败：{e}") from e
        #       self._data = data
        #       return data
        raise NotImplementedError("C1: 还没写 EnvFile.load 的解析部分")

    # TODO(你·C2): 1 行
    def to_dict(self) -> dict[str, str]:
        """返回一份**副本**，调用方随便改都不会污染对象内部。

        期望：d = e.to_dict(); d["X"] = "1" 之后，e.to_dict() 里不该出现 X

        提示：return dict(self.load())
        如果直接 return self.load()，就是把这个对象内部缓存的字典交出去 ——
        调用方一个 d.pop() 就能把你的缓存搞坏。这是封装最容易漏的一条。
        """
        raise NotImplementedError("C2: 还没写 to_dict")

    # TODO(你·C3): 1 行
    @property
    def keys(self) -> tuple[str, ...]:
        """所有 key，按文件里的原始顺序，返回不可变的元组。

        期望：e.keys == ("A", "B")，并且 e.keys 是元组不是 list
              （交出去的 list 会被调用方 append 掉，元组不会）

        提示：return tuple(self.load())
        """
        raise NotImplementedError("C3: 还没写 keys")

    def __repr__(self) -> str:
        # 已写好。注意 __repr__ 里**不读文件**：repr 可能在任何时候被调用
        # （报错、日志、调试器），在里面做 IO 会让"打印个对象"都能炸。
        return f"EnvFile({str(self.path)!r})"


# ======================================================================
# D 组：try / except / else / finally —— 分层捕获，模拟 工具的调用外壳
# ======================================================================
CALLS: list[str] = []  # 记账用的模块级列表，测试靠它验证 finally 到底跑没跑


def call_tool(func: Callable[..., Any], **kwargs: Any) -> dict[str, Any]:
    """调用一个工具函数，把结果或失败都变成字典返回（永远不向外抛）。

    这就是 src/agent/tools/base.py 里 Tool.run 的简化版。要求（顺序不能变）：

      1. try:      value = func(**kwargs)
      2. except ToolError as e:   -> {"ok": False, "error": str(e), "retryable": e.retryable}
      3. except Exception as e:   -> {"ok": False, "error": f"{type(e).__name__}: {e}",
                                       "retryable": False}
      4. else:                    -> {"ok": True, "value": value}
      5. finally:                 CALLS.append(func.__name__)

    为什么第 2 条要在第 3 条前面：except 是按顺序匹配的，ToolError 是 Exception 的子类，
    放反了就永远走不到 ToolError 那一支（C++ 的 catch 也是从上往下匹配，一个道理）。

    为什么 else 不写成 try 里的最后一句：else 只在"没抛异常"时执行，
    把正常逻辑放 else 里，try 块就只剩"可能炸的那一行"，一眼能看出保护范围。
    """
    # TODO(你·D1): 约 10 行，照上面 1~5 写
    raise NotImplementedError("D1: 还没写 call_tool")


# ----------------------------------------------------------------------
# demo 用的两个小工具（已写好，别改）
# ----------------------------------------------------------------------
def _demo_add(a: int, b: int) -> int:
    return a + b


def _demo_fail() -> None:
    raise ToolError("上游 502", tool="http", retryable=True)


# ======================================================================
# demo：跑起来对着【预期】看。前几条就崩是正常的（TODO 还没填完）
# ======================================================================
def demo() -> None:
    print("=" * 72)
    print("1) repr vs str：print 对象用 __str__，print 列表里的元素用 __repr__")
    c = Chunk("你好，世界", "guet.md", 0, 5)
    print(f"   {c!r}")  # 【预期】Chunk(source='guet.md', start=0, text='你好，世界')
    print(f"   {c}")  # 【预期】你好，世界
    print(f"   {[c]}")  # 【预期】[Chunk(source='guet.md', start=0, text='你好，世界')]
    print(f"   c.len = {c.len}")  # 【预期】   c.len = 5

    print("=" * 72)
    print("2) 校验：end 小于 start 抛 ValueError（try/except/else/finally 四个块都在）")
    try:
        Chunk("x", "guet.md", 5, 2)
    except ValueError as e:
        print(f"   抓到 ValueError: {e}")  # 【预期】抓到 ValueError: end(2) 不能小于 start(5)
    else:
        print("   没抛异常 —— 说明 A1 的校验还没写")  # 【预期】不会走到这里
    finally:
        print("   finally 永远执行（不管上面走哪条路）")  # 【预期】finally 永远执行...

    print("=" * 72)
    print("3) 自定义异常：消息里带工具名")
    try:
        raise ToolError("除数为 0", tool="calculator", retryable=True)
    except ToolError as e:
        print(f"   {e}   retryable={e.retryable}")
        # 【预期】[calculator] 除数为 0   retryable=True

    print("=" * 72)
    print("4) call_tool：把失败分成'可预期'和'真 bug'")
    CALLS.clear()
    print(f"   成功      -> {call_tool(_demo_add, a=1, b=2)}")
    # 【预期】成功      -> {'ok': True, 'value': 3}
    print(f"   ToolError -> {call_tool(_demo_fail)}")
    # 【预期】ToolError -> {'ok': False, 'error': '[http] 上游 502', 'retryable': True}
    print(f"   记账 CALLS = {CALLS}")  # 【预期】记账 CALLS = ['_demo_add', '_demo_fail']


# ======================================================================
# 收工前的自测题（能不看上面的注释答出来，今天就算过）
#   1. print(c) 和 print([c]) 分别调用了哪个方法？只写 __str__ 会怎样？
#   2. 为什么裸 except: 危险？except Exception: 为什么就够了？什么东西它接不住？
#   3. class A: items = [] 和 def __init__(self): self.items = [] 差在哪？
#      （tests/test_oop.py 开头有两个现成的对比例子，跑一下看结果）
# ======================================================================


if __name__ == "__main__":
    demo()
    sys.exit(0)
