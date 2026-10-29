import pytest
from pathlib import Path

from domain.text_processing.chunking import (
    mardown_file_read, 
    get_paragraphs_from_text, 
    reduce_paragraph, 
    get_chunks_from_text, 
    chunk_markdown
)

@pytest.fixture
def md_file():
    return Path("tests/fixtures/test_generated_md.MD")


def test_mardown_file_read(md_file):
    result = mardown_file_read(md_file)
    assert "# Guide d'utilisation de Nébuleuse" in result

def test_get_paragraphs_from_text(md_file):
    text = mardown_file_read(md_file)
    paragraphs = get_paragraphs_from_text(text)
    assert len(paragraphs) > 1
    assert "Installation\n\nPour installer l'application" in paragraphs[1]

def test_reduce_paragraph():
    long_paragraph = ("A" * 490) + ". " + ("B" * 50)
    result = reduce_paragraph(long_paragraph)
    assert len(result) == 2
    assert len(result[0]) <= 500
    assert result[1] == ("B" * 50)

def test_get_chunks_from_text(md_file):
    text = mardown_file_read(md_file)
    chunks = get_chunks_from_text(text)
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert chunks[0].startswith("# Guide d'utilisation")

def test_chunk_markdown(md_file):
    chunks = chunk_markdown(md_file)
    assert isinstance(chunks, list)
    assert "Utilisation" in str(chunks)