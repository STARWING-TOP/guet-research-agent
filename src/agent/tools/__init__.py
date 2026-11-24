"""导入即注册。新增工具时在这里 import 一下即可。"""

from agent.tools import builtin  # noqa: F401  <- 这行导入是注册的副作用，不要删
from agent.tools.base import REGISTRY, Tool, all_schemas, call, tool

__all__ = ["REGISTRY", "Tool", "all_schemas", "call", "tool"]
