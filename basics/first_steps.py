"""
First Steps with LangChain

Basic examples of using LangChain to call language models.
This covers the foundational pattern: LLM + Prompt -> Response
"""

import os
from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def simple_llm_call() -> None:
    """
    Example 1: Simple LLM call without prompt template.
    Direct text input to the model.
    """
    print("\n=== Example 1: Simple LLM Call ===")
    
    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )
    
    prompt_text = "What is the capital of France?"
    response = llm.invoke(prompt_text)
    print(f"Prompt: {prompt_text}")
    print(f"Response: {response}")


def llm_with_prompt_template() -> None:
    """
    Example 2: LLM with prompt template.
    Templates allow dynamic input substitution.
    """
    print("\n=== Example 2: LLM with Prompt Template ===")
    
    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.5
    )
    
    # Create a simple prompt template
    prompt = PromptTemplate(
        input_variables=["country"],
        template="What is the capital of {country}?"
    )
    
    # Create a chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run the chain
    country = "Japan"
    response = chain.invoke({"country": country})
    print(f"Country: {country}")
    print(f"Response: {response['text']}")


def chat_model_example() -> None:
    """
    Example 3: Using Chat Models (conversation-aware models).
    Chat models work with messages instead of plain text.
    """
    print("\n=== Example 3: Chat Model ===")
    
    chat = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    from langchain.schema import HumanMessage, SystemMessage
    
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Hello! How are you?")
    ]
    
    response = chat.invoke(messages)
    print(f"Chat Response: {response.content}")


def temperature_effect() -> None:
    """
    Example 4: Understanding temperature parameter.
    Temperature controls randomness in responses:
    - 0.0: Deterministic (same answer every time)
    - 1.0: More creative and random
    """
    print("\n=== Example 4: Temperature Effect ===")
    
    prompt = "Write a one-sentence story about a cat."
    
    for temp in [0.0, 0.5, 1.0]:
        llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=temp
        )
        response = llm.invoke(prompt)
        print(f"Temperature {temp}: {response}")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("LangChain First Steps")
    print("="*50)
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set. Please set it to run examples.")
        print("Example: export OPENAI_API_KEY='sk-...'")
    else:
        # Uncomment to run examples
        # simple_llm_call()
        # llm_with_prompt_template()
        # chat_model_example()
        # temperature_effect()
        
        print("\nExamples are ready to run. Uncomment the function calls to execute.")