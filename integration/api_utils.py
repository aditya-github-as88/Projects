"""
Module: API Utilities
Description: Helper functions and utilities for working with Groq API
Reusable utilities for common tasks
"""

import os
import time
from typing import Optional, List, Dict
from datetime import datetime


class GroqAPIHelper:
    """Helper class for Groq API operations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with API key"""
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set")
    
    def format_prompt(self, instruction: str, context: str = "", 
                     input_text: str = "") -> str:
        """Format a prompt with instruction, context, and input"""
        prompt = ""
        if context:
            prompt += f"Context: {context}\n\n"
        prompt += f"Instruction: {instruction}\n"
        if input_text:
            prompt += f"\nInput: {input_text}"
        return prompt
    
    def create_message_history(self, messages: List[Dict]) -> List[Dict]:
        """Validate and format message history"""
        formatted = []
        valid_roles = {"user", "assistant", "system"}
        
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                raise ValueError("Messages must have 'role' and 'content'")
            if msg["role"] not in valid_roles:
                raise ValueError(f"Invalid role: {msg['role']}")
            formatted.append(msg)
        
        return formatted


def create_prompt_template(name: str, instruction: str, 
                          variables: List[str] = None) -> Dict:
    """Create a reusable prompt template"""
    return {
        "name": name,
        "instruction": instruction,
        "variables": variables or [],
        "created_at": datetime.now().isoformat()
    }


def fill_prompt_template(template: Dict, **kwargs) -> str:
    """Fill a prompt template with values"""
    prompt = template["instruction"]
    
    for var in template["variables"]:
        if var not in kwargs:
            raise ValueError(f"Missing variable: {var}")
        placeholder = f"{{{var}}}"
        prompt = prompt.replace(placeholder, str(kwargs[var]))
    
    return prompt


def create_few_shot_prompt(instruction: str, examples: List[Dict]) -> str:
    """Create a few-shot prompt from examples"""
    prompt = instruction + "\n\nExamples:\n"
    
    for i, example in enumerate(examples, 1):
        prompt += f"\nExample {i}:\n"
        for key, value in example.items():
            prompt += f"{key}: {value}\n"
    
    return prompt


def truncate_response(response: str, max_length: int = 500) -> str:
    """Truncate response to max length"""
    if len(response) <= max_length:
        return response
    return response[:max_length] + "..."


def estimate_tokens(text: str) -> int:
    """Rough estimate of token count"""
    # Approximate: 1 token ≈ 4 characters
    return len(text) // 4


def log_api_call(prompt: str, response: str, latency_ms: float, 
                model: str = "mixtral-8x7b-32768"):
    """Log an API call for analysis"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "prompt_tokens": estimate_tokens(prompt),
        "response_tokens": estimate_tokens(response),
        "latency_ms": latency_ms,
        "timestamp_unix": time.time()
    }
    return log_entry


def calculate_api_cost(input_tokens: int, output_tokens: int, 
                      model: str = "mixtral-8x7b-32768") -> float:
    """Calculate approximate cost of API call"""
    # Example pricing (check Groq docs for actual pricing)
    pricing = {
        "mixtral-8x7b-32768": {
            "input": 0.0001,     # per 1000 tokens
            "output": 0.0002     # per 1000 tokens
        }
    }
    
    if model not in pricing:
        return 0.0
    
    rate = pricing[model]
    cost = (input_tokens * rate["input"] + output_tokens * rate["output"]) / 1000
    return cost


def retry_on_failure(func, max_retries: int = 3, 
                    delay_seconds: float = 1.0):
    """Retry a function call with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = delay_seconds * (2 ** attempt)
            time.sleep(wait_time)


def batch_process_with_rate_limit(items: List, processor_func, 
                                 requests_per_minute: int = 60):
    """Process items with rate limiting"""
    results = []
    delay = 60 / requests_per_minute  # seconds between requests
    
    for item in items:
        result = processor_func(item)
        results.append(result)
        time.sleep(delay)
    
    return results


# Example utility functions for common patterns

def sentiment_analyzer_prompt(text: str) -> str:
    """Generate sentiment analysis prompt"""
    return f"""Analyze the sentiment of the following text as positive, negative, or neutral:

Text: "{text}"

Sentiment:"""


def code_reviewer_prompt(code: str, language: str = "python") -> str:
    """Generate code review prompt"""
    return f"""Review the following {language} code for quality, efficiency, and best practices:

Code:
```{language}
{code}
```

Review:"""


def summarizer_prompt(text: str, max_words: int = 100) -> str:
    """Generate summarization prompt"""
    return f"""Summarize the following text in approximately {max_words} words:

Text: "{text}"

Summary:"""


if __name__ == "__main__":
    # Example usage
    print("=== API Utilities Examples ===\n")
    
    # Template example
    template = create_prompt_template(
        "sentiment",
        "Analyze sentiment of: {text}",
        ["text"]
    )
    print("Template created:", template)
    
    # Fill template
    filled = fill_prompt_template(template, text="This is awesome!")
    print("Filled prompt:", filled)
    
    # Token estimation
    tokens = estimate_tokens("Hello world, this is a test.")
    print(f"Estimated tokens: {tokens}")
