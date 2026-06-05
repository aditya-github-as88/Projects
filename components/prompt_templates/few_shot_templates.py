"""
Few-Shot Prompt Templates

Few-shot prompting provides examples to guide the model's behavior.
Often produces better results than zero-shot prompting.
"""

from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from typing import List, Dict


def basic_few_shot() -> None:
    """
    Example 1: Basic few-shot template.
    Include a few examples before the actual question.
    """
    print("\n=== Example 1: Basic Few-Shot ===")
    
    # Define examples
    examples = [
        {"input": "happy", "output": "positive"},
        {"input": "sad", "output": "negative"},
        {"input": "neutral", "output": "neutral"},
    ]
    
    # Create example prompt
    example_prompt = PromptTemplate(
        input_variables=["input", "output"],
        template="Input: {input}\nOutput: {output}"
    )
    
    # Create few-shot prompt
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Input: {word}\nOutput:",
        input_variables=["word"]
    )
    
    # Use it
    prompt = few_shot_prompt.format(word="excited")
    print(f"Few-shot prompt:\n{prompt}")


def sentiment_analysis_few_shot() -> None:
    """
    Example 2: Few-shot for sentiment analysis.
    Guide the model with classification examples.
    """
    print("\n=== Example 2: Sentiment Analysis Few-Shot ===")
    
    examples = [
        {
            "text": "I love this product! Best purchase ever.",
            "sentiment": "positive"
        },
        {
            "text": "Terrible quality. Complete waste of money.",
            "sentiment": "negative"
        },
        {
            "text": "It's okay, nothing special.",
            "sentiment": "neutral"
        },
    ]
    
    example_prompt = PromptTemplate(
        input_variables=["text", "sentiment"],
        template="""Text: {text}
Sentiment: {sentiment}"""
    )
    
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Classify the sentiment of the following text:\n",
        suffix="\nText: {new_text}\nSentiment:",
        input_variables=["new_text"]
    )
    
    prompt = few_shot_prompt.format(new_text="This is pretty good!")
    print(f"Sentiment classification prompt:\n{prompt}")


def translation_few_shot() -> None:
    """
    Example 3: Few-shot for translation tasks.
    Show examples of English to Spanish translation.
    """
    print("\n=== Example 3: Translation Few-Shot ===")
    
    examples = [
        {"english": "Hello", "spanish": "Hola"},
        {"english": "Good morning", "spanish": "Buenos días"},
        {"english": "How are you?", "spanish": "¿Cómo estás?"},
    ]
    
    example_prompt = PromptTemplate(
        input_variables=["english", "spanish"],
        template="English: {english}\nSpanish: {spanish}"
    )
    
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Translate English to Spanish:",
        suffix="\nEnglish: {phrase}\nSpanish:",
        input_variables=["phrase"]
    )
    
    prompt = few_shot_prompt.format(phrase="Thank you")
    print(f"Translation prompt:\n{prompt}")


def dynamic_example_selection() -> None:
    """
    Example 4: Selecting examples dynamically.
    Choose relevant examples based on input.
    """
    print("\n=== Example 4: Dynamic Example Selection ===")
    
    # Large example pool
    all_examples = [
        {"question": "What is 2+2?", "answer": "4"},
        {"question": "What is 5+3?", "answer": "8"},
        {"question": "What is capital of France?", "answer": "Paris"},
        {"question": "What is capital of Spain?", "answer": "Madrid"},
    ]
    
    def select_examples(input_text: str) -> List[Dict]:
        """
        Select examples based on input type.
        """
        if "capital" in input_text.lower():
            # Return geography examples
            return [ex for ex in all_examples if "capital" in ex["question"]]
        elif any(char.isdigit() for char in input_text):
            # Return math examples
            return [ex for ex in all_examples if "+" in ex["question"]]
        return all_examples[:2]  # Default
    
    # Use dynamic selection
    selected = select_examples("What is the capital of Germany?")
    print(f"Selected examples for geography question:")
    for ex in selected:
        print(f"  Q: {ex['question']} -> A: {ex['answer']}")


def example_selector_integration() -> None:
    """
    Example 5: Using ExampleSelector for intelligent selection.
    Select most similar examples for better performance.
    """
    print("\n=== Example 5: ExampleSelector Integration ===")
    
    try:
        from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
        from langchain_openai.embeddings import OpenAIEmbeddings
        
        examples = [
            {"input": "happy", "output": "positive"},
            {"input": "sad", "output": "negative"},
            {"input": "angry", "output": "negative"},
            {"input": "joyful", "output": "positive"},
        ]
        
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            vectorstore_cls=None  # Would use FAISS or similar
        )
        
        print("ExampleSelector can select most relevant examples based on similarity")
        print("Setup requires OpenAI embeddings and vector store")
    except ImportError:
        print("ExampleSelector requires additional dependencies")


def when_to_use_few_shot() -> None:
    """
    Example 6: Guidelines for using few-shot prompting.
    """
    print("\n=== Example 6: When to Use Few-Shot ===")
    
    guidelines = {
        "Use few-shot when:": [
            "Task has specific format requirements",
            "Zero-shot results are not satisfactory",
            "You have clear examples of correct outputs",
            "Task is complex or requires pattern learning"
        ],
        "Benefits:": [
            "Better accuracy and consistency",
            "Guides model behavior",
            "Reduces need for long instructions",
            "Works with smaller example sets"
        ],
        "Drawbacks:": [
            "Uses more tokens (costs more)",
            "Requires good examples",
            "May overfit to example style",
            "Longer prompt length"
        ]
    }
    
    for category, points in guidelines.items():
        print(f"\n{category}")
        for point in points:
            print(f"  • {point}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Few-Shot Prompt Templates")
    print("="*60)
    
    basic_few_shot()
    sentiment_analysis_few_shot()
    translation_few_shot()
    dynamic_example_selection()
    example_selector_integration()
    when_to_use_few_shot()