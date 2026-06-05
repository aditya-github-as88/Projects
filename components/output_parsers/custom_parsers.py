"""
Custom Output Parsers

Building custom parsers for specific parsing needs.
Extend BaseOutputParser for complete control.
"""

from langchain.schema import BaseOutputParser
from typing import Any, Dict, List
import re


class CommaSeparatedListParser(BaseOutputParser):
    """
    Example 1: Custom parser for comma-separated lists.
    """
    
    def parse(self, text: str) -> List[str]:
        """
        Parse comma-separated values.
        """
        return [item.strip() for item in text.split(",") if item.strip()]
    
    def get_format_instructions(self) -> str:
        return "Return a comma-separated list of values."


class KeyValueParser(BaseOutputParser):
    """
    Example 2: Custom parser for key-value pairs.
    Handles formats like "key1: value1, key2: value2"
    """
    
    def parse(self, text: str) -> Dict[str, str]:
        """
        Parse key-value pairs.
        """
        result = {}
        # Match patterns like "key: value"
        pattern = r'([^:]+):\s*([^,]+)'
        matches = re.findall(pattern, text)
        
        for key, value in matches:
            result[key.strip()] = value.strip()
        
        return result
    
    def get_format_instructions(self) -> str:
        return 'Return key-value pairs in format: "key1: value1, key2: value2"'


class BulletPointParser(BaseOutputParser):
    """
    Example 3: Custom parser for bullet points.
    Handles text like:
    - Point 1
    - Point 2
    """
    
    def parse(self, text: str) -> List[str]:
        """
        Parse bullet-pointed lists.
        """
        # Match lines starting with - or *
        pattern = r'^[\-\*]\s+(.+)$'
        matches = re.findall(pattern, text, re.MULTILINE)
        return [match.strip() for match in matches if match.strip()]
    
    def get_format_instructions(self) -> str:
        return "Return points as a bullet list with - or * prefix."


def usage_examples() -> None:
    """
    Example 4: Using custom parsers.
    """
    print("\n=== Example 4: Using Custom Parsers ===")
    
    # Comma-separated list
    list_parser = CommaSeparatedListParser()
    result = list_parser.parse("apple, banana, cherry, date")
    print(f"Comma-separated: {result}")
    
    # Key-value pairs
    kv_parser = KeyValueParser()
    result = kv_parser.parse("name: Alice, age: 30, city: NYC")
    print(f"Key-value: {result}")
    
    # Bullet points
    bullet_parser = BulletPointParser()
    bullet_text = "- First point\n- Second point\n- Third point"
    result = bullet_parser.parse(bullet_text)
    print(f"Bullet points: {result}")


def extending_output_parser() -> None:
    """
    Example 5: Template for creating your own parser.
    """
    print("\n=== Example 5: Creating a Custom Parser ===")
    
    template = '''
    from langchain.schema import BaseOutputParser
    
    class MyCustomParser(BaseOutputParser):
        def parse(self, text: str) -> Any:
            # Implement your parsing logic
            # Return the parsed result
            return result
        
        def get_format_instructions(self) -> str:
            return "Describe the expected format..."
    '''
    
    print("Template for custom parser:")
    print(template)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Custom Output Parsers")
    print("="*60)
    
    usage_examples()
    extending_output_parser()