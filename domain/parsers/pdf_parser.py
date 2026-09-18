#TODO maybe test from unstructured.partition.auto import partition

from pathlib import Path
from docling.document_converter import DocumentConverter

from infra.parsers.file_creation import text_to_markdown


def pdf_to_text(pdf_path: Path) -> str:
    converter = DocumentConverter()
    text = converter.convert(pdf_path)

    return text.document.export_to_markdown()

def pdf_processing(pdf_path: Path, output_path: Path) -> None:
    markdown_text = pdf_to_text(pdf_path)
    text_to_markdown(markdown_text, output_path)