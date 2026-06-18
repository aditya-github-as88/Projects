import os
import openai
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
load_dotenv()


### Load Model
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)


### Embedding Model
from langchain_openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings(model='text-embedding-3-small')

### Vector Store - Chroma
from langchain_chroma import Chroma
vectordb = Chroma(persist_directory = 'kbase/chroma/',
                  embedding_function = embedding
                  )


### Retrieval

def get_context_info(question):
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k":5})
    docs = retriever.invoke(question)
    return docs

from langchain_core.runnables import RunnableLambda, RunnableParallel

retrieval = RunnableParallel(
    {
        "context": RunnableLambda(lambda x: get_context_info(x["question"])),
        "question": RunnableLambda(lambda x: x["question"])
        }
    )

### Augmentation

# Build prompt
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""

QA_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)


# RAG Chain
rag_chain = (retrieval                     # Retrieval
             | QA_PROMPT                   # Augmentation
             | llm                         # Generation
             | StrOutputParser()
             )

# Langfuse incorporated
from langfuse.langchain import CallbackHandler
langfuse_handler = CallbackHandler()


# User query
input = "Which colors are available?"

# Get response from RAG chain
response = rag_chain.invoke(
    {"question": input},
    config={
        "callbacks": [langfuse_handler],
        "run_name": "RAG_Query"
        }
    )

print(f"Input query: {input}")
print(f"LLM Response:\n{response}")
