from pathlib import Path

from domain.parsers.pdf_parser import pdf_processing
from domain.text_processing.chunking import chunk_markdown


def main():
    print("Hello from school-rag-lab-1!")


if __name__ == "__main__":
    chunks = chunk_markdown(Path("data/processed/pdf/Core Rules.md"))