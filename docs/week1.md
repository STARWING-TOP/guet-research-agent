# 第一周详细清单（Day 1–6 · 11/25–11/30）

> 本周唯一目标：**把 Python 当成一门你能随手用的工具语言**，而不是"学过"。
> 六天之后你应该能：不看资料写出 `.env` 解析、文本切块、手写重试、300 行 CLI 工具。

## 每天的时间块

| 时段 | 时长 | 做什么 |
|---|---|---|
| 读 | 40 min | 只看当天列出的章节，**不要**顺手点开别的 |
| 写 | 90 min | 只做当天列出的练习，做完就停 |
| 记 | 20 min | `docs/notes.md` 写 3 条：收获 / 没懂 / 与 C++ 的差异 |

> 卡超过 30 分钟：把报错原文粘进 `docs/notes.md`，先跳过。第二天回头补，比硬磕划算。

---

## Day 1 · 变量、字符串、数字（11/25 三）

**读**：廖雪峰教程「数据类型和变量」「字符串和编码」

**学**
- 变量无类型声明；`type()` / `isinstance()`
- 字符串：`f"{x}"`、`.strip()`、`.split()`、`.split(k, 1)`、`.join()`、`.replace()`、`.startswith()`
- 数字：`int` 无溢出、`/` 恒返回 float、`//` 整除、`**` 幂
- `None` / `0` / `""` / `[]` 四者的区别（C++ 里 `nullptr` 只有一个）

**写**
1. `scripts/env_parse.py`：实现
   ```python
   def parse_env(text: str) -> dict[str, str]: ...
   ```
   规则：跳过 `#` 注释行与空行；按**第一个** `=` 切分；值两侧空白和成对引号要去掉；值里包含 `=` 的（如 `URL=a=b`）必须正确处理。
2. 用 `pathlib` 读项目里的 `.env.example`，打印解析结果。
3. 加一个 `--mask` 参数：打印时把 key 值替换成 `***`（以后调试真实 `.env` 用得上）。

**自测**（不看资料）
- `"a=1\nb=2"` → `{"a": "1", "b": "2"}`
- 说出 `"5"`、`5`、`5.0` 的类型，以及 `"5" + 5` 会怎样
- 为什么 `if x:` 不能用来判断 `x` 是不是 `0`

**坑**：`text.split("=")` 会把 `URL=a=b` 切成三份 → 用 `split("=", 1)`。

**commit**：`day1: 字符串处理 + .env 解析器`

---

## Day 2 · 容器与切片（11/26 四）

**读**：廖雪峰教程「使用 list 和 tuple」「使用 dict 和 set」

**学**
- `list`：`append/extend/insert/remove/pop/index`
- `dict`：`d[k]` vs `d.get(k, default)`、`setdefault`、`.items()`
- `set`：去重、`& | -`、成员判断 O(1)
- 切片：`a[1:3]`、`a[::-1]`、`a[::2]` —— **C++ 没有，必须练到肌肉记忆**
- **引用语义**：`b = a` 不复制；`copy()` 是浅拷贝；`deepcopy()` 才是深拷贝

**写**
1. 统计 `.env.example` 里所有 key 的字符出现频率，输出 top 5。
2. `scripts/chunk.py`：实现
   ```python
   def chunk_text(text: str, size: int, overlap: int) -> list[str]: ...
   ```
   —— 这就是 W4 检索要用的分块函数，先写朴素版，W4 再优化。
3. 用切片实现：字符串反转、取奇数位、去掉首尾各 3 个字符。

**自测**
- `a=[1,2]; b=a; b.append(3)` 之后 `a` 是什么？为什么？
- `def f(x, acc=[])` 有什么问题？
- `d["k"]` 和 `d.get("k")` 在 key 不存在时分别怎样？

**坑**：遍历 dict 的同时增删 key 会抛 `RuntimeError` → 先 `list(d.items())`。

**commit**：`day2: 容器与切片 + 文本分块`

---

## Day 3 · 函数与参数（11/27 五）

**读**：廖雪峰教程「定义函数」「函数的参数」（递归跳过）

**学**
- 多返回值其实是 tuple
- 位置参数 / 关键字参数 / 默认参数
- `*args`（tuple）、`**kwargs`（dict）、参数解包 `f(*a, **kw)`
- **默认参数只在定义时求值一次** —— Day 2 自测题的答案
- 作用域：`global` / `nonlocal`

**写**
1. `scripts/retry.py`：手写装饰器
   ```python
   def retry(times=3, delay=0.5, backoff=2.0): ...
   ```
   失败重试、指数退避、最后一次仍失败则抛出原异常。**故意让它失败**（传一个必抛异常的函数）来验证。
2. 写一个日志函数，同时接受 `*args` 和 `**kwargs` 并转发（体会 `f(*a, **kw)`）。
3. 用 `for ... else` 写"查找第一个满足条件的元素，找不到返回 None"。

**自测**
- 写一个函数，把收到的 `*args/**kwargs` 原样转发给另一个函数
- 解释为什么 `def f(x, acc=[])` 第二次调用时 `acc` 不是空的
- `retry` 里为什么要用 `functools.wraps`

**坑**：装饰器返回的 `wrapper` 不写 `@wraps(func)` 会丢函数名和 docstring —— 而本项目 `tools/base.py` **正是靠 `func.__name__` 和 `func.__doc__` 注册工具的**，丢了就注册失败。

**commit**：`day3: 函数参数 + 手写 retry 装饰器`

---

## Day 4 · 类与异常（11/28 六）

