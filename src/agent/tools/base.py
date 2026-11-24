"""工具注册表：装饰器 + pydantic 自动生成 JSON Schema。

手写 schema 很容易和函数签名对不上，所以这里用 pydantic 模型当唯一事实来源：
改参数只改一个地方，schema 自动跟着变。
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ValidationError


@dataclass
class Tool:
    name: str
    description: str
    args_model: type[BaseModel]
    func: Callable[..., Any]

    def schema(self) -> dict[str, Any]:
        """转成 OpenAI function calling 需要的格式。"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.args_model.model_json_schema(),
            },
        }

    def run(self, raw_args: str) -> str:
        """执行工具。

        永远返回字符串，永远不抛异常 —— 工具失败也是一种观测结果，
        交给模型自己决定重试还是换路，比让整个 agent 崩掉好。
        """
        try:
            parsed = self.args_model.model_validate_json(raw_args or "{}")
        except ValidationError as e:
            return json.dumps({"error": f"参数不合法: {e.errors()}"}, ensure_ascii=False)

        try:
            result = self.func(**parsed.model_dump())
        except Exception as e:  # noqa: BLE001
            return json.dumps({"error": f"{type(e).__name__}: {e}"}, ensure_ascii=False)

        return result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)


REGISTRY: dict[str, Tool] = {}


def tool(args_model: type[BaseModel]):
    """注册一个工具。

    注意：函数的 docstring 就是模型看到的全部描述，要当成 prompt 来写
    （写清用途、什么时候该调、什么时候不该调）。
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        REGISTRY[func.__name__] = Tool(
            name=func.__name__,
            description=(func.__doc__ or "").strip(),
            args_model=args_model,
            func=func,
        )
        return func

    return decorator


def all_schemas() -> list[dict[str, Any]]:
    return [t.schema() for t in REGISTRY.values()]


def call(name: str, raw_args: str) -> str:
    t = REGISTRY.get(name)
    if t is None:
        return json.dumps({"error": f"未知工具: {name}"}, ensure_ascii=False)
    return t.run(raw_args)
