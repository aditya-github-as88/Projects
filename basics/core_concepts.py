"""
Core Concepts in LangChain

Understanding the fundamental building blocks:
1. Language Models (LLMs)
2. Prompts
3. Chains
4. Memory
5. Agents
"""

from typing import Dict, List


class LLMConcept:
    """
    Concept 1: Language Models (LLMs)
    
    LLMs are the core of LangChain. They take text input and produce text output.
    Types:
    - OpenAI (GPT-3.5, GPT-4)
    - Open source (LLaMA, Mistral)
    - Custom models
    """
    
    explanation = """
    LLMs in LangChain:
    - Abstract interface for different models
    - Consistent API across providers
    - Support for streaming and async calls
    - Built-in token counting
    """
    
    example_code = """
    from langchain_openai import OpenAI
    
    llm = OpenAI(temperature=0.7)
    response = llm.invoke("What is AI?")
    """


class PromptConcept:
    """
    Concept 2: Prompts
    
    Prompts are the way you communicate with LLMs.
    They structure your input in a consistent, reusable way.
    """
    
    explanation = """
    Prompts in LangChain:
    - PromptTemplate: Basic templating with variables
    - FewShotPromptTemplate: Include examples for better results
    - ChatPromptTemplate: For conversation models
    - Dynamic prompts: Create prompts programmatically
    """
    
    example_code = """
    from langchain.prompts import PromptTemplate
    
    # Simple template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms."
    )
    
    # Use it
    result = prompt.format(topic="Machine Learning")
    """


class ChainConcept:
    """
    Concept 3: Chains
    
    Chains combine LLMs with other components to create workflows.
    They sequence operations together.
    """
    
    explanation = """
    Chains in LangChain:
    - LLMChain: Connect LLM with prompt
    - SequentialChain: Run multiple chains in sequence
    - RouterChain: Route to different chains based on input
    - Custom chains: Build your own workflows
    
    Benefits:
    - Reusable components
    - Clear data flow
    - Easy debugging
    """
    
    example_code = """
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain_openai import OpenAI
    
    llm = OpenAI()
    prompt = PromptTemplate(template="...", input_variables=[...])
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.invoke({"input": "value"})
    """


class MemoryConcept:
    """
    Concept 4: Memory
    
    Memory enables conversational interactions by keeping track of history.
    Different memory types serve different purposes.
    """
    
    explanation = """
    Memory Types:
    - ConversationBufferMemory: Stores all messages (can get large)
    - ConversationSummaryMemory: Summarizes old messages
    - ConversationBufferWindowMemory: Keeps only recent messages
    - Entity memory: Tracks specific entities mentioned
    """
    
    example_code = """
    from langchain.memory import ConversationBufferMemory
    
    memory = ConversationBufferMemory()
    memory.save_context({"input": "Hi!"}, {"output": "Hello!"})
    
    # Later, retrieve history
    history = memory.load_memory_variables({})
    """


class AgentConcept:
    """
    Concept 5: Agents
    
    Agents combine LLMs with tools to create interactive systems.
    The LLM decides which tools to use and in what order.
    """
    
    explanation = """
    Agents in LangChain:
    - Zero-shot agents: Decide tool use on the fly
    - ReAct agents: Reason and act iteratively
    - Custom agents: Build your own agent logic
    
    Process:
    1. User provides input
    2. Agent thinks about which tool to use
    3. Agent calls the tool
    4. Agent gets result and decides next step
    5. Repeat until done
    """
    
    example_code = """
    from langchain.agents import initialize_agent, Tool
    from langchain_openai import OpenAI
    
    tools = [Tool(name="...", func=..., description="...")]
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
    result = agent.run("Your question")
    """


class OutputParserConcept:
    """
    Concept 6: Output Parsers
    
    Output parsers extract structured data from LLM responses.
    They convert unstructured text into usable format.
    """
    
    explanation = """
    Output Parsers:
    - JsonOutputParser: Extract JSON from response
    - StructuredOutputParser: Parse structured formats
    - Custom parsers: Build your own parsing logic
    
    Benefits:
    - Structured data from unstructured LLM outputs
    - Error handling and validation
    - Easy integration with downstream systems
    """
    
    example_code = """
    from langchain.output_parsers import JsonOutputParser
    
    parser = JsonOutputParser()
    prompt = PromptTemplate(template="...", output_parser=parser)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    result = chain.invoke({...})  # Returns parsed JSON
    """


def print_concept_overview() -> None:
    """
    Print an overview of all core concepts.
    """
    concepts = [
        ("LLMs", LLMConcept),
        ("Prompts", PromptConcept),
        ("Chains", ChainConcept),
        ("Memory", MemoryConcept),
        ("Agents", AgentConcept),
        ("Output Parsers", OutputParserConcept)
    ]
    
    print("\n" + "="*60)
    print("LangChain Core Concepts Overview")
    print("="*60)
    
    for name, concept_class in concepts:
        print(f"\n### {name} ###")
        print(concept_class.explanation)
        print(f"\nExample Code:\n{concept_class.example_code}")
        print("-" * 60)


if __name__ == "__main__":
    print_concept_overview()