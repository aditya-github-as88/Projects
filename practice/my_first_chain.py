"""
My First LangChain

A beginner-friendly guide to building your first LangChain chain.
Step-by-step tutorial with explanations.
"""

import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI


def setup_environment() -> None:
    """
    Step 1: Set up your environment.
    Install dependencies and configure API keys.
    """
    print("\n=== Step 1: Setup ===")
    print("""
Before getting started:

1. Install LangChain:
   pip install langchain

2. Install OpenAI integration:
   pip install langchain-openai openai

3. Set OPENAI_API_KEY:
   export OPENAI_API_KEY='your-key-here'

4. Verify installation:
   python -c "import langchain; print(langchain.__version__)"
    """)


def create_your_first_chain() -> None:
    """
    Step 2: Create your first chain.
    Combine LLM + Prompt in a chain.
    """
    print("\n=== Step 2: Create Your First Chain ===")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        return
    
    # Step 1: Initialize LLM
    print("\nStep 2a: Initialize the LLM")
    llm = OpenAI(
        api_key=api_key,
        temperature=0.7  # Control creativity (0=deterministic, 1=creative)
    )
    print("  ✓ LLM initialized")
    
    # Step 2: Create Prompt Template
    print("\nStep 2b: Create prompt template")
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Write a short, interesting fact about {topic}."
    )
    print(f"  ✓ Prompt created: {prompt.template}")
    
    # Step 3: Create Chain
    print("\nStep 2c: Create the chain")
    chain = LLMChain(llm=llm, prompt=prompt)
    print("  ✓ Chain created successfully")
    
    # Step 4: Run the chain
    print("\nStep 2d: Run the chain")
    # result = chain.invoke({"topic": "Python"})
    # print(f"  Result: {result['text']}")
    print("  (Uncomment to execute with API call)")


def understanding_chain_components() -> None:
    """
    Step 3: Understanding the components.
    What does each part do?
    """
    print("\n=== Step 3: Chain Components ===")
    
    components = {
        "LLM (Language Model)": {
            "Role": "Generates text responses",
            "Parameters": "temperature, max_tokens, model",
            "Example": "OpenAI, HuggingFace, custom"
        },
        "Prompt Template": {
            "Role": "Structures user input",
            "Parameters": "input_variables, template",
            "Example": "'Write about {topic}'"
        },
        "Chain": {
            "Role": "Connects prompt and LLM",
            "Parameters": "llm, prompt, output_key",
            "Example": "LLMChain, SequentialChain"
        }
    }
    
    print("\nChain flow: Input -> Prompt -> LLM -> Output")
    print("\nComponent details:")
    for component, details in components.items():
        print(f"\n{component}:")
        for key, value in details.items():
            print(f"  {key}: {value}")


def exercise_1_simple_chain() -> None:
    """
    Exercise 1: Build a simple chain.
    Create a chain that answers questions.
    """
    print("\n=== Exercise 1: Simple Q&A Chain ===")
    
    code = '''
# Create a Q&A chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

llm = OpenAI(api_key="your-key")

prompt = PromptTemplate(
    input_variables=["question"],
    template="Answer this question: {question}"
)

chain = LLMChain(llm=llm, prompt=prompt)

# Use it
result = chain.invoke({"question": "What is Python?"})
print(result["text"])
    '''
    
    print(code)


def exercise_2_multiple_variables() -> None:
    """
    Exercise 2: Chain with multiple variables.
    Create a chain that uses multiple inputs.
    """
    print("\n=== Exercise 2: Multiple Variables ===")
    
    code = '''
# Chain with multiple inputs
prompt = PromptTemplate(
    input_variables=["language", "concept"],
    template="Explain {concept} in {language}"
)

chain = LLMChain(llm=llm, prompt=prompt)

result = chain.invoke({
    "language": "simple terms",
    "concept": "machine learning"
})
print(result["text"])
    '''
    
    print(code)


def exercise_3_customize_temperature() -> None:
    """
    Exercise 3: Experiment with temperature.
    See how temperature affects creativity.
    """
    print("\n=== Exercise 3: Temperature Tuning ===")
    
    code = '''
# Try different temperatures
temps = [0.0, 0.5, 1.0]

for temp in temps:
    llm = OpenAI(temperature=temp)
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"topic": "AI"})
    print(f"Temperature {temp}: {result['text']}")
    '''
    
    print(code)


def common_mistakes() -> None:
    """
    Common mistakes beginners make.
    """
    print("\n=== Common Mistakes ===")
    
    mistakes = {
        "Forgot API Key": {
            "Problem": "AuthenticationError when running chain",
            "Solution": "Set OPENAI_API_KEY environment variable"
        },
        "Wrong Variable Names": {
            "Problem": "KeyError in format",
            "Solution": "Template variables must match invoke() keys"
        },
        "Missing Imports": {
            "Problem": "ModuleNotFoundError",
            "Solution": "pip install langchain langchain-openai"
        },
        "Not Handling Errors": {
            "Problem": "Script crashes on API error",
            "Solution": "Use try/except blocks"
        }
    }
    
    print("\nCommon issues and solutions:")
    for mistake, details in mistakes.items():
        print(f"\n{mistake}:")
        for key, value in details.items():
            print(f"  {key}: {value}")


def next_steps() -> None:
    """
    What to learn next.
    Progression from beginner to advanced.
    """
    print("\n=== Next Steps ===")
    
    progression = {
        "Beginner": [
            "Simple chains (LLMChain)",
            "Basic prompts (PromptTemplate)",
            "Understanding temperature/tokens"
        ],
        "Intermediate": [
            "Sequential chains",
            "Memory and conversation",
            "Output parsers",
            "Few-shot prompting"
        ],
        "Advanced": [
            "Custom chains",
            "Agents and tools",
            "Fine-tuning",
            "Vector databases",
            "Production deployment"
        ]
    }
    
    print("\nLearning progression:")
    for level, topics in progression.items():
        print(f"\n{level}:")
        for topic in topics:
            print(f"  → {topic}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("My First LangChain - Beginner's Guide")
    print("="*60)
    
    setup_environment()
    create_your_first_chain()
    understanding_chain_components()
    exercise_1_simple_chain()
    exercise_2_multiple_variables()
    exercise_3_customize_temperature()
    common_mistakes()
    next_steps()