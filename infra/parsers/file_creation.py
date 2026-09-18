

from pathlib import Path


def text_to_markdown(text: str, markdown_path: Path):
    
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(text)