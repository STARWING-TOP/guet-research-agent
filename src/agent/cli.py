"""命令行入口。

用法：
    uv run python -m agent.cli "现在几点，顺便算一下 23*47"
    uv run python -m agent.cli --verbose "..."
    uv run python -m agent.cli --tool          # 列出已注册工具
    uv run python -m agent.cli                 # 交互模式
"""

from __future__ import annotations

import argparse

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from agent.agent import run_agent
from agent.tools import REGISTRY

console = Console()


def _ask(question: str, verbose: bool) -> None:
    try:
        result = run_agent(question, verbose=verbose)
    except RuntimeError as e:
        # 最常见的就是忘配 .env，给一句人话，而不是甩一屏 traceback
        console.print(f"[bold red]✗ {e}[/bold red]")
        raise SystemExit(1) from e
    console.print(Panel(Markdown(result["answer"]), title="回答", border_style="cyan"))
    console.print(f"[dim]steps={result['steps']} | {result['usage']}[/dim]")


def main() -> None:
    parser = argparse.ArgumentParser(description="垂域研究助手 v0.1")
    parser.add_argument("question", nargs="*", help="要问的问题；不填则进入交互模式")
    parser.add_argument("--verbose", action="store_true", help="打印每一步工具调用")
    parser.add_argument("--tool", action="store_true", help="列出已注册工具后退出")
    args = parser.parse_args()

    if args.tool:
        for t in REGISTRY.values():
            console.print(f"[bold cyan]{t.name}[/bold cyan]  {t.description.splitlines()[0]}")
        return

    if args.question:
        _ask(" ".join(args.question), args.verbose)
        return

    console.print("[dim]输入问题，Ctrl+C 退出[/dim]")
    while True:
        try:
            q = console.input("[bold green]你 > [/bold green]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break
        if q:
            _ask(q, args.verbose)


if __name__ == "__main__":
    main()
