from pathlib import Path

from domain.parsers.pdf_parser import pdf_processing


def main():
    print("Hello from school-rag-lab-1!")


if __name__ == "__main__":
    text = pdf_processing(
        Path("data/raw/pdf/Core Rules.pdf"), Path("data/processed/pdf/Core Rules.md")
    )
    print(text)
