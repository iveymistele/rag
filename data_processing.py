import pandas as pd

df = pd.read_csv("data/raw_learning.csv")  


import re

def clean_markdown(text):
    if not isinstance(text, str):
        return ""

    # Remove TOML or YAML frontmatter
    text = re.sub(r"(?s)^(\+\+\+|---).*?(\+\+\+|---)", "", text)

    # Remove code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # Remove inline code
    text = re.sub(r"`.*?`", "", text)

    # Remove markdown links but keep text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove emphasis, headings, bold, etc.
    text = re.sub(r"[*_#>-]", "", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


df["text"] = df["text"].fillna("")

df["cleaned_text"] = df["text"].apply(clean_markdown)
df = df[df["cleaned_text"].str.strip() != ""]

def chunk_text(text, max_words=300):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

chunked_rows = []
for _, row in df.iterrows():
    chunks = chunk_text(row["cleaned_text"])
    for chunk in chunks:
        chunked_rows.append({
            "source": row["file_path"],
            "chunk": chunk
        })

df_chunks = pd.DataFrame(chunked_rows)
df_chunks.to_csv("data/processed_chunks.csv", index=False)
print("worked yay")