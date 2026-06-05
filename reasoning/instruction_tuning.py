"""
Instruction Tuning

Fine-tuning models on instruction-following tasks.
Improving model ability to follow specific instructions.
"""

from typing import List, Dict


def instruction_tuning_overview() -> None:
    """
    Example 1: What is instruction tuning?
    Fine-tuning on instruction-output pairs.
    """
    print("\n=== Example 1: Instruction Tuning Overview ===")
    
    overview = '''Instruction Tuning:
    
    Traditional fine-tuning:
    (Text, Label) pairs -> Model learns to classify
    
    Instruction tuning:
    (Instruction, Response) pairs -> Model learns to follow instructions
    
    Examples:
    - ("Summarize this:", text) -> (summary)
    - ("Classify sentiment:", review) -> (positive/negative)
    - ("Answer this question:", question) -> (answer)
    
    Benefits:
    - Better instruction following
    - More versatile models
    - Works across diverse tasks
    '''
    
    print(overview)


def dataset_creation() -> None:
    """
    Example 2: Creating instruction tuning datasets.
    How to structure training data.
    """
    print("\n=== Example 2: Dataset Creation ===")
    
    dataset_structure = '''Format: (Instruction, Input, Output)
    
    Example 1:
    Instruction: "Translate English to Spanish"
    Input: "Hello, how are you?"
    Output: "Hola, ¿cómo estás?"
    
    Example 2:
    Instruction: "Answer the following question"
    Input: "What is the capital of France?"
    Output: "Paris is the capital of France."
    
    Example 3:
    Instruction: "Summarize the following text"
    Input: "[Long text]"
    Output: "[Summary]"
    
    Guidelines:
    - Clear, specific instructions
    - Diverse instruction types
    - High-quality outputs
    - Balanced dataset
    '''
    
    print(dataset_structure)


def task_diversity() -> None:
    """
    Example 3: Diverse task types for tuning.
    Different instruction types to include.
    """
    print("\n=== Example 3: Task Diversity ===")
    
    task_categories = {
        "Classification": ["Sentiment analysis", "Topic classification", "Intent detection"],
        "Generation": ["Summarization", "Writing", "Code generation"],
        "Extraction": ["Named entity extraction", "Information extraction"],
        "Reasoning": ["QA", "Logical reasoning", "Math problems"],
        "Transformation": ["Translation", "Paraphrasing", "Style transfer"],
        "Dialogue": ["Conversation", "Response generation"]
    }
    
    print("\nTask diversity for comprehensive tuning:")
    for category, tasks in task_categories.items():
        print(f"\n{category}:")
        for task in tasks:
            print(f"  - {task}")


def few_shot_in_context_learning() -> None:
    """
    Example 4: Few-shot examples in instructions.
    Including examples in prompts.
    """
    print("\n=== Example 4: Few-Shot In-Context Learning ===")
    
    example_prompt = '''Instruction: Classify sentiment
    
    Examples:
    1. "I love this product!" -> Positive
    2. "This is terrible" -> Negative
    3. "It's okay" -> Neutral
    
    Now classify:
    "This is amazing!" -> 
    '''
    
    print(example_prompt)
    print("\nIncluding examples helps guide model behavior")


def instruction_format_styles() -> None:
    """
    Example 5: Different instruction format styles.
    Various ways to structure instructions.
    """
    print("\n=== Example 5: Instruction Format Styles ===")
    
    styles = {
        "Direct": "Summarize: [text]",
        "Role-based": "You are a translator. Translate to Spanish: [text]",
        "Question": "What is the sentiment of: [text]?",
        "Detailed": "Please provide a summary of the following text in 2-3 sentences: [text]",
        "Task-oriented": "Task: Extract named entities from the text: [text]",
        "Structured": "Input: [text]\nTask: Summarize\nOutput:"
    }
    
    print("\nInstruction format options:")
    for style, example in styles.items():
        print(f"  {style}: {example}")


def evaluation_of_instruction_following() -> None:
    """
    Example 6: Evaluating instruction following capability.
    Metrics for measuring instruction adherence.
    """
    print("\n=== Example 6: Evaluation Metrics ===")
    
    metrics = {
        "Instruction Adherence": "Does output follow the instruction?",
        "Task Accuracy": "Is the task completed correctly?",
        "Format Compliance": "Does output match requested format?",
        "Relevance": "Is output relevant to instruction?",
        "Completeness": "Does output address all instruction aspects?"
    }
    
    print("\nKey evaluation metrics:")
    for metric, description in metrics.items():
        print(f"  {metric}: {description}")


def real_world_examples() -> None:
    """
    Example 7: Real-world instruction tuning examples.
    Practical applications.
    """
    print("\n=== Example 7: Real-World Examples ===")
    
    examples = {
        "ChatGPT Training": "RLHF with instruction-following objectives",
        "Customer Service": "Tuning models to follow support guidelines",
        "Code Generation": "Training models to generate code per specifications",
        "Content Creation": "Tuning for specific writing styles and guidelines",
        "Domain Adaptation": "Instruction tuning for specialized domains"
    }
    
    print("\nReal-world applications:")
    for application, description in examples.items():
        print(f"  {application}: {description}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Instruction Tuning")
    print("="*60)
    
    instruction_tuning_overview()
    dataset_creation()
    task_diversity()
    few_shot_in_context_learning()
    instruction_format_styles()
    evaluation_of_instruction_following()
    real_world_examples()