"""
Vector Indexes Example

A runnable example showing how to build a vector index and query it.
"""

import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document


def build_vector_index() -> FAISS:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set. Set it to build the vector index.")

    texts = [
        "Python is a popular programming language.",
        "LangChain helps build applications with LLMs.",
        "Vector databases support semantic search.",
        "OpenAI provides powerful language models for generation and embeddings."
    ]

    docs = [Document(page_content=text) for text in texts]
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store


def query_vector_index(vector_store: FAISS, query: str) -> None:
    results = vector_store.similarity_search(query, k=2)
    print(f"\n=== Query: {query} ===")
    for i, doc in enumerate(results, 1):
        print(f"Result {i}: {doc.page_content}")


if __name__ == "__main__":
    print("=== Vector Index Example ===")
    try:
        store = build_vector_index()
        query_vector_index(store, "How can I use a vector index?")
        query_vector_index(store, "Tell me about Python.")
    except Exception as e:
        print(f"Error: {e}")
