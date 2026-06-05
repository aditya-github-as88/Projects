"""
Zero-Shot Agent Example

Runnable LangChain agent example using tools and a chat model.
"""

import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from typing import Dict


def search_tool(query: str) -> str:
    return f"Search results for '{query}' are not available in this demo."


def calculator_tool(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as exc:
        return f"Error evaluating expression: {exc}"


def run_zero_shot_agent() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set. Set it to run the agent example.")
        return

    llm = ChatOpenAI(api_key=api_key, temperature=0.3)
    tools = [
        Tool(name="search", func=search_tool, description="Search for general information."),
        Tool(name="calculator", func=calculator_tool, description="Evaluate a math expression.")
    ]

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    prompt = "Find the square root of 16 and tell me what it means in one sentence."
    response = agent.run(prompt)
    print(f"Agent response:\n{response}")


if __name__ == "__main__":
    print("=== Zero-Shot Agent Example ===")
    run_zero_shot_agent()
