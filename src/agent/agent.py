"""ReAct 循环 —— 整个项目的核心。

也是 W3 的作业：合上这个文件，从零自己写一遍，写完再回来对比。

结构只有三步，循环往复：
    1. 把 messages + 工具 schema 发给模型
    2. 模型要么直接回答（tool_calls 为空），要么要求调工具（tool_calls 非空）
    3. 要调工具 → 执行 → 把结果作为 role="tool" 的消息追加回 messages → 回到 1
"""

from __future__ import annotations

from typing import Any

from loguru import logger

from agent.config import settings
from agent.llm import get_llm
from agent.tools import all_schemas, call

SYSTEM_PROMPT = """你是一个严谨的研究助手。规则：
1. 涉及事实、数字、时间的问题，必须先调用工具，不要凭记忆回答。
2. 回答中的每个事实都要标注来源编号，例如 [1][2]。
3. 检索不到就明确说"资料中没有找到"，绝不编造。
4. 用中文回答，简洁，不要复述题目。"""


def run_agent(
    question: str,
    max_steps: int | None = None,
    verbose: bool = False,
) -> dict[str, Any]:
    """跑完一次 ReAct，返回 {'answer', 'steps', 'usage'}。"""
    llm = get_llm()
    limit = max_steps or settings.max_steps
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    tools = all_schemas()

    for step in range(1, limit + 1):
        resp = llm.chat(messages, tools=tools)
        msg = resp.choices[0].message

        # --- 分支 A：模型要调工具 ---
        if msg.tool_calls:
            # 关键：assistant 这条消息必须原样追加回去（含 tool_calls），
            # 否则下一轮模型看不到自己发起过调用，会重复调用同一个工具。
            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in msg.tool_calls
                    ],
                }
            )

            for tc in msg.tool_calls:
                if verbose:
                    logger.info(f"[step {step}] 调用 {tc.function.name}({tc.function.arguments})")
                result = call(tc.function.name, tc.function.arguments)
                if verbose:
                    logger.info(f"[step {step}] 返回 {result[:200]}")
                messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )
            continue

        # --- 分支 B：模型给出最终回答 ---
        return {"answer": msg.content or "", "steps": step, "usage": str(llm.usage)}

    return {
        "answer": f"达到最大步数 {limit} 仍未得出结论，建议拆小问题。",
        "steps": limit,
        "usage": str(llm.usage),
    }
