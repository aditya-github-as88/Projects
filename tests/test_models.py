"""
Tests for model files.
"""

import os
import pytest
from components.models.custom_models import MockLLM


def test_mock_llm_response():
    mock_llm = MockLLM(responses={"Hello": "Hi there!"})
    output = mock_llm.invoke("Hello")
    assert "Hi there!" in output


def test_mock_llm_default_response():
    mock_llm = MockLLM(responses={})
    output = mock_llm.invoke("Test prompt")
    assert "Mock response to:" in output


def test_api_key_presence():
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY should be set for model tests"
