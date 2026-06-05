"""
Custom Tools Example

Runnable LangChain tools example showing how to wrap local functions and use them in prompts.
"""

from langchain.tools import Tool
from typing import List


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with a gentle breeze (demo data)."


def list_topics(subject: str) -> str:
    topics = {
        "python": ["Syntax", "Data Structures", "Libraries", "Web Development"],
        "langchain": ["Chains", "Agents", "LLMs", "Embeddings"],
        "machine learning": ["Supervised Learning", "Unsupervised Learning", "Evaluation"]
    }
    return ", ".join(topics.get(subject.lower(), ["No topics available for this subject"]))


def get_tools() -> List[Tool]:
    return [
        Tool(name="weather", func=get_weather, description="Get the current weather for a city."),
        Tool(name="topics", func=list_topics, description="List key topics for a subject.")
    ]


def use_tools_directly() -> None:
    tools = get_tools()
    print("\n=== Local Tools Demo ===")
    print(tools[0].run("London"))
    print(tools[1].run("Python"))


if __name__ == "__main__":
    use_tools_directly()
