"""
Chain of Thought Reasoning

Prompting techniques that ask the model to think step by step.
Improves reasoning and accuracy on complex problems.
"""

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI
import os
from typing import Dict


def basic_chain_of_thought() -> None:
    """
    Example 1: Basic Chain of Thought (CoT) prompting.
    Ask model to show reasoning before answering.
    """
    print("\n=== Example 1: Basic Chain of Thought ===")
    
    prompt = PromptTemplate(
        input_variables=["question"],
        template="""Question: {question}

Let's think step by step.

Step 1: What is being asked?
Step 2: What information do we need?
Step 3: How do we solve it?
Step 4: What is the answer?

Answer:"""
    )
    
    example_question = "If there are 3 apples and I add 5 more, then eat 2, how many are left?"
    formatted = prompt.format(question=example_question)
    print(f"CoT Prompt:\n{formatted}")


def math_problem_solving() -> None:
    """
    Example 2: CoT for math problem solving.
    Break down mathematical problems.
    """
    print("\n=== Example 2: Math Problem Solving ===")
    
    prompt = PromptTemplate(
        input_variables=["problem"],
        template="""Problem: {problem}

Let's solve this step by step:

Step 1: Identify what we know
Step 2: Identify what we want to find
Step 3: Choose the right formula/method
Step 4: Calculate
Step 5: Verify the answer

Solution:"""
    )
    
    example = "A rectangle has length 10 and width 5. What is its area?"
    print(f"Example: {example}")
    print(f"Steps would be: Identify values -> Apply formula -> Calculate -> Verify")


def logical_reasoning() -> None:
    """
    Example 3: CoT for logical reasoning.
    Complex logical problems.
    """
    print("\n=== Example 3: Logical Reasoning ===")
    
    prompt = PromptTemplate(
        input_variables=["scenario"],
        template="""Scenario: {scenario}

Let's reason through this:

1. Given facts:
2. What we can deduce:
3. Intermediate conclusions:
4. Final answer:

Conclusion:"""
    )
    
    example_scenario = "All dogs are animals. Fido is a dog. What can we conclude about Fido?"
    print(f"Example logic problem: {example_scenario}")


def complex_problem_decomposition() -> None:
    """
    Example 4: Breaking down complex problems.
    Decompose into manageable sub-problems.
    """
    print("\n=== Example 4: Problem Decomposition ===")
    
    prompt = PromptTemplate(
        input_variables=["problem"],
        template="""Complex Problem: {problem}

Decompose this problem:

1. Main problem can be broken into:
   a) Sub-problem 1
   b) Sub-problem 2
   c) Sub-problem 3

2. Solve each sub-problem:
   a) Sub-problem 1 solution
   b) Sub-problem 2 solution
   c) Sub-problem 3 solution

3. Combine solutions to solve main problem

Final Solution:"""
    )
    
    print("Complex problems are easier when broken down")
    print("Approach: Divide -> Conquer -> Combine")


def verification_and_correction() -> None:
    """
    Example 5: CoT with verification step.
    Check and correct reasoning.
    """
    print("\n=== Example 5: Verification ===")
    
    prompt = PromptTemplate(
        input_variables=["question"],
        template="""Question: {question}

Think through this step by step:

Initial reasoning:
[Show your work]

Verification:
- Does this make sense?
- Are there any errors?
- Did we consider all factors?

Corrected answer:"""
    )
    
    print("Verification step ensures accuracy")
    print("Catches reasoning errors before finalizing answer")


def few_shot_cot() -> None:
    """
    Example 6: Few-shot Chain of Thought.
    Show examples of CoT reasoning.
    """
    print("\n=== Example 6: Few-Shot CoT ===")
    
    from langchain.prompts import FewShotPromptTemplate
    
    examples = [
        {
            "question": "If John has 5 apples and gives 2 away, how many does he have?",
            "reasoning": "John starts with 5. He gives away 2. So 5 - 2 = 3.",
            "answer": "3 apples"
        },
        {
            "question": "Mary has 3 times as many books as John. If John has 4, how many does Mary have?",
            "reasoning": "John has 4 books. Mary has 3 times as many. So 4 * 3 = 12.",
            "answer": "12 books"
        }
    ]
    
    print("Few-shot examples help guide the model:")
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"  Q: {example['question']}")
        print(f"  Reasoning: {example['reasoning']}")
        print(f"  A: {example['answer']}")


def best_practices() -> None:
    """
    Example 7: Best practices for Chain of Thought.
    """
    print("\n=== Example 7: Best Practices ===")
    
    practices = {
        "Prompting": [
            "Use 'Let's think step by step'",
            "Break problems into clear steps",
            "Ask for intermediate reasoning",
            "Verify final answer"
        ],
        "Problem Selection": [
            "Works best for complex reasoning",
            "Good for math, logic, planning",
            "Less needed for simple facts",
            "Helps with multi-step problems"
        ],
        "Optimization": [
            "Reduces token usage for accuracy gain",
            "Combine with few-shot examples",
            "Use shorter steps for simpler problems",
            "Cache complex reasoning patterns"
        ],
        "Evaluation": [
            "Check if reasoning is correct",
            "Verify answer independently",
            "Look for logical fallacies",
            "Test on diverse problems"
        ]
    }
    
    for category, tips in practices.items():
        print(f"\n{category}:")
        for tip in tips:
            print(f"  ✓ {tip}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Chain of Thought Reasoning")
    print("="*60)
    
    basic_chain_of_thought()
    math_problem_solving()
    logical_reasoning()
    complex_problem_decomposition()
    verification_and_correction()
    few_shot_cot()
    best_practices()