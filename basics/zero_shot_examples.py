"""
Zero-Shot Examples

Zero-shot prompting means asking the model to perform a task
without providing any examples. The model uses its general knowledge.

Vs. Few-shot: Providing examples to guide the model.
"""

import os
from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def zero_shot_classification() -> None:
    """
    Example 1: Zero-shot text classification.
    Classify text without training examples.
    """
    print("\n=== Example 1: Zero-Shot Classification ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Classify the following text as either 'positive', 'negative', or 'neutral'.
Respond with only one word.

Text: {text}
Classification:"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    texts = [
        "I love this product!",
        "This is the worst experience ever.",
        "The weather is rainy today."
    ]
    
    for text in texts:
        result = chain.invoke({"text": text})
        print(f"Text: {text}")
        print(f"Classification: {result['text'].strip()}")


def zero_shot_summarization() -> None:
    """
    Example 2: Zero-shot text summarization.
    Summarize without specific format examples.
    """
    print("\n=== Example 2: Zero-Shot Summarization ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["article"],
        template="""Please summarize the following article in 2-3 sentences:

{article}

Summary:"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    article = """
    Artificial Intelligence has revolutionized the technology industry.
    From natural language processing to computer vision, AI models are now
    capable of performing complex tasks that previously required human expertise.
    Companies are investing heavily in AI research and deployment.
    """
    
    result = chain.invoke({"article": article})
    print(f"Original article:\n{article}")
    print(f"\nSummary:\n{result['text'].strip()}")


def zero_shot_translation() -> None:
    """
    Example 3: Zero-shot language translation.
    Translate text without examples.
    """
    print("\n=== Example 3: Zero-Shot Translation ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["text", "target_language"],
        template="""Translate the following text to {target_language}.
Respond with only the translation.

Text: {text}
Translation:"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    text = "Hello, how are you?"
    languages = ["Spanish", "French", "German"]
    
    for language in languages:
        result = chain.invoke({"text": text, "target_language": language})
        print(f"{language}: {result['text'].strip()}")


def zero_shot_question_answering() -> None:
    """
    Example 4: Zero-shot question answering.
    Answer questions based on given context.
    """
    print("\n=== Example 4: Zero-Shot Question Answering ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""Based on the following context, answer the question.
If the answer is not in the context, say 'I don't know'.

Context: {context}

Question: {question}
Answer:"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    context = "Paris is the capital of France. It is known for the Eiffel Tower and the Louvre Museum."
    questions = [
        "What is the capital of France?",
        "What is Paris known for?",
        "What is the capital of Spain?"
    ]
    
    for question in questions:
        result = chain.invoke({"context": context, "question": question})
        print(f"Q: {question}")
        print(f"A: {result['text'].strip()}")


def zero_shot_sentiment_analysis() -> None:
    """
    Example 5: Zero-shot sentiment analysis with confidence.
    Provide sentiment and confidence scores.
    """
    print("\n=== Example 5: Zero-Shot Sentiment Analysis ===")
    
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = PromptTemplate(
        input_variables=["review"],
        template="""Analyze the sentiment of the following review.
Respond in format: "Sentiment: [positive/negative/neutral], Confidence: [0-100]%"

Review: {review}
Analysis:"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    reviews = [
        "This movie was absolutely fantastic!",
        "Not bad, but could be better.",
        "Total waste of time and money."
    ]
    
    for review in reviews:
        result = chain.invoke({"review": review})
        print(f"Review: {review}")
        print(f"Analysis: {result['text'].strip()}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("LangChain Zero-Shot Examples")
    print("="*60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set. Please set it to run examples.")
    else:
        print("\nExamples available (uncomment in main to run):")
        print("1. zero_shot_classification()")
        print("2. zero_shot_summarization()")
        print("3. zero_shot_translation()")
        print("4. zero_shot_question_answering()")
        print("5. zero_shot_sentiment_analysis()")