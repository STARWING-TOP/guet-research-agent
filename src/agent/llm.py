"""DeepSeek 客户端封装：重试、token 记账、成本估算都收在这一层。

用 openai SDK 是因为 DeepSeek 的接口与 OpenAI 完全兼容，改个 base_url 就行。
这一层不放业务逻辑，它只负责「发一次请求、记一次账」。
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from loguru import logger
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from agent.config import settings

# DeepSeek 官网价目（元 / 百万 token）。价格会变，以官网实时价目为准。
PRICE_INPUT_PER_M = 2.0
PRICE_OUTPUT_PER_M = 8.0


@dataclass
class Usage:
    """累计用量。评测报告和简历里的成本数字都从这里来。"""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    calls: int = 0

    def add(self, prompt: int, completion: int) -> None:
        self.prompt_tokens += prompt
        self.completion_tokens += completion
        self.calls += 1

    @property
    def cost_cny(self) -> float:
        return (
            self.prompt_tokens / 1_000_000 * PRICE_INPUT_PER_M
            + self.completion_tokens / 1_000_000 * PRICE_OUTPUT_PER_M
        )

    def __str__(self) -> str:
        return (
            f"calls={self.calls} in={self.prompt_tokens} out={self.completion_tokens} "
            f"cost=¥{self.cost_cny:.4f}"
        )


class LLM:
    def __init__(self, api_key: str | None = None) -> None:
        key = api_key or settings.deepseek_api_key
        if not key:
            raise RuntimeError(
                "没有找到 API key。请把 .env.example 复制成 .env，填入 DEEPSEEK_API_KEY。"
            )
        self._client = OpenAI(api_key=key, base_url=settings.deepseek_base_url)
        self.usage = Usage()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        **overrides: Any,
    ):
        """发一次 chat completion，返回**原始** completion 对象。

        为什么返回原始对象而不是字符串：agent 需要拿到 tool_calls 才能决定下一步。
        """
        kwargs: dict[str, Any] = {
            "model": overrides.get("model", settings.model),
            "messages": messages,
            "temperature": overrides.get("temperature", settings.temperature),
            "max_tokens": overrides.get("max_tokens", settings.max_tokens),
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = overrides.get("tool_choice", "auto")

        resp = self._client.chat.completions.create(**kwargs)
        if resp.usage is not None:
            self.usage.add(resp.usage.prompt_tokens, resp.usage.completion_tokens)
            logger.debug(f"llm ok | {self.usage}")
        return resp


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    """全局单例，保证 usage 是累计的，而不是每次新建。"""
    return LLM()
