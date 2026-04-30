"""
Module: Few-Shot Prompting
Description: Providing examples to guide the model's behavior
This improves performance on specific tasks by demonstration
"""

def sentiment_analysis_few_shot():
    """Classify sentiment with examples"""
    prompt = """
    Classify the sentiment of movie reviews as positive or negative.
    
    Examples:
    Review: "This movie was amazing! Brilliant acting and great story."
    Sentiment: Positive
    
    Review: "Terrible waste of time. Boring and predictable."
    Sentiment: Negative
    
    Review: "It was okay, nothing special but watchable."
    Sentiment: Neutral
    
    Now classify this review:
    Review: "Outstanding cinematography! A masterpiece of modern cinema."
    Sentiment:
    """
    return prompt


def entity_extraction_few_shot():
    """Extract entities with examples"""
    prompt = """
    Extract the person's name and their profession from the text.
    
    Examples:
    Text: "John Smith is a software engineer at Google."
    Name: John Smith
    Profession: Software Engineer
    
    Text: "Dr. Emily Wilson works as a cardiologist."
    Name: Emily Wilson
    Profession: Cardiologist
    
    Now extract from this text:
    Text: "Michael Johnson is a professional chef and food blogger."
    Name:
    Profession:
    """
    return prompt


def question_answering_few_shot():
    """Answer questions with examples"""
    prompt = """
    Answer the following questions based on the provided text.
    
    Example:
    Text: "The Amazon rainforest is the largest tropical rainforest in the world."
    Q: Where is the largest tropical rainforest?
    A: The Amazon rainforest
    
    Text: "Python is a high-level programming language known for its simplicity."
    Q: What is Python known for?
    A: Its simplicity
    
    Now answer this:
    Text: "Machine learning is a subset of artificial intelligence focused on enabling computers to learn from data."
    Q: What is machine learning focused on?
    A:
    """
    return prompt


def translation_few_shot():
    """Translate with examples"""
    prompt = """
    Translate the following English sentences to Spanish.
    
    Examples:
    English: "Good morning"
    Spanish: "Buenos días"
    
    English: "How are you?"
    Spanish: "¿Cómo estás?"
    
    Now translate:
    English: "Thank you very much"
    Spanish:
    """
    return prompt


if __name__ == "__main__":
    print("=== Few-Shot Prompting Examples ===\n")
    print("1. Sentiment Analysis:")
    print(sentiment_analysis_few_shot())
    print("\n2. Entity Extraction:")
    print(entity_extraction_few_shot())
    print("\n3. Question Answering:")
    print(question_answering_few_shot())
    print("\n4. Translation:")
    print(translation_few_shot())
