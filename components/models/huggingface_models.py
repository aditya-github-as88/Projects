"""
HuggingFace Models in LangChain

Integration examples for open-source models from HuggingFace.
Supports models hosted on HuggingFace Hub or local models.
"""

import os
from typing import Optional


def huggingface_hub_models() -> None:
    """
    Example 1: Using HuggingFace Hub hosted models.
    Requires HUGGINGFACEHUB_API_TOKEN environment variable.
    """
    print("\n=== Example 1: HuggingFace Hub Models ===")
    
    try:
        from langchain_community.llms import HuggingFaceHub
        
        llm = HuggingFaceHub(
            repo_id="mistralai/Mistral-7B-Instruct-v0.1",
            model_kwargs={"temperature": 0.7, "max_length": 100},
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )
        
        response = llm.invoke("What is machine learning?")
        print(f"Response:\n{response}")
    except ImportError:
        print("HuggingFace integration not available. Install: pip install langchain-community")


def local_huggingface_pipeline() -> None:
    """
    Example 2: Using local HuggingFace models with transformers.
    Downloads and runs models locally.
    """
    print("\n=== Example 2: Local HuggingFace Pipeline ===")
    
    try:
        from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        
        # Load model and tokenizer
        model_id = "gpt2"  # Smaller model for example
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        
        # Create pipeline
        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=100
        )
        
        llm = HuggingFacePipeline(pipeline=hf_pipeline)
        response = llm.invoke("The future of AI is")
        print(f"Response:\n{response}")
    except ImportError:
        print("Dependencies not available. Install: pip install transformers")


def popular_huggingface_models() -> None:
    """
    Example 3: Popular HuggingFace models for different tasks.
    
    Recommended models:
    - Text Generation: mistralai/Mistral-7B, meta-llama/Llama-2-7b
    - Code Generation: codellama/CodeLlama-7b
    - Dialogue: facebook/blenderbot-400M-distilled
    - Summarization: facebook/bart-large-cnn
    """
    print("\n=== Example 3: Popular HuggingFace Models ===")
    
    popular_models = {
        "Text Generation": "mistralai/Mistral-7B-Instruct-v0.1",
        "Code Generation": "codellama/CodeLlama-7b-Instruct-hf",
        "Summarization": "facebook/bart-large-cnn",
        "Question Answering": "deepset/roberta-base-squad2"
    }
    
    print("\nPopular models available on HuggingFace Hub:")
    for task, model_id in popular_models.items():
        print(f"  {task}: {model_id}")


def model_parameters() -> None:
    """
    Example 4: Common parameters for HuggingFace models.
    
    Parameters:
    - temperature: Controls randomness (0.0-1.0)
    - max_length: Maximum token output length
    - top_p: Nucleus sampling parameter
    - top_k: Keep top k highest probability tokens
    - repetition_penalty: Penalize repetition
    """
    print("\n=== Example 4: HuggingFace Model Parameters ===")
    
    model_kwargs = {
        "temperature": 0.7,
        "max_length": 100,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.2
    }
    
    print("\nRecommended model parameters:")
    for param, value in model_kwargs.items():
        print(f"  {param}: {value}")


def comparison_with_openai() -> None:
    """
    Example 5: Comparison between HuggingFace and OpenAI models.
    
    HuggingFace Advantages:
    - Open source, free to use
    - Privacy (run locally)
    - Fine-tuning support
    - No API costs
    
    HuggingFace Disadvantages:
    - Requires computational resources
    - Smaller models generally less capable
    - Setup complexity
    
    OpenAI Advantages:
    - State-of-the-art performance
    - Easy API integration
    - No local compute needed
    
    OpenAI Disadvantages:
    - Subscription costs
    - Data sent to external servers
    - Limited customization
    """
    print("\n=== Example 5: HuggingFace vs OpenAI Comparison ===")
    
    comparison = {
        "HuggingFace": {
            "Advantages": ["Open source", "Privacy", "Customizable", "Free"],
            "Disadvantages": ["Resource intensive", "Setup complex", "Less capable"]
        },
        "OpenAI": {
            "Advantages": ["Best performance", "Easy to use", "Always available"],
            "Disadvantages": ["Costs money", "Data privacy", "Limited control"]
        }
    }
    
    for provider, details in comparison.items():
        print(f"\n{provider}:")
        print(f"  Advantages: {', '.join(details['Advantages'])}")
        print(f"  Disadvantages: {', '.join(details['Disadvantages'])}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("HuggingFace Models in LangChain")
    print("="*60)
    
    print("\nExamples available:")
    print("1. huggingface_hub_models() - Requires HUGGINGFACEHUB_API_TOKEN")
    print("2. local_huggingface_pipeline() - Requires transformers library")
    print("3. popular_huggingface_models() - Model recommendations")
    print("4. model_parameters() - Parameter guide")
    print("5. comparison_with_openai() - Pros and cons comparison")