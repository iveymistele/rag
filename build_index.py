from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import pickle
import pandas as pd
from pathlib import Path

# step 1 -  
data_dir = Path("data")
csv_files = list(data_dir.glob("*.csv"))

all_docs = [] # to input into langchain

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        if pd.notnull(row["content"]):
            doc = Document(
                page_content=row["content"],
                metadata={
                    "source": row["url"],
                    "title": row.get("title", ""),
                    "section": csv_file.stem  # e.g., "containers_data"
                }
            )
            all_docs.append(doc)

print(f"Loaded {len(all_docs)} documents from {len(csv_files)} CSV files.")


# next split the docs into short chunks (llm friendly)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

split_docs = splitter.split_documents(all_docs)

print(f"Split into {len(split_docs)} total chunks.")

# next step is vector embedding i think do that later 
