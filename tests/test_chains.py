"""
Tests for chain examples.
"""

import pytest
from components.chains.custom_chains import ValidationChain, CustomChain


def test_validation_chain_empty_text():
    chain = ValidationChain()
    outputs = chain({"text": ""})
    assert outputs["valid"] == "false"
    assert "empty" in outputs["message"].lower()


def test_validation_chain_valid_text():
    chain = ValidationChain()
    outputs = chain({"text": "Hello world"})
    assert outputs["valid"] == "true"


def test_custom_chain_processing():
    chain = CustomChain()
    outputs = chain({"input": "sample text"})
    assert outputs["output"] == "Processed: sample text"