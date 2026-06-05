"""
Structured Output Parser

Parse LLM outputs into structured formats like Pydantic models.
Provides schema validation and type safety.
"""

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
import json


class PersonInfo(BaseModel):
    """
    Example 1: Define a Pydantic model for structured output.
    """
    name: str = Field(description="The person's name")
    age: int = Field(description="The person's age")
    email: str = Field(description="The person's email address")
    occupation: str = Field(description="The person's job")


class CompanyInfo(BaseModel):
    """
    Example 2: More complex Pydantic model with nested structures.
    """
    company_name: str
    industry: str
    employee_count: int
    headquarters: str
    key_products: List[str] = Field(description="Main products or services")
    founded_year: int
    stock_symbol: Optional[str] = None


class SentimentAnalysis(BaseModel):
    """
    Example 3: Model for sentiment analysis output.
    """
    text: str = Field(description="The input text")
    sentiment: str = Field(description="Sentiment: positive, negative, or neutral")
    confidence: float = Field(description="Confidence score 0-1")
    key_words: List[str] = Field(description="Words contributing to sentiment")


def basic_pydantic_parser() -> None:
    """
    Example 1: Using PydanticOutputParser.
    """
    print("\n=== Example 1: Basic Pydantic Parser ===")
    
    parser = PydanticOutputParser(pydantic_object=PersonInfo)
    
    print("Parser instructions:")
    print(parser.get_format_instructions())
    
    # Example of how to use with prompt
    from langchain.prompts import PromptTemplate
    
    prompt = PromptTemplate(
        template="Extract person information from:\n{text}\n\n{format_instructions}",
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    print(f"\nFormat instructions integrated into prompt")


def parse_example() -> None:
    """
    Example 2: Parsing JSON string to Pydantic model.
    """
    print("\n=== Example 2: Parsing to Pydantic Model ===")
    
    parser = PydanticOutputParser(pydantic_object=PersonInfo)
    
    # Sample JSON response from LLM
    json_output = '''
    {
        "name": "Alice Johnson",
        "age": 28,
        "email": "alice@example.com",
        "occupation": "Software Engineer"
    }
    '''
    
    try:
        parsed = parser.parse(json_output)
        print(f"Successfully parsed:")
        print(f"  Name: {parsed.name}")
        print(f"  Age: {parsed.age}")
        print(f"  Email: {parsed.email}")
        print(f"  Occupation: {parsed.occupation}")
    except Exception as e:
        print(f"Parsing error: {e}")


def complex_structure_parsing() -> None:
    """
    Example 3: Parsing complex nested structures.
    """
    print("\n=== Example 3: Complex Structure Parsing ===")
    
    parser = PydanticOutputParser(pydantic_object=CompanyInfo)
    
    # Sample company data
    company_json = '''
    {
        "company_name": "TechCorp Inc",
        "industry": "Software",
        "employee_count": 500,
        "headquarters": "San Francisco, CA",
        "key_products": ["CloudSync", "DataVault", "AIAssist"],
        "founded_year": 2018,
        "stock_symbol": "TECH"
    }
    '''
    
    try:
        company = parser.parse(company_json)
        print(f"Company: {company.company_name}")
        print(f"Industry: {company.industry}")
        print(f"Employees: {company.employee_count}")
        print(f"Products: {', '.join(company.key_products)}")
    except Exception as e:
        print(f"Error: {e}")


def validation_and_errors() -> None:
    """
    Example 4: Handle validation errors gracefully.
    """
    print("\n=== Example 4: Validation and Error Handling ===")
    
    parser = PydanticOutputParser(pydantic_object=PersonInfo)
    
    # Invalid data (age is string, not int)
    invalid_json = '''
    {
        "name": "Bob",
        "age": "thirty",
        "email": "bob@example.com",
        "occupation": "Manager"
    }
    '''
    
    try:
        parsed = parser.parse(invalid_json)
    except Exception as e:
        print(f"Validation error caught: {type(e).__name__}")
        print(f"The parser validates data types")
        print(f"Age must be integer, not string")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Structured Output Parser")
    print("="*60)
    
    basic_pydantic_parser()
    parse_example()
    complex_structure_parsing()
    validation_and_errors()