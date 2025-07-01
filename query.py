import argparse
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from chromadb import PersistentClient
from langchain_ollama import OllamaEmbeddings, ChatOllama
import json

CHROMA_PATH = "./chroma"
COLLECTION_NAME = "data"

PROMPT_TEMPLATE = '''
Answer the question based only on the following context: {context}

---
Answer the question based on the above context: {question}

'''

def get_vector_store() -> Chroma:
    persistent_client = PersistentClient(
        path=CHROMA_PATH,
    )

    embeddings = OllamaEmbeddings(
        base_url="http://localhost:11434",
        model="qwen3",
    )

    return Chroma(
        client=persistent_client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

def rag_query(vector_store: Chroma, query: str) -> str:
    """
    Perform a RAG query on the Chroma vector store.
    """
    docs = vector_store.similarity_search_with_relevance_scores(query, k=5)
    context = "\n".join([result.page_content for result, _ in docs]) if docs else "No relevant documents found."
    # print(f"Context for query '{query}': {context}")


    prompt = f"""
    You are a chatbot for University of Virginia Research Computing (UVA RC). You are given the following context from the UVA RC YouTube channel and from various other UVA RC resources. Respond to the question using the context provided succinctly and accurately.
    Context: {context}
    Question: {query}
    Answer:
    """

    chat = ChatOllama(
        base_url="http://localhost:11434",
        model="qwen3",
        temperature=0.1,  # Adjust temperature for more deterministic responses
    )

    # disable thinking 
    response = chat.invoke(prompt, think=False)

    sources = {doc.metadata["source_type"]: doc.metadata for doc, _score in docs}

    sources_formatted = []
    for source_type, metadata in sources.items():
        if source_type == "youtube":
            sources_formatted.append(f'Source: [{metadata["title"]}]({metadata["webpage_url"]}) by [{metadata["author"]}](https://www.youtube.com/channel/{metadata["channel_id"]})')
        elif source_type == "markdown":
            sources_formatted.append(f'Source: [{metadata["title"]}]({metadata["source"]})')

    formatted_response = json.dumps({
        "response": response.content,
        "sources": sources_formatted
    }, indent=2)

    return formatted_response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="Query text")
    args = parser.parse_args()
    query_text = args.query

    vector_store = get_vector_store()

    print(f"Querying vector store with: {query_text}")
    print(f"Number of documents in vector store: {len(vector_store.get()['ids'])}")

    formatted_response = rag_query(vector_store, query_text)

    print(formatted_response)


if __name__ == "__main__":
    main()


