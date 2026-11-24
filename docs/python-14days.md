# Python 14 天速通（W1–W2）

> 面向**有 C/C++ 基础、零 Python 经验**的人。每天 2.5–3 小时，只学 agent 开发真正会用到的部分。
> 目标不是"学完 Python"，而是 **14 天后能独立读写这个项目里的每一行代码**。

## 怎么用

- 每天节奏：**读 40 分钟 → 写 90 分钟 → 记 3 条笔记 20 分钟**
- 打勾规则：只有「自测」那行**不看任何资料**能完成，才算过
- 卡住超过 30 分钟：记进 `docs/notes.md`，先跳过，第二天回头补
- 每天结束必须 `git commit` 一次，信息写清楚今天做了什么

## 日期对照

| Day | 日期 | Day | 日期 |
|---|---|---|---|
| 1 | 11/25 三 | 8 | 12/02 三 |
| 2 | 11/26 四 | 9 | 12/03 四 |
| 3 | 11/27 五 | 10 | 12/04 五 |
| 4 | 11/28 六 | 11 | 12/05 六 |
| 5 | 11/29 日 | 12 | 12/06 日 |
| 6 | 11/30 一 | 13 | 12/07 一 |
| 7 | 12/01 二 | 14 | 12/08 二 |

---

## Day 1 · 变量、字符串、数字

- [ ] 安装确认：`uv run python -c "import sys; print(sys.version)"`
- [ ] 变量无需声明类型；`type()`、`isinstance()`
- [ ] 字符串：单双引号等价、`f"{x}"`、`.strip()/.split()/.join()/.replace()/.startswith()`
- [ ] 数字：`int` 无溢出、`/` 永远返回 float、`//` 整除、`**` 幂
- [ ] `None` 不等于 `0`、`""`、`[]`（和 C++ 的 `nullptr` 对比）
- [ ] 练习：读一个 `.env` 文件，解析成 `dict`，把 `KEY=VALUE` 里的注释行跳过
- [ ] **自测**：不用查资料，写出把 `"a=1\nb=2"` 变成 `{"a": "1", "b": "2"}` 的代码

## Day 2 · 容器与切片

- [ ] `list`：`append/extend/insert/remove/pop/index`
- [ ] `dict`：`d[k]` vs `d.get(k, default)`、`setdefault`、`.items()/.keys()/.values()`
- [ ] `set`：去重、`& | -`、判断成员 O(1)
- [ ] `tuple`：不可变、可作 dict 的 key
- [ ] 切片：`a[1:3]`、`a[::-1]`、`a[::2]`（C++ 没有，重点练）
- [ ] 可变 vs 不可变；**`a = b` 是引用不是拷贝**，`copy()` / `deepcopy()`
- [ ] 练习：统计一段中文文本里每个字出现的次数，输出 top 10
- [ ] **自测**：解释为什么 `def f(x, acc=[])` 是坑

## Day 3 · 控制流、函数、参数

- [ ] `for/while`、`break/continue`、`for...else`（少见但会考）
- [ ] 函数定义、返回值、多返回值（其实是 tuple）
- [ ] 默认参数、关键字参数、`*args`、`**kwargs`
- [ ] 作用域：`global` / `nonlocal`（对照 C++ 的静态变量）
- [ ] 可变对象作默认参数的坑（Day 2 自测题的答案）
- [ ] 练习：写 `parse_args` 风格的函数，接受任意关键字参数并打印
- [ ] **自测**：写出一个接受 `*args` 和 `**kwargs` 并原样转发的函数

## Day 4 · 类与异常

- [ ] `class`、`__init__`、`self`（对照 C++ 的 `this`，但必须显式写）
- [ ] 类属性 vs 实例属性、`@property`、`@staticmethod` / `@classmethod`
- [ ] 继承、`super()`、`__repr__` vs `__str__`
- [ ] 异常：`try/except/else/finally`、`raise`、自定义异常
- [ ] **不要**用裸 `except:`；捕获具体类型
- [ ] 练习：写一个 `Document` 类，有 `text`、`chunks()` 方法，参数非法时抛自定义异常
- [ ] **自测**：说明 `__repr__` 和 `__str__` 分别什么时候被调用

## Day 5 · 推导式、迭代器、生成器

- [ ] 列表/字典/集合推导式，带 `if` 过滤
- [ ] `enumerate`、`zip`、`any/all`、`sum/min/max(..., key=...)`
- [ ] `sorted(key=lambda)`、多级排序 `key=lambda x: (-x[1], x[0])`
- [ ] 迭代器协议：`__iter__` / `__next__`、`StopIteration`
- [ ] 生成器：`yield`、惰性求值、`itertools.islice`
- [ ] 练习：用生成器实现"按行读大文件"，内存不爆
- [ ] **自测**：把 `[x*2 for x in a if x > 0]` 改写成生成器表达式，并说明差别

## Day 6 · 模块、包、工程化工具

- [ ] 模块与 `import`：绝对导入 vs 相对导入
- [ ] 包：`__init__.py` 的作用（本项目 `agent/tools/__init__.py` 就是注册入口）
- [ ] `if __name__ == "__main__":` 到底在防什么
- [ ] `uv init / add / run / sync`、`pyproject.toml` 各字段含义
- [ ] `pathlib`（别再用字符串拼路径）、`argparse`、`json`
- [ ] **综合练习（今天的大头）**：写一个 300 行的 CLI 小工具
      —— 遍历目录、按后缀统计文件大小、输出 JSON 报告、支持 `--top N` 参数
