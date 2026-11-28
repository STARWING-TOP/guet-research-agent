# 前四天复盘（Day 1–4）·「学」清单 vs 实际代码

> 生成：2026-11-28 20:40 · 数据来源：`docs/week1.md` 的「学」清单 + 仓库真实代码 + `git log`
> 用途：① 查"学了但没落地"的缺口 ② 面试前复习这几页比翻文档快

---

## 0. 判定口径

| 标记 | 含义 |
|---|---|
| ✅ | 在 `scripts/` 或 `src/` 的**产品代码**里真的写过，并且测试跑通过 |
| 🟡 | 只在 `tests/` 或 playground 里出现过（看得懂、能改，但没在项目里主动用过） |
| ❌ | 全仓库 0 次，只停留在"读过教程" |

次数统计包含 `tests/`，所以 🟡 要额外看它到底在哪儿。

---

## 1. 每天真正交付并推送了什么

| Day | commit | 新增/改动 | 交付的功能 | 当天测试 | 已推送 |
|---|---|---|---|---|---|
| 1 | `40279a4` | `scripts/env_parse.py`（+53/−3） | `parse_env()` 解析 .env、`mask_secrets()` 脱敏、`main()` 带 `--path/--mask/--json` | 15 | ✅ |
| 2 | `b1bd1d6` | `scripts/chunk.py`（+12/−6） | `chunk_text()` 定长重叠分块、`top_chars()` 词频、3 个切片函数 | 15 | ✅ |
| 3 | `1b3db35` | `scripts/retry.py` + `tests/test_retry.py`（+220） | `retry()` 装饰器（指数退避 + 原异常透传）、`log_call()`、`find_first()` | 10 | ✅ |
| 4 | `158761a` | `scripts/oop.py`（+33/−20） | `Chunk` / `ToolError` / `EnvParseError` / `EnvFile` / `call_tool` | 26 | ✅ |

**累计 73 passed，ruff 0 error，main 与 origin 同步。**

注意每一行的性质：Day 1–2 是**纯函数**，Day 3 开始出现**装饰器（高阶函数）**，Day 4 是**对象 + 异常体系**。这条线正好是 W2 之后所有代码的三种基本形状。

---

## 2. 逐条核对：「学」里写了什么 → 代码里有没有

### Day 1 · 字符串与数字

| 学到的点 | 代码里的位置 | 次数 | 判定 |
|---|---|---|---|
| 变量无类型声明；`type()` / `isinstance()` | `src/agent/tools/builtin.py` 的 `_eval_node()` 全用 `isinstance` 分流 | 15 | ✅ |
| f-string | 全仓到处都是 | 大量 | ✅ |
| `.strip()` / `.split(k, 1)` / `.join()` / `.replace()` / `.startswith()` | `env_parse.py:66` `line.split("=", 1)`、`line.startswith("#")` | 9 / 3 / 2 / 3 | ✅ |
| `int` 无溢出、`/` 恒 float、`//` 整除、`**` 幂 | `builtin.py` 的 `_BIN_OPS`（`operator.floordiv` / `pow`） | — | ✅ |
| `None` / `0` / `""` / `[]` 的区别 | `env_parse.py` 用 `if not line` 同时挡空串和空行 | — | ✅ |
| 坑：`split("=")` 会把 `URL=a=b` 切碎 | 你直接写成了 `split("=", 1)`，**没踩这个坑** | 3 | ✅ |

**Day 1 是四天里落地率最高的一天。**

### Day 2 · 容器与切片

| 学到的点 | 代码里的位置 | 次数 | 判定 |
|---|---|---|---|
| `list.append` | `chunk.py` 的 `chunks.append(piece)` | ✅ | ✅ |
| `extend / insert / remove / pop / index` | — | 0 | ❌ |
| `dict` 的 `d[k]` vs `.get(k, default)` | `tools/base.py` `REGISTRY.get(name)` | 5 | ✅ |
| `setdefault` | — | 0 | ❌ |
| `set` 去重、交集/并集/差集、O(1) 成员判断 | — | 0 | ❌ **完全没碰** |
| `.items()` | 少量 | 1 | 🟡 |
| `Counter` | `chunk.py` 的 `top_chars` | ✅ | ✅ |
| 切片 `[a:b]` / `[::-1]` / `[::2]` | `chunk.py`：`trim_ends` 用 `s[n:-n]`、`odd_chars` 用 `s[::2]`、`reverse_str` 用 `s[: : -1]` | 各 1 | ✅ |
| 引用语义 `b = a` / `copy()` / `deepcopy()` | 引用语义只在 `tests/test_oop.py` 用 `is` 验证过；`deepcopy` | 0 | 🟡 |
| 坑：遍历 dict 时增删 → `RuntimeError` | — | 0 | ❌ |

### Day 3 · 函数与参数

