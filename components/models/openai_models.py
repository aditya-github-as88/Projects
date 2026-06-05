"""
OpenAI Models in LangChain

Integration examples for OpenAI's language models.
Supports GPT-3.5-turbo, GPT-4, and standard text generation models.
"""

import os
from typing import List

from langchain_openai import OpenAI, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def basic_openai_llm() -> None:
    """
    Example 1: Simple OpenAI LLM invocation.
    """
    print("\n=== Basic OpenAI LLM ===")
    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-davinci-003",
        temperature=0.7,
        max_tokens=120
    )

    response = llm.invoke("Explain LangChain in one sentence.")
    print(f"Response: {response}")


def chat_openai_example() -> None:
    """
    Example 2: Using the OpenAI chat model.
    """
    print("\n=== OpenAI Chat Model ===")
    chat = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        temperature=0.6
    )

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Summarize why LangChain is useful.")
    ]
    response = chat.invoke(messages)
    print(f"Chat response: {response.content}")


def parameter_control() -> None:
    """
    Example 3: Controlling model parameters.
    """
    print("\n=== Model Parameter Control ===")
    temperatures = [0.0, 0.5, 1.0]
    for temp in temperatures:
        llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temp,
            max_tokens=50
        )
        response = llm.invoke("Generate a friendly greeting.")
        print(f"Temperature={temp}: {response}")


def chat_history_example() -> None:
    """
    Example 4: Using chat history with a chat model.
    """
    print("\n=== Chat History Example ===")
    chat = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        temperature=0.5
    )
    
    history = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Hi, I need ideas for a workshop."),
        HumanMessage(content="I want the ideas to be interactive and beginner friendly.")
    ]
    response = chat.invoke(history)
    print(f"Response: {response.content}")


def model_comparison() -> None:
    """
    Example 5: Compare OpenAI models and use cases.
    """
    print("\n=== OpenAI Model Comparison ===")
    models = ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]
    for model_name in models:
        print(f"- {model_name}")
    print("Use GPT-4 for advanced reasoning and GPT-3.5 for cost-effective general use.")


def error_handling() -> None:
    """
    Example 6: Show how to handle API errors.
    """
    print("\n=== Error Handling ===")
    try:
        llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="invalid-model")
        llm.invoke("Hello")
    except Exception as e:
        print(f"Caught error: {type(e).__name__} - {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("OpenAI Models Examples")
    print("="*60)
    basic_openai_llm()
    chat_openai_example()
    parameter_control()
    chat_history_example()
    model_comparison()
    error_handling()