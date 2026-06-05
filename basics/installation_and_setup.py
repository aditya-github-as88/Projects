"""
Installation and Setup for LangChain

This module demonstrates how to install and configure LangChain.

Prerequisites:
  - Python 3.8+
  - pip (Python package manager)

Installation Steps:
  1. Basic LangChain installation:
     pip install langchain

  2. For OpenAI integration:
     pip install langchain-openai openai

  3. For community integrations:
     pip install langchain-community

  4. For core components:
     pip install langchain-core

  5. Install all requirements:
     pip install -r requirements.txt

Environment Setup:
  - Set OPENAI_API_KEY environment variable for OpenAI access
  - Example: export OPENAI_API_KEY='your-key-here'
"""

import os
import sys
from typing import Optional

try:
    from langchain import __version__
    print(f"✓ LangChain version: {__version__}")
except ImportError:
    print("✗ LangChain not installed. Run: pip install langchain")
    sys.exit(1)

try:
    from langchain_openai import OpenAI, ChatOpenAI
    print("✓ OpenAI integration available")
except ImportError:
    print("⚠ OpenAI integration not available. Run: pip install langchain-openai")

try:
    from langchain_community.llms import HuggingFaceHub
    print("✓ Community integrations available")
except ImportError:
    print("⚠ Community integrations not available. Run: pip install langchain-community")


def check_api_key(provider: str = "openai") -> bool:
    """
    Check if API key is set for the given provider.
    
    Args:
        provider: API provider name (e.g., 'openai', 'huggingface')
    
    Returns:
        bool: True if API key is set, False otherwise
    """
    if provider.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print(f"✓ {provider.upper()} API key is set")
            return True
        else:
            print(f"✗ {provider.upper()} API key not found")
            return False
    return False


def print_system_info() -> None:
    """
    Print system information for debugging.
    """
    print("\n=== System Information ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")


if __name__ == "__main__":
    print("\n=== LangChain Setup Check ===")
    check_api_key("openai")
    print_system_info()
    print("\n✓ Setup complete! You're ready to use LangChain.")