"""
hooks.py
Implements the lifecycle callbacks defined in .github/hooks.md.
Wraps every tool invocation with logging, error handling, and
catch_all-specific behaviour.
"""

import json
import time
from datetime import datetime
from typing import Any, Callable, Dict


AUDIT_LOG = []  # In production: write to a file or internal logging service


def before_tool(tool_name: str, tool_input: Dict) -> None:
    """Fires before any tool is called."""
    entry = {
        "event": "before_tool",
        "tool": tool_name,
        "input_keys": list(tool_input.keys()),
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
    AUDIT_LOG.append(entry)

    print(f"\n{'─'*60}")
    print(f"[Hook: before_tool]  tool={tool_name}")

    if tool_name == "catch_all_tool":
        routing = tool_input.get("routing_reason", "not specified")
        print(f"[catch_all] No specific tool matched.")
        print(f"[catch_all] Routing reason: {routing}")
        print(f"[catch_all] Routing to internal reasoning engine...")


def after_tool(tool_name: str, result: Dict, elapsed_ms: float) -> Dict:
    """Fires after any tool returns. Returns the result (possibly annotated)."""
    entry = {
        "event": "after_tool",
        "tool": tool_name,
        "elapsed_ms": round(elapsed_ms, 2),
        "has_error": "error" in result,
        "has_trace": "trace" in result,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
    AUDIT_LOG.append(entry)

    print(f"[Hook: after_tool]   tool={tool_name}  elapsed={elapsed_ms:.1f}ms")

    if "error" in result:
        return on_error(tool_name, result["error"])

    # Surface trace from catch_all
    if "trace" in result:
        _surface_trace(result["trace"])

    # Check for new tool suggestion
    if result.get("trace", {}).get("suggest_new_tool"):
        on_new_tool_suggestion(result["trace"])

    return result


def on_error(tool_name: str, error_msg: str) -> Dict:
    """Fires when a tool returns an error."""
    entry = {
        "event": "on_error",
        "tool": tool_name,
        "error": error_msg,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
    AUDIT_LOG.append(entry)

    print(f"[Hook: on_error]     tool={tool_name}  error={error_msg}")

    return {
        "error": True,
        "user_message": (
            f"The {tool_name} encountered an issue: {error_msg}. "
            f"Try rephrasing your query or check the input values."
        )
    }


def on_new_tool_suggestion(trace: Dict) -> None:
    """Fires when catch_all detects a recurring query pattern."""
    reason = trace.get("suggestion_reason", "")
    print(f"\n[Hook: on_new_tool_suggestion]")
    print(f"  Pattern detected: {reason}")
    print(f"  [Agent] This query type recurs. Consider adding a dedicated tool.")


def _surface_trace(trace: Dict) -> None:
    """Pretty-print the reasoning trace from catch_all."""
    print(f"\n[Hook: trace_surfaced]")
    print(f"  Category  : {trace.get('knowledge_category', 'unknown')}")
    print(f"  Method    : {trace.get('inference_method', 'unknown')}")
    if trace.get("suggest_new_tool"):
        print(f"  Suggestion: {trace.get('suggestion_reason', '')}")


def get_audit_log() -> str:
    """Return the full audit log as JSON string."""
    return json.dumps(AUDIT_LOG, indent=2)


def run_with_hooks(tool_name: str, tool_fn: Callable, tool_input: Dict) -> Dict:
    """
    Wraps a tool call with before/after hooks and timing.
    Use this instead of calling tool functions directly.
    """
    before_tool(tool_name, tool_input)

    start = time.time()
    try:
        result = tool_fn(**tool_input)
    except Exception as e:
        result = {"error": str(e)}
    elapsed = (time.time() - start) * 1000

    result = after_tool(tool_name, result, elapsed)
    return result
