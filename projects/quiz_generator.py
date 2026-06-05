"""
Quiz Generator

Generate a quiz based on a topic using LangChain.
"""

import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def generate_quiz() -> None:
    """
    Generate a short quiz with questions and answers.
    """
    print("\n=== Quiz Generator Demo ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        return
    
    llm = OpenAI(api_key=api_key, temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="""Create a quiz with 5 multiple-choice questions about {topic}.
Include the correct answer for each question."""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.invoke({"topic": "renewable energy"})
    print(result["text"])


if __name__ == "__main__":
    generate_quiz()