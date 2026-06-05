"""
Advanced Prompt Customization

Advanced techniques for prompt engineering:
- Chain-of-Thought prompting
- Prompt optimization
- Dynamic prompt construction
- Multi-step reasoning
"""

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from typing import List, Dict


def chain_of_thought_prompting() -> None:
    """
    Example 1: Chain-of-Thought (CoT) prompting.
    Ask the model to show its reasoning step by step.
    """
    print("\n=== Example 1: Chain-of-Thought Prompting ===")
    
    cot_prompt = PromptTemplate.from_template(
        """Question: {question}

Let's think step by step.

Step 1: Understand the problem
Step 2: Identify key information
Step 3: Solve step by step
Step 4: Verify the answer

Answer:"""
    )
    
    example_question = "If John has 10 apples and gives away 3, then buys 5 more, how many does he have?"
    prompt = cot_prompt.format(question=example_question)
    print(f"CoT Prompt:\n{prompt}")


def self_consistency_prompting() -> None:
    """
    Example 2: Self-consistency prompting.
    Generate multiple outputs and find consensus.
    """
    print("\n=== Example 2: Self-Consistency Prompting ===")
    
    prompt = PromptTemplate.from_template(
        """Question: {question}

Generate {num_samples} different approaches to solve this problem.
For each approach:
1. Explain your reasoning
2. Show the solution
3. State your confidence (high/medium/low)

After all approaches, identify the most likely correct answer."""
    )
    
    formatted = prompt.format(
        question="What is 47 * 3?",
        num_samples=3
    )
    print(f"Self-consistency prompt:\n{formatted}")


def role_based_prompting() -> None:
    """
    Example 3: Role-based prompting.
    Assign specific roles to improve quality.
    """
    print("\n=== Example 3: Role-Based Prompting ===")
    
    roles = {
        "expert": "You are a world-class expert in {domain}.",
        "teacher": "You are a patient teacher explaining to a beginner.",
        "journalist": "You are an investigative journalist seeking the truth.",
        "lawyer": "You are a careful lawyer reviewing documents for accuracy."
    }
    
    prompt_template = """Role: {role_description}

Task: {task}

Provide a {quality_level} quality response.

Response:"""
    
    for role_name, role_desc in roles.items():
        prompt = PromptTemplate.from_template(prompt_template).format(
            role_description=role_desc,
            task="Explain quantum computing",
            quality_level="comprehensive"
        )
        print(f"\n{role_name.title()} role prompt (first 100 chars):")
        print(f"  {prompt[:100]}...")


def constraint_based_prompting() -> None:
    """
    Example 4: Constraint-based prompting.
    Specify strict constraints for output.
    """
    print("\n=== Example 4: Constraint-Based Prompting ===")
    
    constraints_prompt = PromptTemplate.from_template(
        """Task: {task}

Constraints:
1. Response must be exactly {word_count} words
2. Must not mention: {avoid_topics}
3. Must be written in {tone} tone
4. Include: {required_elements}
5. Format: {format_requirement}

Response:"""
    )
    
    prompt = constraints_prompt.format(
        task="Write about artificial intelligence",
        word_count=100,
        avoid_topics="job losses, bias",
        tone="professional",
        required_elements="definition, applications, future",
        format_requirement="paragraph format"
    )
    print(f"Constraint-based prompt:\n{prompt}")


def structured_output_prompting() -> None:
    """
    Example 5: Prompts designed for structured output.
    Get JSON or formatted data from the model.
    """
    print("\n=== Example 5: Structured Output Prompting ===")
    
    json_prompt = PromptTemplate.from_template(
        """Extract information from the following text and respond in JSON format.

Text: {text}

Extract:
- name: The person's name
- age: Their age if mentioned
- location: Where they're from
- occupation: Their job

Respond ONLY with valid JSON, no other text:"""
    )
    
    prompt = json_prompt.format(
        text="John Smith, 35, from New York, is a software engineer."
    )
    print(f"JSON extraction prompt:\n{prompt}")


def instruction_following_prompting() -> None:
    """
    Example 6: Improving instruction following.
    Clear, detailed instructions lead to better results.
    """
    print("\n=== Example 6: Instruction Following ===")
    
    # Poor instruction
    poor = "Summarize this: {text}"
    
    # Better instruction
    better = PromptTemplate.from_template(
        """Please summarize the following text according to these criteria:

1. Length: 2-3 sentences
2. Focus: Main ideas only, not details
3. Style: Clear and concise
4. Audience: For someone unfamiliar with the topic

Text: {text}

Summary:"""
    )
    
    print("\nPoor instruction: 'Summarize this'")
    print("\nBetter instruction with detailed criteria")
    print("\nKey improvements:")
    print("  - Specific length requirements")
    print("  - Clear focus")
    print("  - Style guidance")
    print("  - Target audience")


def dynamic_prompt_construction() -> None:
    """
    Example 7: Dynamically constructing prompts.
    Build prompts based on runtime conditions.
    """
    print("\n=== Example 7: Dynamic Prompt Construction ===")
    
    def build_analysis_prompt(data_type: str, analysis_depth: str) -> str:
        """
        Build a prompt based on parameters.
        """
        depths = {
            "shallow": "provide a brief overview",
            "medium": "provide analysis with examples",
            "deep": "provide thorough analysis with detailed reasoning"
        }
        
        types = {
            "text": "Analyze the following text",
            "code": "Review the following code",
            "data": "Analyze the following dataset"
        }
        
        prompt = f"{types.get(data_type, 'Analyze the following')}. Please {depths.get(analysis_depth, 'provide analysis')}."
        return prompt
    
    # Generate different prompts based on parameters
    print("\nDynamic prompt examples:")
    print(f"Text + Deep: {build_analysis_prompt('text', 'deep')}")
    print(f"Code + Shallow: {build_analysis_prompt('code', 'shallow')}")
    print(f"Data + Medium: {build_analysis_prompt('data', 'medium')}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Advanced Prompt Customization")
    print("="*60)
    
    chain_of_thought_prompting()
    self_consistency_prompting()
    role_based_prompting()
    constraint_based_prompting()
    structured_output_prompting()
    instruction_following_prompting()
    dynamic_prompt_construction()