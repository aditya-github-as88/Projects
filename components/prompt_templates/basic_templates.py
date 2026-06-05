"""
Basic Prompt Templates

PromptTemplate is the fundamental way to create reusable prompts.
They allow dynamic variable substitution for consistent prompting.
"""

from langchain.prompts import PromptTemplate
from typing import Dict, List


def simple_template() -> None:
    """
    Example 1: Simple prompt template with one variable.
    """
    print("\n=== Example 1: Simple Template ===")
    
    template = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in simple terms for a beginner."
    )
    
    # Format the template
    prompt = template.format(topic="Machine Learning")
    print(f"Template: {template.template}")
    print(f"Formatted prompt:\n{prompt}")


def multiple_variables() -> None:
    """
    Example 2: Template with multiple variables.
    """
    print("\n=== Example 2: Multiple Variables ===")
    
    template = PromptTemplate(
        input_variables=["question", "context"],
        template="""Context: {context}

Question: {question}

Answer:"""
    )
    
    prompt = template.format(
        context="Paris is the capital of France.",
        question="What is the capital of France?"
    )
    print(f"Formatted prompt:\n{prompt}")


def from_template_string() -> None:
    """
    Example 3: Creating template from a template string.
    Simpler way to create templates.
    """
    print("\n=== Example 3: From Template String ===")
    
    template = PromptTemplate.from_template(
        "Translate the following text to {language}:\n\n{text}"
    )
    
    prompt = template.format(
        language="Spanish",
        text="Hello, how are you?"
    )
    print(f"Formatted prompt:\n{prompt}")


def partial_variables() -> None:
    """
    Example 4: Partially filling template variables.
    Useful when some variables are known ahead of time.
    """
    print("\n=== Example 4: Partial Variables ===")
    
    template = PromptTemplate(
        input_variables=["topic"],
        template="You are an expert in {domain}. Explain {topic}.",
        partial_variables={"domain": "Artificial Intelligence"}
    )
    
    # Only need to provide 'topic', 'domain' is already set
    prompt = template.format(topic="Neural Networks")
    print(f"Formatted prompt:\n{prompt}")


def validation_example() -> None:
    """
    Example 5: Template validation.
    Ensure all required variables are provided.
    """
    print("\n=== Example 5: Template Validation ===")
    
    template = PromptTemplate(
        input_variables=["name", "age"],
        template="My name is {name} and I am {age} years old."
    )
    
    # Check required variables
    print(f"Required input variables: {template.input_variables}")
    
    # This will work
    try:
        prompt = template.format(name="Alice", age=30)
        print(f"Valid prompt: {prompt}")
    except Exception as e:
        print(f"Error: {e}")
    
    # This will fail (missing variable)
    try:
        prompt = template.format(name="Bob")
        print(f"Invalid prompt: {prompt}")
    except Exception as e:
        print(f"Error caught: Missing required variable")


def reusable_templates() -> None:
    """
    Example 6: Creating reusable template library.
    Store and reuse templates across your application.
    """
    print("\n=== Example 6: Reusable Templates ===")
    
    # Template library
    templates = {
        "summarize": PromptTemplate.from_template(
            "Summarize the following text in 2-3 sentences:\n\n{text}"
        ),
        "translate": PromptTemplate.from_template(
            "Translate to {language}:\n\n{text}"
        ),
        "qa": PromptTemplate.from_template(
            "Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        ),
        "sentiment": PromptTemplate.from_template(
            "Analyze sentiment of this text (positive/negative/neutral):\n\n{text}"
        )
    }
    
    # Use templates
    text = "I really enjoyed this movie!"
    print(f"Summarize: {templates['summarize'].format(text=text)}")
    print(f"\nSentiment: {templates['sentiment'].format(text=text)}")


def with_chain() -> None:
    """
    Example 7: Using templates with chains.
    Templates are the bridge between input and LLM.
    """
    print("\n=== Example 7: Template with Chain ===")
    
    from langchain.chains import LLMChain
    from langchain_openai import OpenAI
    import os
    
    # Create template
    template = PromptTemplate(
        input_variables=["product"],
        template="What are 3 features of {product}?"
    )
    
    # Would use with chain like this:
    # llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # chain = LLMChain(llm=llm, prompt=template)
    # result = chain.invoke({"product": "Python"})
    
    print("Chain usage (requires OpenAI API key):")
    print("  llm = OpenAI(api_key=...)")
    print("  chain = LLMChain(llm=llm, prompt=template)")
    print("  result = chain.invoke({\"product\": \"Python\"})")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Basic Prompt Templates")
    print("="*60)
    
    simple_template()
    multiple_variables()
    from_template_string()
    partial_variables()
    validation_example()
    reusable_templates()
    with_chain()