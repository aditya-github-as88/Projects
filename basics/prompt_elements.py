"""
Module: Prompt Elements
Description: Demonstrates the core elements of effective prompts
- Instruction: What the model should do
- Context: Background information
- Input: The data to process
- Output Indicator: Format/type of expected output
"""

def example_instruction():
    """Basic instruction prompt"""
    prompt = "Summarize the following text in 3 sentences."
    return prompt


def example_context():
    """Prompt with context"""
    context = """
    You are a professional data analyst with expertise in business intelligence.
    Your goal is to provide insights that are clear and actionable.
    """
    instruction = "Analyze the quarterly sales data below:"
    return context + instruction


def example_input_output():
    """Complete prompt with all elements"""
    prompt = {
        "instruction": "Translate the following English text to Spanish",
        "context": "You are a professional translator with 10 years of experience",
        "input": "The weather is beautiful today.",
        "output_indicator": "Provide only the Spanish translation without explanation."
    }
    return prompt


def complete_example():
    """Full prompt with all elements combined"""
    return """
    You are an expert customer service representative. Your role is to help customers solve problems quickly and politely.
    
    INSTRUCTION: Respond to the following customer inquiry
    
    CUSTOMER INPUT: I ordered a package 3 weeks ago and it hasn't arrived yet. What should I do?
    
    EXPECTED OUTPUT: A helpful, empathetic response that offers solutions and next steps.
    """


if __name__ == "__main__":
    print("=== Prompt Elements Examples ===\n")
    print("1. Basic Instruction:")
    print(example_instruction())
    print("\n2. With Context:")
    print(example_context())
    print("\n3. With Input/Output:")
    print(example_input_output())
    print("\n4. Complete Example:")
    print(complete_example())
