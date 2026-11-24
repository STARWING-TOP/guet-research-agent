"""内置工具：两个最小的、无副作用的，用来跑通 function calling。"""

from __future__ import annotations

import ast
import json
import operator
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field

from agent.tools.base import tool

TZ = ZoneInfo("Asia/Shanghai")


class EmptyArgs(BaseModel):
    """无参数工具用这个占位。"""


class CalcArgs(BaseModel):
    expression: str = Field(
        description="纯算术表达式，例如 (23*47)+100。只支持 + - * / // % ** 和括号。"
    )


@tool(EmptyArgs)
def now() -> str:
    """获取当前时间（北京时间）和星期。

    任何涉及"今天""现在""最近""还有几天"的问题，都必须先调用本工具，
    不要用你训练数据里的时间。
    """
    dt = datetime.now(TZ)
    return json.dumps(
        {"datetime": dt.strftime("%Y-%m-%d %H:%M:%S"), "weekday": dt.strftime("%A")},
        ensure_ascii=False,
    )


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def _eval_node(node: ast.AST) -> float:
    """只放行算术节点。绝不使用 eval()。"""
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd | ast.USub):
        v = _eval_node(node.operand)
        return v if isinstance(node.op, ast.UAdd) else -v
    raise ValueError(f"不支持的语法: {type(node).__name__}")


@tool(CalcArgs)
def calculator(expression: str) -> str:
    """计算算术表达式。不要心算，任何涉及数字运算的问题一律调用本工具。"""
    tree = ast.parse(expression, mode="eval")
    return json.dumps({"expression": expression, "result": _eval_node(tree.body)})