**读**：廖雪峰教程「类和实例」「访问限制」「继承和多态」「错误处理」

**学**
- `self` 必须显式写；`__init__` 不是构造函数而是初始化器
- 类属性 vs 实例属性（踩坑高发区）
- `@property` 做只读/计算属性
- `__repr__`（给开发者看）vs `__str__`（给用户看）
- `try/except/else/finally`、`raise`、自定义异常
- 绝不裸 `except:`；捕获具体类型

**写**
1. `class Chunk`：`text / source / start / end` 四个字段 + `__repr__`，再加一个 `len` 属性。
2. `class ToolError(Exception)`，在 Day 1 的 `parse_env` 里，遇到既非注释也非 `KEY=VALUE` 的行时抛出。
3. `class EnvFile`：封装读取 + 解析 + `to_dict()`，用 `@property` 暴露 `keys`。

**自测**
- `__repr__` 和 `__str__` 分别在什么时候被调用？print 一个列表里的对象会调用哪个？
- 为什么 `except:` 是危险的？`except Exception:` 够不够？
- `class A: items = []` 和 `def __init__(self): self.items = []` 的区别？

**坑**：可变类属性被所有实例共享 —— 这是 Python 最经典的 bug 之一。

**commit**：`day4: 类封装 + 自定义异常`

---

## Day 5 · 推导式、生成器、排序（11/29 日）

**读**：廖雪峰教程「切片」「迭代」「列表生成式」「生成器」「sorted」

**学**
- 列表/字典/集合推导式，带 `if` 过滤
- `enumerate`、`zip`、`any/all`、`sum(..., key=)`
- `sorted(key=lambda)`、多级排序 `key=lambda x: (-x.score, x.id)`
- 生成器：`yield`、惰性求值、`itertools.islice`

**写**
1. `scripts/topk.py`：`top_k(texts: list[str], k: int) -> list[tuple[str, int]]`，用 `collections.Counter`。
2. `read_lines(path)` 用生成器逐行 yield，**内存 O(1)**；用 10 万行假数据验证内存不涨。
3. 把 Day 2 的 `chunk_text` 改写成生成器版本 `iter_chunks(...)`，对比内存占用。
4. 给一组 `Chunk` 对象做多级排序：先按来源，再按长度降序。

**自测**
- 生成器表达式 `(x*2 for x in a)` 和列表推导 `[x*2 for x in a]` 的区别
- 生成器为什么只能迭代一次？
- `sorted(key=lambda x: -x)` 和 `reverse=True` 有什么区别

**坑**：生成器被 `sum()` 消费后再遍历就是空的 —— W4 处理语料时会反复踩。

**commit**：`day5: 推导式/生成器/多级排序`

---

## Day 6 · 模块、包、uv、CLI 工具（11/30 一）

**读**：廖雪峰教程「模块」；`argparse`、`pathlib`、`json` 官方文档（各 15 分钟，只看你要用的部分）

**学**
- `import` 机制、绝对导入 vs 相对导入
- `__init__.py` 的作用（**本项目 `tools/__init__.py` 就是"导入即注册"的入口**）
- `if __name__ == "__main__":` 防的是什么
- `uv init/add/run/sync` 与 `pyproject.toml` 的关系
- `pathlib.Path` 替代字符串拼路径

**写（今天的大头，120 行）**
`scripts/repo_stats.py`：

```
uv run python scripts/repo_stats.py --path . --top 5
uv run python scripts/repo_stats.py --path . --json
```

要求：
1. 遍历目录，跳过 `.venv`、`.git`、`__pycache__`
2. 按后缀统计：文件数、总字节、最大文件
3. `--top N` 控制显示前 N 类
4. `--json` 输出机器可读格式
5. 用 `argparse` / `pathlib` / `json` / `Counter`，**不用任何第三方库**
6. 加 `--exclude` 参数支持自定义排除目录

**自测**
- `uv run python -m agent.cli --tool` 为什么能跑？`-m` 做了什么？
- `uv run` 和直接用 `.venv\Scripts\python.exe` 有什么区别？
- `sys.path` 是什么？为什么 `import agent` 能找到 `src/agent`？

**验收**：`uv run python scripts/repo_stats.py --top 5` 输出的是**本项目真实数据**（`.py` 文件数、总行数）。

**commit**：`day6: 120 行 CLI 工具 repo_stats`

> 为什么从 300 行降到 120 行：300 行的边际收益很低，省下的 2 小时给 W2 的 asyncio
> （那是面试必问、也是本项目 agent 循环的地基）。细节见 `docs/roadmap.md`。

---

## 本周验收（11/30 晚）

- [ ] 6 个 commit，日期连续
- [ ] 不看资料，20 分钟内写出 `parse_env` + `chunk_text` + `retry`
- [ ] `uv run pytest -q` 仍然全绿
- [ ] `docs/notes.md` 有 18 条笔记（6 天 × 3 条，**现在它就是"面试问答卡"库**，见 `docs/roadmap.md`）
- [ ] Day 4 起，每个练习**自己补 2 条测试**（不再是"别人写测试我变绿"）
- [ ] 能解释：`b = a` 是引用、默认参数只求值一次、生成器只能迭代一次、`@wraps` 为什么重要

**任何一条没做到**：周日不要开始 Day 7，先补。Day 7 的装饰器 + pydantic 是 W3 的地基。

## 卡住时怎么问

把这三样贴过来，我能一次定位：

```
1. 我想做什么：
2. 我写了什么（完整文件，不要截图）：
3. 报错原文（完整 traceback，最后一行最关键）：
```
