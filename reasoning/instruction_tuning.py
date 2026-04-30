"""
Module: Instruction Tuning
Description: Refining and optimizing prompts for better model alignment and performance
Learn how to iteratively improve your prompts
"""

def basic_instruction_v1():
    """First version - too vague"""
    return "Tell me about Python"


def basic_instruction_v2():
    """Improved - more specific"""
    return "Explain what Python is and why it's useful for beginners"


def basic_instruction_v3():
    """Optimized - clear context and format"""
    return """
    Explain Python in a way suitable for someone with no programming experience.
    Include:
    - What Python is
    - Why beginners should learn it
    - One simple code example
    Keep the explanation to 3-4 sentences.
    """


def summarization_v1():
    """Poor - unclear requirements"""
    return "Summarize this: The quick brown fox jumps over the lazy dog"


def summarization_v2():
    """Better - specifies length"""
    return "Summarize in 2-3 sentences: The quick brown fox jumps over the lazy dog"


def summarization_v3():
    """Optimized - clear output format"""
    return """
    Summarize the following text in exactly 2 sentences:
    
    Text: "The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet."
    
    Summary:
    """


def instruction_refinement_guide():
    """Guide for refining instructions"""
    return """
    Tips for Instruction Tuning:
    
    1. Be Specific
       - Vague: "Write a story"
       - Better: "Write a 100-word science fiction story about time travel"
    
    2. Provide Context
       - Vague: "Translate this"
       - Better: "You are a professional translator. Translate to Spanish:"
    
    3. Specify Output Format
       - Vague: "List the benefits"
       - Better: "List 3-5 benefits as bullet points"
    
    4. Use Examples
       - Vague: "Categorize this text"
       - Better: "Categorize as positive/negative/neutral. Example: 'Great movie!' = Positive"
    
    5. Set Constraints
       - Vague: "Explain quantum computing"
       - Better: "Explain quantum computing in 50 words using simple language"
    
    6. Clarify Audience
       - Vague: "Explain AI"
       - Better: "Explain AI to a 10-year-old child"
    """


def iterative_improvement_example():
    """Show an iterative improvement process"""
    return """
    Example: Creating a Recipe Summarizer
    
    Version 1 (Too Simple):
    "Summarize this recipe"
    
    Version 2 (More Specific):
    "Summarize this recipe in bullet points"
    
    Version 3 (Better Formatted):
    "Summarize the recipe using:
     - Ingredients (3-5 main items)
     - Steps (3-4 key steps)"
    
    Version 4 (Optimized with Example):
    "You are a professional recipe editor. Summarize the recipe with:
     - Ingredients: List 3-5 main ingredients
     - Steps: Condense to 3-4 key steps
     
     Example format:
     INGREDIENTS: flour, eggs, milk
     STEPS: Mix, bake, cool"
    """


if __name__ == "__main__":
    print("=== Instruction Tuning Examples ===\n")
    print("Basic Instruction Evolution:")
    print(f"V1: {basic_instruction_v1()}")
    print(f"V2: {basic_instruction_v2()}")
    print(f"V3:\n{basic_instruction_v3()}")
    print("\n" + "="*50)
    print("\nSummarization Evolution:")
    print(f"V1: {summarization_v1()}")
    print(f"V2: {summarization_v2()}")
    print(f"V3:\n{summarization_v3()}")
    print("\n" + "="*50)
    print("\nRefinement Guide:")
    print(instruction_refinement_guide())
    print("\n" + "="*50)
    print("\nIterative Improvement:")
    print(iterative_improvement_example())
