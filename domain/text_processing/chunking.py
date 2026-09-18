from pathlib import Path

MAX_CHUNK_SIZE = 10


def mardown_file_read(file_path: Path) -> str: ...


def get_paragraphs_from_text(str) -> list[str]: ...


def get_paragraph_length(str) -> int: ...


def reduce_paragraph(str) -> list[str]: ...


def get_chunks_from_text(text: str) -> list[str]:
    final_paragraphs = []

    paragraphs = get_paragraphs_from_text(text)
    for paragraph in paragraphs:

        if get_paragraph_length(paragraph) > MAX_CHUNK_SIZE:
            new_paragraphs = reduce_paragraph(paragraph)

            for new_paragraph in new_paragraphs:
                final_paragraphs.append(new_paragraph)

        else:
            final_paragraphs.append(paragraph)

    return final_paragraphs


def chunk_markdown(file_path: Path) -> list[str]:
    text = mardown_file_read(file_path)
    chunks = get_chunks_from_text(text)
    print(chunks)
    return chunks
