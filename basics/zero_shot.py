"""
Module: Zero-Shot Prompting
Description: Asking the model to perform a task without any examples
This tests the model's inherent knowledge and reasoning abilities
"""

def sentiment_analysis_zero_shot():
    """Classify sentiment without examples"""
    prompt = """
    Classify the sentiment of the following text as positive, negative, or neutral:
    
    Text: "I absolutely loved this restaurant! The food was delicious and the service was excellent."
    
    Sentiment:
    """
    return prompt


def math_problem_zero_shot():
    """Solve a math problem without examples"""
    prompt = """
    Solve the following math problem:
    
    If a train travels at 60 mph for 2.5 hours, how far does it travel?
    
    Answer:
    """
    return prompt


def question_answering_zero_shot():
    """Answer a question without examples"""
    prompt = """
    What is the capital of France?
    """
    return prompt


def code_generation_zero_shot():
    """Generate code without examples"""
    prompt = """
    Write a Python function that checks if a number is prime.
    """
    return prompt


def creative_task_zero_shot():
    """Creative task without examples"""
    prompt = """
    Write a short haiku about autumn.
    """
    return prompt


if __name__ == "__main__":
    print("=== Zero-Shot Prompting Examples ===\n")
    print("1. Sentiment Analysis:")
    print(sentiment_analysis_zero_shot())
    print("\n2. Math Problem:")
    print(math_problem_zero_shot())
    print("\n3. Question Answering:")
    print(question_answering_zero_shot())
    print("\n4. Code Generation:")
    print(code_generation_zero_shot())
    print("\n5. Creative Task:")
    print(creative_task_zero_shot())
