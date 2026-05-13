"""
agent.py  —  Weather Monitoring Agent  (v2)

The catch-all here is NOT a tool.
When no tool matches, the LLM answers from its own world knowledge.
The system prompt instructs it to append a "Reasoning trace:" block.
This runner detects that block and formats it for the user.

No external APIs. No catch_all_tool. Just the LLM reasoning transparently.
"""

import json
import re
from pathlib import Path
from anthropic import Anthropic

from tools.math_tool      import TOOL_SCHEMA as MATH_SCHEMA,      run as math_run
from tools.sentiment_tool import TOOL_SCHEMA as SENTIMENT_SCHEMA,  run as sentiment_run
from tools.forecast_tool  import TOOL_SCHEMA as FORECAST_SCHEMA,   run as forecast_run
from core.hooks           import run_with_hooks, get_audit_log

ROOT = Path(__file__).parent

# ── Only THREE tools registered. No catch_all. ───────────────────────────────
TOOL_REGISTRY = {
    "math_tool":      (math_run,      MATH_SCHEMA),
    "sentiment_tool": (sentiment_run, SENTIMENT_SCHEMA),
    "forecast_tool":  (forecast_run,  FORECAST_SCHEMA),
}
ALL_SCHEMAS = [schema for _, schema in TOOL_REGISTRY.values()]


def load_system_prompt() -> str:
    """Load prompt from .github/prompt.md + skills context."""
    parts = []
    for p in [ROOT / ".github/prompt.md", ROOT / ".github/skills/SKILL.md"]:
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
    return "\n\n---\n\n".join(parts)


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name not in TOOL_REGISTRY:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    tool_fn, _ = TOOL_REGISTRY[tool_name]
    result = run_with_hooks(tool_name, tool_fn, tool_input)
    return json.dumps(result, indent=2)


# ── Response formatters ───────────────────────────────────────────────────────

def format_tool_result(tool_name: str, raw_json: str) -> None:
    print(f"\n{'='*60}")
    print(f"  [Tool used: {tool_name}]")
    print(f"{'='*60}")
    try:
        data = json.loads(raw_json)
        for k, v in data.items():
            if isinstance(v, list):
                print(f"  {k}:")
                for item in v:
                    print(f"    • {item}")
            else:
                print(f"  {k}: {v}")
    except Exception:
        print(raw_json)


def format_direct_response(text: str) -> None:
    """
    The LLM answered without calling a tool.
    Split on 'Reasoning trace:' and display both parts clearly.
    """
    print(f"\n{'='*60}")
    print(f"  [No tool matched — LLM answered directly]")
    print(f"{'='*60}")

    if "Reasoning trace:" in text:
        answer_part, trace_part = text.split("Reasoning trace:", 1)
        print(f"\n{answer_part.strip()}")
        print(f"\n{'─'*60}")
        print(f"  Reasoning trace:")
        print(f"{'─'*60}")
        for line in trace_part.strip().splitlines():
            print(f"  {line}")
    else:
        # LLM didn't include a trace — show the answer as-is
        print(f"\n{text.strip()}")
        print(f"\n  (No reasoning trace found — consider strengthening prompt.md)")

    print()


# ── Agentic loop ──────────────────────────────────────────────────────────────

def run_agent(user_message: str, client: Anthropic, system_prompt: str) -> None:
    print(f"\n{'='*60}")
    print(f"  User: {user_message}")
    print(f"{'='*60}")

    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=system_prompt,
            tools=ALL_SCHEMAS,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            # ── LLM chose a tool ─────────────────────────────────────────
            tool_block = next(
                (b for b in response.content if b.type == "tool_use"), None
            )
            if not tool_block:
                break

            result_json = execute_tool(tool_block.name, tool_block.input)
            format_tool_result(tool_block.name, result_json)

            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_block.id,
                    "content": result_json,
                }],
            })

        else:
            # ── LLM answered directly (the catch-all path) ───────────────
            final_text = next(
                (b.text for b in response.content if hasattr(b, "text")),
                ""
            )
            format_direct_response(final_text)
            break


# ── Demo ──────────────────────────────────────────────────────────────────────

def main():
    client        = Anthropic()
    system_prompt = load_system_prompt()

    print("\n" + "="*60)
    print("  WEATHER MONITORING AGENT  (v2 — correct catch-all)")
    print("  Tools: math_tool | sentiment_tool | forecast_tool")
    print("  Catch-all: LLM answers directly, no 4th tool")
    print("="*60)

    queries = [
        # → math_tool
        "Convert 37°C to Fahrenheit",

        # → math_tool (two inputs)
        "Heat index at 38°C and 75% humidity?",

        # → sentiment_tool
        "Is it safe to jog outside at 42 degrees?",

        # → forecast_tool
        "75% chance of rain and temperature rising — what should I prepare for?",

        # → LLM direct (no tool matches)
        "Why is the sky blue on a clear day?",

        # → LLM direct (comparison, no tool matches)
        "Compare how monsoon humidity feels versus winter humidity",

        # → LLM direct (world knowledge, no tool matches)
        "What causes the cold wind that comes just before a thunderstorm?",
    ]

    for q in queries:
        run_agent(q, client, system_prompt)
        print("─" * 60)

    # Interactive
    print("\n[Interactive — type 'exit' or 'log']\n")
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                break
            if user_input.lower() == "log":
                print(get_audit_log())
                continue
            run_agent(user_input, client, system_prompt)
        except KeyboardInterrupt:
            break

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
