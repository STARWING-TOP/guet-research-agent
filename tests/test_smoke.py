"""冒烟测试：不需要 API key 就能跑，保证骨架没坏。

跑法：uv run pytest -q
"""

from __future__ import annotations

import json

from agent.config import settings
from agent.tools import REGISTRY, all_schemas, call


def test_tools_registered() -> None:
    assert "now" in REGISTRY
    assert "calculator" in REGISTRY


def test_schema_shape() -> None:
    schemas = all_schemas()
    assert schemas
    for s in schemas:
        assert s["type"] == "function"
        assert {"name", "description", "parameters"} <= s["function"].keys()


def test_calculator_works() -> None:
    out = json.loads(call("calculator", '{"expression": "(23*47)+100"}'))
    assert out["result"] == 1181


def test_calculator_rejects_call_expression() -> None:
    payload = {"expression": '__import__("os").system("dir")'}
    out = json.loads(call("calculator", json.dumps(payload)))
    assert "error" in out


def test_calculator_rejects_bad_args() -> None:
    out = json.loads(call("calculator", '{"nope": 1}'))
    assert "error" in out


def test_unknown_tool_is_reported_not_raised() -> None:
    assert "error" in json.loads(call("does_not_exist", "{}"))


def test_settings_defaults_are_sane() -> None:
    assert settings.max_steps >= 1
    assert settings.top_k >= 1
