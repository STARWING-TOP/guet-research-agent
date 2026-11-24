"""垂域研究助手 —— ReAct + RAG + 引用。"""

from __future__ import annotations

import os
import sys

from loguru import logger

__version__ = "0.1.0"

# loguru 默认把 DEBUG 也打出来，对学习期来说太吵。
# 需要看详细日志时：$env:LOG_LEVEL="DEBUG"
logger.remove()
logger.add(
    sys.stderr,
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <7}</level> | {message}",
)
