import os
from pathlib import Path
import shutil

INPUT_DIR = Path("./md_content")
OUTPUT_DIR = Path("./flat_content")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def flatten_markdown_files(input_dir, output_dir):
    counter = 0

    for md_file in input_dir.rglob("*.md"):
        rel_path = md_file.relative_to(input_dir)
        flat_name = "_".join(rel_path.parts)
        
        # Optional: add counter if needed to avoid filename collisions
        if (output_dir / flat_name).exists():
            counter += 1
            flat_name = f"{counter}_{flat_name}"

        shutil.copy(md_file, output_dir / flat_name)

flatten_markdown_files(INPUT_DIR, OUTPUT_DIR)
