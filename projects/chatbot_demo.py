"""
Chatbot Demo

A simple chatbot example using LangChain and a chat model.
"""

import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def run_chatbot() -> None:
    """
    Example chatbot that responds to a user prompt.
    """
    print("\n=== Chatbot Demo ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        return
    
    chat = ChatOpenAI(
        api_key=api_key,
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Hello! Can you help me brainstorm an idea for a blog post?")
    ]
    
    response = chat.invoke(messages)
    print(f"Bot: {response.content}")


if __name__ == "__main__":
    run_chatbot()