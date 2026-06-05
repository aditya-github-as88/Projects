"""
Creative Writer Assistant

A creative writing assistant for generating story ideas and excerpts.
"""

import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def creative_writing() -> None:
    """
    Draft a creative story idea based on a theme.
    """
    print("\n=== Creative Writer Demo ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        return
    
    llm = OpenAI(api_key=api_key, temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["theme"],
        template="""Generate a creative short story prompt based on the theme: {theme}.
Include characters, setting, and conflict."""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"theme": "space exploration and friendship"})
    print(result["text"])


if __name__ == "__main__":
    creative_writing()