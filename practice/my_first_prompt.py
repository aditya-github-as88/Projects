
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from groq import Groq
from config import GROQ_API_KEY

MODEL_NAME = "openai/gpt-oss-20b"

from basics.zero_shot import sentiment_analysis_zero_shot

# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     raise EnvironmentError("Missing GROQ_API_KEY environment variable")

def createGroqClient():
    groq_client = Groq(api_key=GROQ_API_KEY)
    return groq_client

def get_simple_prompt():
    '''
        Factual prompt. simple question without reasoning.
        Worldly Facts, definitions, or straightforward queries.
    '''
    prompt = "How many planets in the solar system"
    return prompt

def executePrompt(prompt):
    '''
        Execute the prompt and return the response.
        This is a placeholder for the actual execution logic, which could involve
        calling an API, running a model, or any other processing.
    '''
    # Placeholder for execution logic
    response = None
    prompt = prompt or get_simple_prompt()
    groq_client = createGroqClient()
    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1024
    )
    
    return response.choices[0].message.content
  


if __name__ == "__main__":
    ppt = get_simple_prompt()
    print(ppt)

    #1. Model inference using a simple prompt
    # print(f'\n___ Simple Prompt ____{ppt}\n')
    # model_inference = executePrompt(ppt)
    # print(model_inference)

    #2. Model inference using a classification prompt
    print(f'\n___ Classification Prompt ____{sentiment_analysis_zero_shot()}\n')
    model_inference = executePrompt(sentiment_analysis_zero_shot())
    print(model_inference)