"""
Custom Models in LangChain

How to integrate custom or alternative model providers.
Includes examples of:
- Wrapping custom APIs
- Implementing the LLM interface
- Using alternative providers
"""

from langchain.llms.base import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Optional, List, Any


class CustomLLM(LLM):
    """
    Example 1: Implementing a custom LLM class.
    
    To create a custom LLM, inherit from LLM and implement:
    - _call(): Synchronous method to get predictions
    - _llm_type(): Property returning model type name
    """
    
    model_name: str = "custom-model"
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "custom"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on some input."""
        # Implement your custom logic here
        # This could call an external API, local model, etc.
        
        if stop:
            # Handle stop sequences if needed
            pass
        
        # Placeholder implementation
        return f"Response from {self.model_name}: {prompt}"


class MockLLM(LLM):
    """
    Example 2: Mock LLM for testing purposes.
    Useful for testing chains without calling real APIs.
    """
    
    responses: dict = {}
    
    @property
    def _llm_type(self) -> str:
        return "mock"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Return predefined response for testing.
        """
        # Return predefined response if exists, else return prompt
        return self.responses.get(prompt, f"Mock response to: {prompt}")


def alternative_providers() -> None:
    """
    Example 3: Other model providers that can be integrated.
    
    Popular alternatives:
    - Anthropic Claude: langchain-anthropic
    - Cohere: langchain-community
    - Replicate: langchain-community
    - Together AI: langchain-community
    - Ollama: Open-source local models
    """
    print("\n=== Alternative Model Providers ===")
    
    providers = {
        "Anthropic Claude": "langchain-anthropic",
        "Cohere": "langchain-community",
        "Replicate": "langchain-community",
        "Together AI": "langchain-community",
        "Ollama": "langchain-community"
    }
    
    print("\nSupported providers:")
    for provider, package in providers.items():
        print(f"  {provider}: {package}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Custom Models in LangChain")
    print("="*60)
    
    print("\nExamples:")
    print("1. CustomLLM - Basic custom implementation")
    print("2. MockLLM - For testing")
    print("3. Alternative providers")
    
    # Uncomment to run
    # alternative_providers()