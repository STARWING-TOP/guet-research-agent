"""Day 3 练习：函数与参数 —— 手写重试装饰器

运行测试：uv run pytest tests/test_retry.py -q

为什么写这个：
    项目里 src/agent/llm.py 用的是 tenacity 库做重试。手写一遍之后，
    你再看 tenacity 的配置（stop_after_attempt / wait_exponential）就知道每行在干嘛。
"""

from __future__ import annotations

import functools
import time
from typing import Any, Callable


# ======================================================================
# 练习 1：retry 装饰器（今天的重点）
# ======================================================================
def retry(times: int = 3, delay: float = 0.5, backoff: float = 2.0):
    """失败重试装饰器，带指数退避。

    用法：
        @retry(times=3, delay=0.5)
        def fetch():
            ...

    要求：
    1. 最多执行 times 次（不是"重试 times 次"，是"总共 times 次"）
    2. 某次成功 → 立刻返回结果，不再重试
    3. 某次失败 → 等一会儿再试：第 1 次失败等 delay 秒，
       第 2 次失败等 delay * backoff 秒，第 3 次等 delay * backoff ** 2 秒…
    4. 最后一次（attempt == times）还失败 → 抛出**原异常**，不要包一层
    5. 必须保留原函数的 __name__ 和 __doc__（见下面 @functools.wraps 的注释）

    提示（循环骨架）：
        current_delay = delay
        for attempt in range(1, times + 1):
            try:
                ...  # 调用 func
            except Exception:
                ...  # 是最后一次吗？是 → raise；不是 → sleep 一下，delay 翻倍
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        # 这一行我已经写好，别删。
        # 原因：本项目的 tools/base.py 靠 func.__name__ 和 func.__doc__ 注册工具，
        #      装饰器不写 @wraps 会把这两个属性丢掉，工具就注册不上。
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # TODO(你): 重试循环，约 8 行
            current_delay = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


# ======================================================================
# 练习 2：把收到的参数原样转发（体会 *args / **kwargs）
# ======================================================================
def log_call(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """打印调用信息，然后把参数原样转发给 func。

    要求：
        log_call(add, 1, b=2)
        # 打印：调用 add(args=(1,), kwargs={'b': 2})
        # 返回：add(1, b=2) 的结果

    提示：
        打印：print(f"调用 {func.__name__}(args={args}, kwargs={kwargs})")
        转发：return func(*args, **kwargs)
    """
    # TODO(你): 2 行
    print(f"调用{func.__name__}(args={args}, kwargs={kwargs})")
    return func(*args, **kwargs)
    raise NotImplementedError("log_call 还没写")


# ======================================================================
# 练习 3：for ... else（循环没被 break 时才走 else）
# ======================================================================
def find_first(items: list[Any], predicate: Callable[[Any], bool]) -> Any:
    """返回第一个满足条件的元素，找不到返回 None。

    例：
        find_first([1, 2, 3], lambda x: x > 1)  -> 2
        find_first([1, 2, 3], lambda x: x > 9)  -> None

    要求：必须用 for ... else 写。

    提示：
        for item in items:
            if predicate(item):
                break          # 找到了就跳出
        else:
            return None        # 注意缩进：else 和 for 对齐，不是和 if 对齐
        return item
    """
    # TODO(你): 约 5 行
    for item in items:
        if predicate(item):
            break
    else:
        return None
    return item
