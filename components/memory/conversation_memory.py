"""
Conversation Memory Examples

Runnable LangChain memory examples showing how to preserve conversation history.
"""

import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage, SystemMessage


def run_conversation_buffer_memory() -> None:
    """Create a conversation chain using ConversationBufferMemory."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set. Set it to run memory examples.")
        return

    llm = ChatOpenAI(api_key=api_key, temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)

    print("\nSending first message...")
    response1 = chain.predict(input="Hello! Can you introduce yourself?")
    print(f"Assistant: {response1}")

    print("\nSending second message with context preserved...")
    response2 = chain.predict(input="What did I ask you earlier?")
    print(f"Assistant: {response2}")


def run_windowed_memory() -> None:
    """Create a conversation chain using ConversationBufferWindowMemory."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set. Set it to run memory examples.")
        return

    llm = ChatOpenAI(api_key=api_key, temperature=0.7)
    memory = ConversationBufferWindowMemory(k=2, return_messages=True)
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)

    chain.predict(input="Hi there.")
    chain.predict(input="I am working on a LangChain project.")
    response = chain.predict(input="What was I working on?")
    print(f"Assistant: {response}")


def run_summary_memory() -> None:
    """Create a conversation chain using ConversationSummaryBufferMemory."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set. Set it to run memory examples.")
        return

    llm = ChatOpenAI(api_key=api_key, temperature=0.7)
    memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=150)
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)

    chain.predict(input="I want to build an agent that can answer questions about a product.")
    chain.predict(input="Please remember that I prefer short answers.")
    response = chain.predict(input="What should I keep in mind?\n")
    print(f"Assistant: {response}")


if __name__ == "__main__":
    print("=== Conversation Memory Examples ===")
    run_conversation_buffer_memory()
    run_windowed_memory()
    run_summary_memory()
