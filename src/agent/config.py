"""全局配置。所有可调参数集中在这里，改行为不用翻代码。"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- LLM ---
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.0
    max_tokens: int = 2048

    # --- Agent ---
    max_steps: int = 8          # ReAct 循环最多几轮，防止无限调用
    tool_timeout: float = 15.0  # 单次工具执行超时（秒）

    # --- RAG ---
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 5
    rerank_top_n: int = 3


settings = Settings()
