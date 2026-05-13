# Agent Hooks

## before_tool
Fires before any tool call. Logs tool name and inputs.

## after_tool
Fires after any tool call. Logs result summary and elapsed time.
If result contains "error", triggers on_error.

## on_error
Logs the error and returns a user-friendly message.
Does not retry — user decides next step.

## on_direct_response
Fires when the LLM answers WITHOUT calling a tool (the catch-all path).
Detects a "Reasoning trace:" section in the response and formats it clearly.
Optionally flags recurring patterns that suggest a new tool should be added.
