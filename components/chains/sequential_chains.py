"""
Sequential Chains

Chains that execute multiple steps in sequence.
Output of one step becomes input to the next.
"""

import os
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI


def simple_sequential_chain() -> None:
    """
    Example 1: SimpleSequentialChain.
    Simplest form - output of first chain is input to second.
    """
    print("\n=== Example 1: SimpleSequentialChain ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # First chain: Generate topic
    prompt1 = PromptTemplate(
        input_variables=["input"],
        template="Generate a topic about {input}."
    )
    chain1 = LLMChain(llm=llm, prompt=prompt1)
    
    # Second chain: Write about topic
    prompt2 = PromptTemplate(
        input_variables=["input"],
        template="Write a paragraph about {input}."
    )
    chain2 = LLMChain(llm=llm, prompt=prompt2)
    
    # Combine into sequential chain
    sequential_chain = SimpleSequentialChain(
        chains=[chain1, chain2],
        verbose=False
    )
    
    print("SimpleSequentialChain flow:")
    print("  Input -> Chain1 -> Chain2 -> Output")
    # result = sequential_chain.invoke("technology")
    # print(f"Result: {result['output']}")


def complex_sequential_chain() -> None:
    """
    Example 2: SequentialChain with named outputs.
    More flexible - control which outputs are used.
    """
    print("\n=== Example 2: Complex SequentialChain ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Chain 1: Identify topic category
    prompt1 = PromptTemplate(
        input_variables=["topic"],
        template="What category does {topic} belong to? (Science, Art, Technology, etc.)",
        output_key="category"
    )
    chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="category")
    
    # Chain 2: Generate key points
    prompt2 = PromptTemplate(
        input_variables=["topic", "category"],
        template="Generate 3 key points about {topic} in {category}.",
        output_key="key_points"
    )
    chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="key_points")
    
    # Chain 3: Create summary
    prompt3 = PromptTemplate(
        input_variables=["topic", "category", "key_points"],
        template="Write a summary of {topic} ({category}) using these points: {key_points}",
        output_key="summary"
    )
    chain3 = LLMChain(llm=llm, prompt=prompt3, output_key="summary")
    
    # Combine into sequential chain
    sequential_chain = SequentialChain(
        chains=[chain1, chain2, chain3],
        input_variables=["topic"],
        output_variables=["category", "key_points", "summary"],
        verbose=False
    )
    
    print("Complex sequential chain with named outputs:")
    print("  Input: topic")
    print("  -> Chain1 output: category")
    print("  -> Chain2 output: key_points")
    print("  -> Chain3 output: summary")


def conditional_chain() -> None:
    """
    Example 3: Conditional chain execution.
    Execute different chains based on input.
    """
    print("\n=== Example 3: Conditional Chains ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Different chains for different purposes
    summarize_prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize: {text}"
    )
    summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)
    
    translate_prompt = PromptTemplate(
        input_variables=["text"],
        template="Translate to Spanish: {text}"
    )
    translate_chain = LLMChain(llm=llm, prompt=translate_prompt)
    
    def execute_conditional(task_type: str, text: str):
        if task_type == "summarize":
            return summarize_chain.invoke({"text": text})
        elif task_type == "translate":
            return translate_chain.invoke({"text": text})
        else:
            return {"error": "Unknown task type"}
    
    print("Conditional chain example:")
    print("  - If task == 'summarize': use summarize_chain")
    print("  - If task == 'translate': use translate_chain")


def parallel_chains() -> None:
    """
    Example 4: Running chains in parallel.
    Execute multiple chains concurrently.
    """
    print("\n=== Example 4: Parallel Chains ===")
    
    import asyncio
    
    print("Parallel execution patterns:")
    print("  - Use asyncio for concurrent execution")
    print("  - Combine results from multiple chains")
    print("  - Better performance for independent tasks")
    print("\nExample:")
    print("  chain1.ainvoke(inputs1) - async call")
    print("  chain2.ainvoke(inputs2) - async call")
    print("  results = await asyncio.gather(...)")


def chain_composition() -> None:
    """
    Example 5: Composing chains together.
    Reuse chains as building blocks.
    """
    print("\n=== Example 5: Chain Composition ===")
    
    print("Benefits of chain composition:")
    print("  - Reusable components")
    print("  - Cleaner code organization")
    print("  - Easier testing")
    print("  - Modular architecture")
    
    print("\nPattern:")
    print("  1. Create atomic chains (single responsibility)")
    print("  2. Combine into sequential chains")
    print("  3. Further compose into higher-level chains")
    print("  4. Mix and match for different use cases")


def debugging_chains() -> None:
    """
    Example 6: Debugging chain execution.
    """
    print("\n=== Example 6: Debugging Chains ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["input"],
        template="Respond to: {input}"
    )
    
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)  # Enable verbose mode
    
    print("Debugging techniques:")
    print("  - Set verbose=True for detailed logs")
    print("  - Print intermediate results")
    print("  - Test chains individually first")
    print("  - Use output_key for clarity")
    print("  - Monitor token usage")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Sequential Chains in LangChain")
    print("="*60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set")
    
    simple_sequential_chain()
    complex_sequential_chain()
    conditional_chain()
    parallel_chains()
    chain_composition()
    debugging_chains()