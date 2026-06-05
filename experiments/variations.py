"""
Prompt and Chain Variations

A/B testing different prompts and configurations.
Systematically evaluating what works best.
"""

from typing import List, Dict, Any
import json
from datetime import datetime


def ab_testing_framework() -> None:
    """
    Example 1: A/B testing framework.
    Compare different prompt variations.
    """
    print("\n=== Example 1: A/B Testing Framework ===")
    
    variations = {
        "Prompt A (Direct)": "Summarize this text in one paragraph.",
        "Prompt B (CoT)": "Think about the key points, then summarize in one paragraph.",
        "Prompt C (Examples)": "Here are examples of good summaries. Now summarize this text."
    }
    
    print("Testing variations:")
    for variant_name, prompt in variations.items():
        print(f"  {variant_name}")
    
    print("\nMetrics to compare:")
    print("  - Accuracy")
    print("  - Response time")
    print("  - Token usage")
    print("  - User satisfaction")


def temperature_tuning() -> None:
    """
    Example 2: Tuning temperature parameter.
    Finding optimal randomness level.
    """
    print("\n=== Example 2: Temperature Tuning ===")
    
    temperatures = {
        0.0: "Deterministic - same output every time",
        0.3: "Low randomness - consistent, focused",
        0.7: "Medium - balanced creativity and consistency",
        1.0: "High randomness - creative, varied"
    }
    
    print("\nTemperature effects:")
    for temp, description in temperatures.items():
        print(f"  {temp}: {description}")
    
    print("\nTesting recommendation:")
    print("  - Start with 0.7 for general use")
    print("  - Lower for factual/deterministic tasks")
    print("  - Higher for creative tasks")


def model_comparison() -> None:
    """
    Example 3: Comparing different models.
    Which model works best for your task?
    """
    print("\n=== Example 3: Model Comparison ===")
    
    models = {
        "GPT-4": {
            "Cost": "High",
            "Speed": "Medium",
            "Quality": "Best",
            "Best For": "Complex reasoning, high accuracy needed"
        },
        "GPT-3.5-turbo": {
            "Cost": "Medium",
            "Speed": "Fast",
            "Quality": "Good",
            "Best For": "General purpose, good balance"
        },
        "Open-source (Llama)": {
            "Cost": "Low",
            "Speed": "Depends on hardware",
            "Quality": "Good",
            "Best For": "Privacy-critical, cost-sensitive"
        }
    }
    
    print("\nModel comparison matrix:")
    for model, characteristics in models.items():
        print(f"\n{model}:")
        for char, value in characteristics.items():
            print(f"  {char}: {value}")


def prompt_engineering_experiments() -> None:
    """
    Example 4: Systematic prompt engineering.
    Testing different prompt strategies.
    """
    print("\n=== Example 4: Prompt Engineering Experiments ===")
    
    strategies = {
        "Strategy A: Instruction only": "Summarize the following text.",
        "Strategy B: Role assignment": "You are an expert summarizer. Summarize the following text.",
        "Strategy C: Format specification": "Summarize in 3 bullet points.",
        "Strategy D: Step-by-step": "1. Identify main topics 2. Create concise summary",
        "Strategy E: Few-shot": "Example: ... Now summarize this: ..."
    }
    
    print("\nPrompt strategies to test:")
    for strategy, example in strategies.items():
        print(f"  {strategy}")


def result_logging_framework() -> None:
    """
    Example 5: Framework for logging test results.
    Track experiments systematically.
    """
    print("\n=== Example 5: Result Logging ===")
    
    test_result = {
        "experiment_id": "exp_001",
        "timestamp": datetime.now().isoformat(),
        "variation_name": "Prompt A",
        "parameters": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 100
        },
        "metrics": {
            "accuracy": 0.92,
            "response_time_ms": 450,
            "tokens_used": 85
        },
        "results": [
            {"input": "sample text", "output": "summary", "score": 0.95},
            {"input": "sample text 2", "output": "summary 2", "score": 0.89}
        ]
    }
    
    print("Test result structure:")
    print(json.dumps(test_result, indent=2))


def statistical_significance() -> None:
    """
    Example 6: Determining statistical significance.
    Is one variation actually better?
    """
    print("\n=== Example 6: Statistical Significance ===")
    
    print("Methods to determine significance:")
    print("\n1. Sample Size:")
    print("  - Need sufficient samples (typically 30+)")
    print("  - More samples = more confidence")
    
    print("\n2. Statistical Tests:")
    print("  - t-test for continuous metrics")
    print("  - chi-square for categorical data")
    print("  - Mann-Whitney for non-normal distributions")
    
    print("\n3. Confidence Interval:")
    print("  - Calculate 95% confidence interval")
    print("  - Check if intervals overlap")
    
    print("\n4. Effect Size:")
    print("  - How large is the difference?")
    print("  - Practical significance matters too")


def multivariate_testing() -> None:
    """
    Example 7: Testing multiple variables together.
    More complex experiment designs.
    """
    print("\n=== Example 7: Multivariate Testing ===")
    
    factors = {
        "Prompt Style": ["Direct", "CoT", "Role-based"],
        "Temperature": [0.3, 0.7, 1.0],
        "Model": ["GPT-3.5", "GPT-4"]
    }
    
    total_combinations = 3 * 3 * 2
    
    print(f"\nFactors to test:")
    for factor, values in factors.items():
        print(f"  {factor}: {', '.join(map(str, values))}")
    
    print(f"\nTotal combinations: {total_combinations}")
    print("\nDesign of Experiments (DoE) techniques:")
    print("  - Factorial design")
    print("  - Fractional factorial (reduce combinations)")
    print("  - Response surface methodology")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Prompt and Chain Variations")
    print("="*60)
    
    ab_testing_framework()
    temperature_tuning()
    model_comparison()
    prompt_engineering_experiments()
    result_logging_framework()
    statistical_significance()
    multivariate_testing()