- [ ] **自测**：`uv run python -m agent.cli --tool` 为什么能跑？`-m` 做了什么？

## Day 7 · 装饰器、上下文管理器、dataclass

- [ ] 函数是对象；闭包
- [ ] 装饰器原理：`@wraps`、带参数的装饰器
- [ ] **重点**：看懂 `src/agent/tools/base.py` 里的 `@tool(ArgsModel)` 到底做了什么
- [ ] 上下文管理器：`with`、`__enter__/__exit__`、`contextlib.contextmanager`
- [ ] `dataclass`：`field(default_factory=...)`
- [ ] 类型注解：`list[str]`、`dict[str, Any]`、`Optional`、`|None`
- [ ] 练习：写一个 `@timer` 装饰器，打印函数耗时
- [ ] **自测**：不看源码，解释 `@tool(CalcArgs)` 注册流程的三步

## Day 8 · pydantic（agent 的基石）

- [ ] `BaseModel`、字段类型、默认值
- [ ] `Field(description=...)` —— **这个 description 会进给模型的 JSON Schema**
- [ ] 校验：类型转换、必填、`ValidationError`
- [ ] `model_json_schema()`：对照 `all_schemas()` 的输出看
- [ ] `model_validate_json()` / `model_dump()`
- [ ] `pydantic-settings`：`Settings` 如何从 `.env` 读配置
- [ ] 练习：给 `src/agent/config.py` 加一个新配置项，让它在 `.env` 里可覆盖
- [ ] **自测**：画出 `CalcArgs` → JSON Schema → 模型 → `tool_calls` → `model_validate_json` 的完整链路

## Day 9 · asyncio 上（最容易卡的一关）

- [ ] 什么是协程；`async def` 调用得到的是 coroutine 对象，不执行
- [ ] `await` 在等什么（对照 C++ 的 future，但单线程事件循环）
- [ ] `asyncio.run()`、`asyncio.gather()`、`create_task()`
- [ ] 并发 ≠ 并行：IO 密集才有收益
- [ ] 练习：并发请求 5 个 URL，对比串行耗时
- [ ] **自测**：解释 `gather` 和 `await` 一个个调用的区别

## Day 10 · asyncio 下 + httpx

- [ ] `asyncio.wait_for` 超时、`asyncio.Semaphore` 限流
- [ ] 异常传播：`gather(return_exceptions=True)`
- [ ] `asyncio.sleep` vs `time.sleep`（后者会卡死整个事件循环）
- [ ] `httpx.AsyncClient`、连接池复用
- [ ] 练习：给 Day 9 的并发请求加超时和并发上限
- [ ] **自测**：说明为什么 agent 里的工具调用几乎都要 async

## Day 11 · 第一次调 DeepSeek API

- [ ] `openai` SDK + `base_url` 改指向 DeepSeek
- [ ] `messages` 结构：`system` / `user` / `assistant`
- [ ] 读懂 response：`choices[0].message.content`、`finish_reason`、`usage`
- [ ] `temperature`、`max_tokens` 的作用与代价
- [ ] 读 `src/agent/llm.py`，逐行看懂 `retry` 和 `Usage` 记账
- [ ] 练习：不加任何封装，20 行内调通一次对话
- [ ] **自测**：打印原始 response JSON，说出每个字段的含义

## Day 12 · function calling（今天的成果就是 M1）

- [ ] `tools` 参数格式：`{"type":"function","function":{name,description,parameters}}`
- [ ] 模型返回的 `tool_calls` 长什么样
- [ ] 把工具结果作为 `role="tool"` 消息追加回去
- [ ] 为什么 assistant 那条消息必须原样回填（漏了会死循环）
- [ ] 练习：**合上 `agent.py`，自己从零写一个 ReAct 循环**
- [ ] **自测**：跑通 `uv run python -m agent.cli "现在几点，算一下 23*47" --verbose`，能解释每一步

## Day 13 · 测试与日志

- [ ] `pytest`：`assert`、`fixture`、`parametrize`、`raises`
- [ ] 给 `tools/base.py` 的 `call()` 写 3 个测试（正常 / 坏参数 / 未知工具）
- [ ] `logging` vs `loguru`；日志级别；为什么不要 `print` 调试
- [ ] `ruff check` / `ruff format`
- [ ] 练习：把 `tests/test_smoke.py` 扩充到 12 个用例
- [ ] **自测**：`uv run pytest -q` 全绿，且你能说出每个用例在防什么

## Day 14 · 复盘 + 通读项目

- [ ] 不看代码，画出 `cli.py → agent.py → llm.py → tools/` 的调用链
- [ ] 通读 `src/agent/` 全部 5 个文件，每个文件写 3 行注释
- [ ] 整理 `docs/notes.md`，把 14 天的笔记压成一页
- [ ] 写一篇《C++ 程序员踩的 10 个 Python 坑》发到仓库（`docs/`）
- [ ] **自测**：能对着白板讲 10 分钟"这个 agent 是怎么工作的"

---

## 14 天后的验收标准

- [ ] 能独立写出一个带工具调用的 agent 循环，不抄代码
- [ ] 能解释 `messages` 数组在每一轮里如何变化
- [ ] 能看懂并修改本项目任意一个文件
- [ ] `uv run pytest -q` 全绿，`uv run ruff check .` 无警告
- [ ] 仓库有 14 天连续 commit 记录

过了这 5 条，W3 才真正开始学 agent；没过就再补一周，**不要硬着头皮往前冲**——
W3 之后所有东西都建立在这两周之上，地基虚了后面全是背概念。
