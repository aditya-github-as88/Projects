"""
JSON Output Parser

Examples for extracting structured JSON output from LLM responses.
"""

import json
from langchain.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from typing import Any, Dict


def basic_json_output_parser() -> None:
    """
    Example 1: Create and inspect a JSON output parser.
    """
    print("\n=== JSON Output Parser ===")
    parser = JsonOutputParser()
    print("Format instructions:")
    print(parser.get_format_instructions())


def json_parse_example() -> None:
    """
    Example 2: Parse JSON text returned by an LLM.
    """
    print("\n=== JSON Parsing Example ===")
    parser = JsonOutputParser()
    json_text = '{"name": "Alice", "email": "alice@example.com", "role": "Engineer"}'

    parsed = parser.parse(json_text)
    print(f"Parsed result: {parsed}")


def validate_json_output() -> None:
    """
    Example 3: Validate JSON output and handle errors.
    """
    print("\n=== Validate JSON Output ===")
    parser = JsonOutputParser()
    invalid_text = '{name: Alice, email: alice@example.com}'
    try:
        parser.parse(invalid_text)
    except Exception as e:
        print(f"Invalid JSON error: {e}")


def json_prompt_with_parser() -> None:
    """
    Example 4: Use parser instructions in a prompt template.
    """
    print("\n=== Prompt with JSON Parser Instructions ===")
    parser = JsonOutputParser()
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Extract name and email from the following text.

{text}

{format_instructions}""",
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    print(prompt.format(text="Alice is an engineer with email alice@example.com."))


def nested_json_example() -> None:
    """
    Example 5: Show nested JSON structure expectations.
    """
    print("\n=== Nested JSON Example ===")
    nested = {
        "user": {"name": "Alice", "email": "alice@example.com"},
        "roles": ["engineer", "author"]
    }
    print(json.dumps(nested, indent=2))


def best_practices() -> None:
    """
    Example 6: Best practices for JSON output parsing.
    """
    print("\n=== JSON Parser Best Practices ===")
    practices = [
        "Always include format instructions.",
        "Ask for valid JSON only.",
        "Use a parser object to validate output.",
        "Handle invalid or partial JSON gracefully."
    ]
    for practice in practices:
        print(f"- {practice}")


if __name__ == "__main__":
    basic_json_output_parser()
    json_parse_example()
    validate_json_output()
    json_prompt_with_parser()
    nested_json_example()
    best_practices()