# 垂域研究助手（GUET Research Agent）

一个从零手写的 ReAct Agent：本地语料检索 + 工具调用 + 带引用的回答。
不依赖 LangChain，循环、工具注册、检索全部自己实现，方便逐层拆解和面试讲解。

> 状态：**W2 阶段**（基础骨架已跑通，检索层待接入）

## 快速开始

```bash
cp .env.example .env          # Windows: copy .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

uv sync                       # 装依赖
uv run pytest -q              # 冒烟测试（不需要 API key）
uv run python -m agent.cli --tool
uv run python -m agent.cli "现在几点，顺便算一下 23*47" --verbose
```

## 架构

```
question
   │
   ▼
┌─────────────┐   tool_calls    ┌──────────────┐
│  ReAct 循环  │ ──────────────▶ │  工具注册表   │
│  agent.py   │ ◀────────────── │  tools/      │
└─────────────┘   tool result   └──────────────┘
   │                                   │
   │ 最终回答（带 [1][2] 引用）          ├─ retrieve   （待接入）
   ▼                                   ├─ fetch_url  （待接入）
  CLI / Web                            ├─ calculator
                                       └─ now
```

| 模块 | 职责 | 状态 |
|---|---|---|
| `config.py` | pydantic Settings，读 `.env` | ✅ |
| `llm.py` | DeepSeek 客户端、重试、token 记账 | ✅ |
| `tools/base.py` | 装饰器注册 + pydantic 自动生成 schema | ✅ |
| `tools/builtin.py` | `now` / `calculator` | ✅ |
| `agent.py` | ReAct 循环 | ✅ v0.1 |
| `rag/` | chunk / embed / store / rerank | ⬜ W4 |
| `api.py` | FastAPI + SSE 流式 | ⬜ W6 |
| `eval/` | 20 条评测集 + 报告 | 🟡 种子 5 条 |

## 评测

> 待 W6 填充。格式：优化前 → 优化后。

| 指标 | 基线 | 优化后 |
|---|---|---|
| 引用可追溯率 | — | — |
| 关键事实覆盖率 | — | — |
| 平均延迟 | — | — |
| 单次成本 | — | — |

## 路线图

- [x] W1–W2 环境 + Python 基础 + 首次 function calling
- [ ] W3 合上 `agent.py` 手写三遍 ReAct / Plan-and-Solve / Reflection
- [ ] W4 RAG 底座（bge-m3 + Chroma + reranker）
- [ ] W5 串联 v1（5 个工具 + 引用）
- [ ] W6 评测 + Langfuse trace + 流式 Web
- [ ] W7 Docker 部署 + demo 视频
- [ ] W8 简历 + 投递

## 目录

```
src/agent/      核心代码
  tools/        工具（新增工具：写函数 + @tool + 在 __init__ 里 import）
  rag/          检索（W4 填充）
eval/           评测集与脚本
data/raw/       原始语料（不进 git）
data/index/     向量库（不进 git）
tests/          测试
```

## License

MIT
