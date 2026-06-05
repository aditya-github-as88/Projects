"""
Data Analysis with LangChain

Use LangChain to analyze text or structured data.
"""

import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def analyze_dataset_summary() -> None:
    """
    Example: Summarize dataset insights from a text description.
    """
    print("\n=== Data Analysis Demo ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set")
        return
    
    llm = OpenAI(api_key=api_key, temperature=0.6)
    prompt = PromptTemplate(
        input_variables=["data_description"],
        template="""You are a data analyst.
Summarize the key insights from this dataset description:

{data_description}

Summary:"""
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    description = """
A retail dataset contains sales information for stores across three regions.
Columns include date, store_id, product_category, units_sold, revenue, and customer_feedback.
The dataset spans one year and includes seasonal patterns, product promotions, and customer satisfaction ratings.
"""
    
    result = chain.invoke({"data_description": description})
    print(result["text"])


if __name__ == "__main__":
    analyze_dataset_summary()