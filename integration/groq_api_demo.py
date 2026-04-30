"""
Module: Groq API Demo
Description: Basic examples of using the Groq API for prompt execution
Demonstrates low-latency inference with Groq
"""

import os
from typing import Optional


def example_groq_setup():
    """Show how to set up Groq API"""
    code = """
    from groq import Groq
    
    # Initialize Groq client
    # Requires GROQ_API_KEY environment variable
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )
    """
    return code


def simple_completion_example():
    """Basic completion example"""
    code = """
    def simple_completion(prompt: str) -> str:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # or another available model
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content
    
    # Usage
    result = simple_completion("Explain what machine learning is")
    print(result)
    """
    return code


def system_prompt_example():
    """Example with system prompt for role-based behavior"""
    code = """
    def chat_with_role(user_message: str, role: str) -> str:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a {role}"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content
    
    # Usage
    result = chat_with_role(
        "Explain quantum computing",
        "physics professor"
    )
    """
    return code


def streaming_example():
    """Example of streaming responses"""
    code = """
    def stream_response(prompt: str):
        stream = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True,
            max_tokens=1024
        )
        
        # Print response as it streams
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="")
    
    # Usage
    stream_response("Write a short story about a robot")
    """
    return code


def multi_turn_conversation():
    """Example of maintaining conversation history"""
    code = """
    def multi_turn_chat(messages: list) -> str:
        # messages should be a list of dicts with 'role' and 'content'
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            max_tokens=1024
        )
        return response.choices[0].message.content
    
    # Usage
    messages = [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a programming language..."},
        {"role": "user", "content": "What are its main uses?"}
    ]
    
    result = multi_turn_chat(messages)
    """
    return code


def error_handling_example():
    """Example with error handling"""
    code = """
    def safe_completion(prompt: str) -> Optional[str]:
        try:
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    # Usage
    result = safe_completion("Hello!")
    if result:
        print(result)
    else:
        print("Failed to get response")
    """
    return code


def available_models():
    """List of available Groq models"""
    models = """
    AVAILABLE GROQ MODELS (as of knowledge cutoff):
    
    1. mixtral-8x7b-32768
       - Fast, versatile model
       - Good for most tasks
       - 32k token context window
    
    2. llama2-70b-4096
       - Larger, more capable
       - Better reasoning
       - 4k token context
    
    3. gemma-7b-it
       - Instruction-tuned
       - Lightweight
       - Fast inference
    
    Note: Check Groq documentation for the most current model list
    and specifications.
    """
    return models


if __name__ == "__main__":
    print("=== Groq API Demo ===\n")
    print("1. Setup:")
    print(example_groq_setup())
    print("\n2. Simple Completion:")
    print(simple_completion_example())
    print("\n3. System Prompt:")
    print(system_prompt_example())
    print("\n4. Streaming:")
    print(streaming_example())
    print("\n5. Multi-Turn Conversation:")
    print(multi_turn_conversation())
    print("\n6. Error Handling:")
    print(error_handling_example())
    print("\n7. Available Models:")
    print(available_models())
