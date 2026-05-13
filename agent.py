"""
agent.py  —  Weather Monitoring Agent (v2, no external LLM)

Routing is handled locally: the agent reads the user query,
matches it against the tool registry using keyword rules
(mirroring what the system prompt would tell an LLM to do),
executes the right tool, and prints the result.

For open-ended queries that match no tool, the agent prints
the system prompt instructions so Copilot (your executor)
can answer directly in the Chat panel.

No Anthropic SDK. No API keys. No external calls.
Run with:  python agent.py
"""

import json
from pathlib import Path
from typing import Optional

from tools.math_tool      import TOOL_SCHEMA as MATH_SCHEMA,      run as math_run
from tools.sentiment_tool import TOOL_SCHEMA as SENTIMENT_SCHEMA,  run as sentiment_run
from tools.forecast_tool  import TOOL_SCHEMA as FORECAST_SCHEMA,   run as forecast_run
from core.hooks           import run_with_hooks, get_audit_log

ROOT = Path(__file__).parent

# ── Tool registry (3 tools, no catch_all) ─────────────────────────────────────
TOOL_REGISTRY = {
    "math_tool":      (math_run,      MATH_SCHEMA),
    "sentiment_tool": (sentiment_run, SENTIMENT_SCHEMA),
    "forecast_tool":  (forecast_run,  FORECAST_SCHEMA),
}


# ── Load .github files ─────────────────────────────────────────────────────────

def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

SYSTEM_PROMPT = load_file(ROOT / ".github" / "prompt.md")
SKILL_CONTEXT = load_file(ROOT / ".github" / "skills" / "SKILL.md")


# ── Local router (mirrors the LLM routing rules in prompt.md) ─────────────────

def route(query: str) -> Optional[str]:
    """
    Return the tool name that should handle this query, or None.
    Rules mirror .github/prompt.md decision order.
    """
    q = query.lower()

    math_keywords = [
        "convert", "celsius", "fahrenheit", "kelvin", "°c", "°f",
        "mph", "km/h", "hpa", "inhg", "heat index", "wind chill",
        "dew point", "to f", "to c", "to k",
    ]
    if any(k in q for k in math_keywords):
        return "math_tool"

    sentiment_keywords = [
        "safe", "feel", "feels", "comfortable", "jog", "run", "exercise",
        "dangerous", "hot outside", "too hot", "too cold", "activity",
        "should i go", "can i go outside", "wear",
    ]
    if any(k in q for k in sentiment_keywords):
        return "sentiment_tool"

    forecast_keywords = [
        "rain", "forecast", "precipitation", "chance of", "umbrella",
        "storm", "prepare for", "trend", "rising", "falling", "tomorrow",
    ]
    if any(k in q for k in forecast_keywords):
        return "forecast_tool"

    return None   # catch-all path


# ── Tool input builder ─────────────────────────────────────────────────────────

def build_tool_input(tool_name: str, query: str) -> dict:
    """Extract parameters from the query for the matched tool."""
    import re
    numbers = re.findall(r"-?\d+(?:\.\d+)?", query)
    floats  = [float(n) for n in numbers]

    if tool_name == "math_tool":
        q = query.lower()
        if "heat index" in q:
            op = "heat_index"
        elif "wind chill" in q:
            op = "wind_chill"
        elif "dew point" in q:
            op = "dew_point"
        elif any(w in q for w in ["to f", "fahrenheit"]):
            op = "c_to_f"
        elif any(w in q for w in ["to c", "celsius"]) and "fahrenheit" in q:
            op = "f_to_c"
        elif "kelvin" in q or "to k" in q:
            op = "c_to_k"
        elif "mph" in q:
            op = "mph_to_kmh"
        elif "hpa" in q:
            op = "hpa_to_inhg"
        else:
            op = "c_to_f"

        inp: dict = {"operation": op, "value": floats[0] if floats else 0.0}
        if len(floats) >= 2 and op in {"heat_index", "wind_chill", "dew_point"}:
            inp["secondary_value"] = floats[1]
        return inp

    if tool_name == "sentiment_tool":
        inp = {"temperature_c": floats[0] if floats else 30.0}
        for activity in ["jog", "run", "hike", "swim", "cycle", "exercise", "work"]:
            if activity in query.lower():
                inp["activity"] = activity
                break
        if any(w in query.lower() for w in ["elderly", "child", "kids", "vulnerable"]):
            inp["vulnerable_group"] = True
        if len(floats) >= 2:
            inp["humidity_pct"] = floats[1]
        return inp

    if tool_name == "forecast_tool":
        inp: dict = {"precipitation_pct": floats[0] if floats else 50.0}
        q = query.lower()
        inp["temperature_trend"] = (
            "rising"  if "rising"  in q else
            "falling" if any(w in q for w in ["falling", "drop"]) else
            "stable"
        )
        if len(floats) >= 2:
            inp["humidity_pct"] = floats[1]
        return inp

    return {}


# ── Output formatters ──────────────────────────────────────────────────────────

def format_tool_result(tool_name: str, raw_json: str) -> None:
    print(f"\n{'='*60}")
    print(f"  [Tool: {tool_name}]")
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
    print()


def format_catch_all(query: str) -> None:
    """
    No tool matched.
    In VS Code: paste this output into Copilot Chat — it will answer directly.
    The format mirrors what prompt.md instructs an LLM to do.
    """
    print(f"\n{'='*60}")
    print(f"  [No tool matched — catch-all path]")
    print(f"  → Copilot/LLM answers from world knowledge")
    print(f"{'='*60}")
    print(f"\n  Query: {query}")
    print(f"\n  Copilot should respond as:")
    print(f"  {'─'*50}")
    print(f"    <direct answer from world knowledge>")
    print(f"")
    print(f"    Reasoning trace:")
    print(f"    - Knowledge used: <physics / geography / general science / etc.>")
    print(f"    - Confident: <facts you are sure about>")
    print(f"    - Uncertain: <what you cannot confirm without live data>")
    print(f"    - New tool suggested: <yes/no and why>")
    print()


# ── Main runner ────────────────────────────────────────────────────────────────

def run_agent(query: str) -> None:
    print(f"\n{'─'*60}")
    print(f"  User: {query}")
    print(f"{'─'*60}")

    tool_name = route(query)

    if tool_name:
        tool_fn, _ = TOOL_REGISTRY[tool_name]
        tool_input  = build_tool_input(tool_name, query)
        result      = run_with_hooks(tool_name, tool_fn, tool_input)
        format_tool_result(tool_name, json.dumps(result, indent=2))
    else:
        format_catch_all(query)


def main() -> None:
    print("\n" + "="*60)
    print("  WEATHER MONITORING AGENT")
    print("  No Anthropic SDK | No API keys | No external calls")
    print("  Tools: math_tool | sentiment_tool | forecast_tool")
    print("  Catch-all: Copilot answers from world knowledge")
    print("="*60)

    demo_queries = [
        "Convert 37°C to Fahrenheit",
        "Heat index at 38°C and 75% humidity?",
        "Is it safe to jog outside at 42 degrees?",
        "75% chance of rain and temperature rising — what should I prepare for?",
        "Why is the sky blue on a clear day?",              # → catch-all
        "Compare monsoon humidity vs winter humidity",       # → catch-all
        "What causes the cold wind before a thunderstorm?", # → catch-all
    ]

    for q in demo_queries:
        run_agent(q)

    print("\n" + "="*60)
    print("  Interactive mode  (type 'exit' to quit, 'log' for audit trail)")
    print("="*60 + "\n")

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
            run_agent(user_input)
        except KeyboardInterrupt:
            break

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
