from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from chromadb import PersistentClient
from langchain_ollama import OllamaEmbeddings, ChatOllama
import json
import uuid
from langchain.chains.history_aware_retriever import create_history_aware_retriever

CHROMA_PATH = "./chroma"
COLLECTION_NAME = "data"

chat_instances = {}

REPHRASE_PROMPT = '''
Given the following conversation and follow-up, rephrase the follow-up question to be more specific and clear, while retaining the original intent.
Conversation:
{chat_history}

Follow-up: {input}

Standalone rephrased question:
'''

PROMPT_TEMPLATE = '''
Answer the question based on previous messages and the following context:
---

{context}

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

def create_rag_chat() -> uuid.UUID:
    """
    Create a RAG chat instance using the Ollama model.
    """
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    chat = ChatOllama(
        base_url="http://localhost:11434",
        model="qwen3",
        temperature=0.1,  # Adjust temperature for more deterministic responses
        prompt=prompt,
    )

    # Generate a unique ID for the chat instance
    chat_id = str(uuid.uuid4())
    chat_instances[chat_id] = {
        "chat": chat,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for University of Virginia Research Computing (UVA RC). You will answer questions based on the context provided from the UVA RC YouTube channel and UVA RC Teaching Markdowns. Respond succinctly and accurately. If background knowledge combined with the context does not provide enough information, state that you do not know. If the user asks questions completely unrelated to the context or computing, politely inform them that you can only answer questions related to RC. If the user asks something related to RC, but the context does not provide enough information, state that you do not know."}
        ],
    }
    
    return chat_id

def rag_query(chat_id: uuid.UUID, vector_store: Chroma, query: str) -> str:
    """
    Perform a RAG query on the Chroma vector store.
    """
    chat_instance = chat_instances[chat_id]
    chat = chat_instance["chat"]

    prompt = chat_instance["messages"]

    # retriever_multi_query = MultiQueryRetriever.from_llm(
    #     retriever=vector_store.as_retriever(),
    #     llm=chat,
    # )

    # # Perform the retrieval
    # docs = retriever_multi_query.invoke(query)

    retriever = create_history_aware_retriever(
        llm=chat,
        retriever=vector_store.as_retriever(),
        prompt=ChatPromptTemplate.from_template(REPHRASE_PROMPT),
    )

    # Perform the retrieval
    docs = retriever.invoke({
        "input": query,
        "chat_history": prompt,
    })

    # Take the top 5 documents
    docs = docs[:5]

    context = "\n".join([result.page_content for result in docs]) if docs else "No relevant documents found."
    print(f"Context: {context}")

    prompt.append(
        {"role": "user", "content": ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
            context=context,
            question=query
        )}
    )

    # disable thinking 
    response = chat.invoke(prompt, think=False)

    sources = {doc.metadata["source"]: doc.metadata for doc in docs}

    sources_formatted = []
    for source, metadata in sources.items():
        match metadata["source_type"]:
            case "youtube":
                sources_formatted.append(f'[{metadata["title"]}]({metadata["webpage_url"]}) by [{metadata["author"]}](https://www.youtube.com/channel/{metadata["channel_id"]})')
            case "markdown":
                sources_formatted.append(f'[{metadata["source"]}]({metadata["source"]})')
    
    formatted_response = {
        "response": response.content,
        "sources": sources_formatted
    }

    prompt.append(
        {"role": "assistant", "content": response.content}
    )

    return formatted_response

def main():
    vector_store = get_vector_store()
    rag_chat = create_rag_chat()

    print(f"Number of documents in vector store: {len(vector_store.get()['ids'])}")

    while True:
        query_text = input("Enter your query: ")

        response = rag_query(rag_chat, vector_store, query_text)

        formatted_response = json.dumps(response, indent=2)

        print(formatted_response)


if __name__ == "__main__":
    main()


