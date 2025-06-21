import pandas as pd

# first combine the two and put in langchain

df1 = pd.read_csv("data/processed_chunks_learning.csv")
df2 = pd.read_csv("data/processed_chunks_web.csv")
df = pd.concat([df1, df2], ignore_index=True)

from langchain.schema import Document

documents = [
    Document(page_content=row["chunk"], metadata={"source": row["source"]})
    for _, row in df.iterrows()
]

# create embeddings

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS 

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents, embedding_model)

# Save 
vectorstore.save_local("data/rc_faiss_index")
