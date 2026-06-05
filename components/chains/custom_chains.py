"""
Custom Chains

Building custom chain classes for specific workflows.
Extend Chain base class for complete control.
"""

from langchain.chains.base import Chain
from langchain.callbacks.manager import CallbackManagerForChainRun
from typing import Dict, List, Optional, Any


class CustomChain(Chain):
    """
    Example 1: Basic custom chain implementation.
    """
    
    @property
    def input_keys(self) -> List[str]:
        """Define input variable names."""
        return ["input"]
    
    @property
    def output_keys(self) -> List[str]:
        """Define output variable names."""
        return ["output"]
    
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        """Execute the chain logic."""
        # Your custom logic here
        input_text = inputs["input"]
        output = f"Processed: {input_text}"
        return {"output": output}


class ValidationChain(Chain):
    """
    Example 2: Chain that validates input.
    """
    
    @property
    def input_keys(self) -> List[str]:
        return ["text"]
    
    @property
    def output_keys(self) -> List[str]:
        return ["valid", "message"]
    
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        """Validate input text."""
        text = inputs["text"]
        
        if not text or len(text.strip()) == 0:
            return {"valid": "false", "message": "Text is empty"}
        
        if len(text) < 5:
            return {"valid": "false", "message": "Text too short (min 5 chars)"}
        
        return {"valid": "true", "message": "Text is valid"}


class TransformChain(Chain):
    """
    Example 3: Chain that transforms data.
    """
    
    transform_type: str = "uppercase"  # or "lowercase", "reverse", etc.
    
    @property
    def input_keys(self) -> List[str]:
        return ["text"]
    
    @property
    def output_keys(self) -> List[str]:
        return ["transformed"]
    
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        """Transform text based on type."""
        text = inputs["text"]
        
        if self.transform_type == "uppercase":
            transformed = text.upper()
        elif self.transform_type == "lowercase":
            transformed = text.lower()
        elif self.transform_type == "reverse":
            transformed = text[::-1]
        else:
            transformed = text
        
        return {"transformed": transformed}


class Pipeline(Chain):
    """
    Example 4: Chain that pipelines multiple operations.
    """
    
    chains: List[Chain] = []
    
    @property
    def input_keys(self) -> List[str]:
        return ["input"]
    
    @property
    def output_keys(self) -> List[str]:
        return ["output"]
    
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        """Execute chains in pipeline."""
        result = inputs
        
        for chain in self.chains:
            result = chain(result)
        
        return result


def chain_templates() -> None:
    """
    Example 5: Templates for common chain patterns.
    """
    print("\n=== Example 5: Chain Templates ===")
    
    templates = {
        "Data Validation": "Validate input -> Transform -> Output",
        "Processing Pipeline": "Parse -> Process -> Format -> Output",
        "Routing": "Classify input -> Route to handler -> Output",
        "Caching": "Check cache -> Execute if needed -> Return result",
        "Retry Logic": "Execute -> Check result -> Retry if needed",
        "Rate Limiting": "Check rate -> Execute -> Update counter"
    }
    
    print("\nCommon chain patterns:")
    for pattern, flow in templates.items():
        print(f"  {pattern}: {flow}")


def best_practices() -> None:
    """
    Example 6: Best practices for custom chains.
    """
    print("\n=== Example 6: Best Practices ===")
    
    practices = {
        "Design": [
            "Single responsibility per chain",
            "Clear input/output contracts",
            "Reusable components",
            "Composable with other chains"
        ],
        "Implementation": [
            "Implement input_keys and output_keys",
            "Implement _call method",
            "Handle errors gracefully",
            "Add logging for debugging"
        ],
        "Testing": [
            "Unit test each chain",
            "Test input validation",
            "Test edge cases",
            "Test composition with other chains"
        ],
        "Performance": [
            "Minimize token usage",
            "Cache when possible",
            "Use async for parallel work",
            "Monitor performance metrics"
        ]
    }
    
    for category, tips in practices.items():
        print(f"\n{category}:")
        for tip in tips:
            print(f"  ✓ {tip}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Custom Chains in LangChain")
    print("="*60)
    
    print("\nCustom chain examples:")
    print("1. CustomChain - Basic implementation")
    print("2. ValidationChain - Input validation")
    print("3. TransformChain - Data transformation")
    print("4. Pipeline - Chain composition")
    
    chain_templates()
    best_practices()