import re
from pathlib import Path

FLATTENED_DIR = Path("./flat_content")

def remove_front_matter(text):
    # Remove TOML or YAML frontmatter delimited by +++ or ---
    return re.sub(r"(?s)^(\+\+\+|---).*?(\+\+\+|---)", "", text).lstrip()

def clean_all_files(directory):
    for md_file in directory.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            original = f.read()

        cleaned = remove_front_matter(original)

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(cleaned)

clean_all_files(FLATTENED_DIR)