| 学到的点 | 代码里的位置 | 次数 | 判定 |
|---|---|---|---|
| 多返回值其实是 tuple（解包） | `key, value = line.split("=", 1)` | ✅ | ✅ |
| 位置 / 关键字 / 默认参数 | `retry(times=3, delay=0.5, backoff=2.0)` | ✅ | ✅ |
| `*args` / `**kwargs` / `f(*a, **kw)` | `retry.wrapper(*args, **kwargs)`、`log_call` | 6 / 10 | ✅ |
| 默认参数只在定义时求值一次 | 只背了结论，**没写过可变默认参数的反例** | 0 | ❌ |
| 作用域 `global` / `nonlocal` | — | 0 | ❌ **完全没碰** |
| 闭包 | `retry` 里 `current_delay` 被 `wrapper` 捕获 —— 你写过，但 handoff 里写着"概念模糊" | 1 | 🟡 |
| `functools.wraps` | `retry.py:49` | 3 | ✅ |
| `for ... else` | `retry.py` 的 `find_first` | ✅ | ✅ |

### Day 4 · 类与异常

| 学到的点 | 代码里的位置 | 次数 | 判定 |
|---|---|---|---|
| `self` 必写；`__init__` 只初始化 | `Chunk.__init__` / `EnvFile.__init__` | ✅ | ✅ |
| 类属性 vs 实例属性 | 只在 `tests/test_oop.py` 的 `_TrapBag` / `_FixedBag` 演示过 | 🟡 | 🟡 |
| `@property` | `Chunk.len`、`EnvFile.keys` | 7 | ✅ |
| `__repr__` vs `__str__` | `Chunk` 各一份，测试里比对过 | 10 / 11 | ✅ |
| `__eq__` 与 `NotImplemented` | `Chunk.__eq__` | 2 | ✅ |
| 继承 + `super()` | `EnvParseError(ToolError)` | 6 | ✅ |
| 访问限制（`_data` 私有约定） | `EnvFile._data` | ✅ | ✅ |
| `try/except/else/finally` | `call_tool`（四个块齐全） | ✅ | ✅ |
| 自定义异常 + `raise ... from e` | `EnvParseError` 两处包装 | 5 | ✅ |
| 绝不裸 `except` | `tools/base.py` 用 `except Exception as e:  # noqa: BLE001` | ✅ | ✅ |

---

## 3. 六个真实缺口（按"面试会不会问"排序）

| # | 缺口 | 为什么现在必须补 |
|---|---|---|
| 1 | **`set`**（去重 / 交并差 / O(1) 成员判断） | 面试高频："怎么给列表去重？""两个集合求交集"。W4 给 chunk 去重、给 source 去重都会用。**10 分钟能补** |
| 2 | **`global` / `nonlocal`** | 这是"装饰器为什么能记住状态""闭包怎么改外层变量"的答案。你 handoff 里自己写着**闭包概念模糊**，根子就在这里 |
| 3 | **`deepcopy` / 深浅拷贝** | W2 写 ReAct 时 `messages` 列表要回溯、要复制；复制错了会污染历史上下文。测试里只用 `is` 验证过引用，没写过真拷贝场景 |
| 4 | **可变默认参数陷阱** | 只背了结论没写过反例。面试官常让"解释一下 `def f(x, acc=[])`"——背结论和能写出复现代码，是两种说服力 |
| 5 | **`setdefault` / `.items()` / 遍历中增删** | 数据聚合的日常写法，目前全靠 `Counter` 替代；W4 统计语料时会撞上 |
| 6 | **`list.extend / insert / remove / pop / index`** | `append` 之外的 5 个方法没练。W2 的 `messages` 要 `pop/insert/extend`，W4 的 chunk 列表要 `extend` |

**缺口的共同点**：都不是"没学过"，而是"没写过"。看一遍教程 + 写 5 行代码，这六个能一起补掉，成本 45 分钟。

---

## 4. 怎么补（不单独开一天）

| 时机 | 动作 | 成本 |
|---|---|---|
| Day 5 顺手 | `iter_chunks` 用 `extend` 拼结果；`top_k` 用 `sorted(key=lambda)`（本来就是 Day 5 内容） | 0（融入当天练习） |
| Day 5 收工前 | 写 `playground/topics/t09_gaps.py`：set 去重 / nonlocal 计数器 / 可变默认参数反例，三个各 5 行 | 15 min |
| Day 6 收工前 | 在 `repo_stats.py` 里用 `set` 收集后缀、用 `setdefault` 建 `dict[str, list[str]]` | 15 min |
| W2 第一天（asyncio 之前） | 写一个"`messages` 列表回溯"小 demo：`deepcopy` 快照 + `pop` 回退 + `extend` 追加 | 15 min |

---

## 5. 一句话结论

> 四天交付的都是**能跑、带测试、已推送**的真代码（73 passed），这比大多数"看完教程就算学过"的人强很多。
> 但「学」清单里大约 **20% 只停留在"读懂"**，其中 3 个（`set` / `nonlocal` / `deepcopy`）在 W2–W4 会被真的用到。
> 补它们只要 45 分钟——趁现在补，别留到面试前。
