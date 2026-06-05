"""
Flower Delivery Assistant

A domain-specific assistant that helps create delivery notes and gift suggestions.
"""

import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def flower_delivery_assistant() -> None:
    """
    Generate a friendly delivery note and gift suggestion.
    """
    print("\n=== Flower Delivery Assistant ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        return
    
    llm = OpenAI(api_key=api_key, temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["recipient", "occasion", "flower_type"],
        template="""Write a warm delivery note for {recipient} on the occasion of {occasion}.
Include a brief message about {flower_type} and why it is a good choice."""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({
        "recipient": "Emma",
        "occasion": "her promotion",
        "flower_type": "roses"
    })
    print(result["text"])


if __name__ == "__main__":
    flower_delivery_assistant()