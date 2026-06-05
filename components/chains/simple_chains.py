"""
Simple Chains

Basic chain patterns using LangChain.
Chains connect components together for workflow automation.
"""

import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from typing import Dict


def basic_llm_chain() -> None:
    """
    Example 1: Basic LLMChain.
    Simplest chain connecting prompt and LLM.
    """
    print("\n=== Example 1: Basic LLMChain ===")
    
    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7
    )
    
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a short paragraph about {topic}."
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Run the chain
    # result = chain.invoke({"topic": "Machine Learning"})
    # print(f"Result: {result['text']}")
    
    print("Chain structure: Prompt -> LLM -> Output")
    print("Usage: chain.invoke({\"topic\": \"Machine Learning\"})")


def chain_with_memory() -> None:
    """
    Example 2: Chain with conversation memory.
    Maintains context across multiple interactions.
    """
    print("\n=== Example 2: Chain with Memory ===")
    
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    memory = ConversationBufferMemory()
    
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )
    
    print("ConversationChain includes:")
    print("  - LLM")
    print("  - Memory (saves conversation history)")
    print("  - Automatic prompt formatting")


def chain_with_variables() -> None:
    """
    Example 3: Chain with multiple variables.
    Handle complex prompt inputs.
    """
    print("\n=== Example 3: Multiple Variables ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["question", "context"],
        template="""Context: {context}

Question: {question}

Answer:"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # inputs = {
    #     "context": "Paris is the capital of France.",
    #     "question": "What is the capital of France?"
    # }
    # result = chain.invoke(inputs)
    
    print("Chain with multiple input variables:")
    print("  - context")
    print("  - question")


def chain_with_output_key() -> None:
    """
    Example 4: Naming the output key.
    Control what the output is called.
    """
    print("\n=== Example 4: Output Key Configuration ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["product"],
        template="List 5 features of {product}."
    )
    
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="features"  # Custom output key
    )
    
    # result = chain.invoke({"product": "Python"})
    # print(result["features"])  # Access via custom key
    
    print("Output key allows custom naming of results")
    print("Usage: result[\"features\"]")


def chain_streaming() -> None:
    """
    Example 5: Streaming chain output.
    Get results as they're generated.
    """
    print("\n=== Example 5: Streaming Output ===")
    
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
    
    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in 100 words."
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    print("Streaming chain outputs tokens as generated:")
    print("  - Better UX for long responses")
    print("  - Lower latency perception")
    print("  - Useful for real-time applications")


def error_handling_in_chain() -> None:
    """
    Example 6: Error handling in chains.
    Handle failures gracefully.
    """
    print("\n=== Example 6: Error Handling ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["input"],
        template="Process: {input}"
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Proper error handling
    try:
        # result = chain.invoke({"input": "test"})
        pass
    except Exception as e:
        print(f"Chain error: {type(e).__name__}")
        print(f"Handle API errors, timeouts, etc.")


def chain_performance_tips() -> None:
    """
    Example 7: Performance optimization tips.
    """
    print("\n=== Example 7: Performance Tips ===")
    
    tips = {
        "Prompt Optimization": [
            "Keep prompts concise",
            "Avoid unnecessary tokens",
            "Reuse templates"
        ],
        "Model Selection": [
            "Use smaller models when possible",
            "Consider temperature settings",
            "Optimize max_tokens"
        ],
        "Caching & Memory": [
            "Cache frequently used prompts",
            "Use appropriate memory type",
            "Clear old memory regularly"
        ],
        "Async Processing": [
            "Use async chains for multiple requests",
            "Implement batching",
            "Handle rate limits"
        ]
    }
    
    for category, tips_list in tips.items():
        print(f"\n{category}:")
        for tip in tips_list:
            print(f"  • {tip}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Simple Chains in LangChain")
    print("="*60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set")
    
    basic_llm_chain()
    chain_with_memory()
    chain_with_variables()
    chain_with_output_key()
    chain_streaming()
    error_handling_in_chain()
    chain_performance_tips()