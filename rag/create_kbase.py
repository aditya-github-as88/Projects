import os
import openai
import numpy as np
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
load_dotenv()


### Load PDF
from langchain_community.document_loaders import PyMuPDFLoader

folder_path = '/'.join(__file__.split('/')[:-1])

loaders = [
    PyMuPDFLoader(folder_path + "/docs/Product_XSound_Pro_Headphones.pdf")
]

docs = []
for loader in loaders:
    docs.extend(loader.load())


### Splitting of document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

splits = text_splitter.split_documents(docs)

#print(len(splits))
#print(len(splits[0].page_content) )
#print(splits[0].page_content)


### Embedding Model
from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings(model='text-embedding-3-small')


### Vector Store - Chroma
from langchain_chroma import Chroma       # Light-weight and in memory

persist_directory = 'kbase/chroma/'

import shutil

# Remove directory if it exists
if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
    shutil.rmtree(persist_directory)
    print(f"Removed existing directory: {persist_directory}")


vectordb = Chroma.from_documents(
    documents=splits,                    # splits we created earlier
    embedding=embedding,
    persist_directory=persist_directory, # save the directory
)

#print(vectordb._collection.count()) # same as number of splits

if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
    print(f"Created persistent directory for Chroma: {persist_directory}")

