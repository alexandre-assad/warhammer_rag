from pathlib import Path

MAX_CHUNK_SIZE = 500


def mardown_file_read(file_path: Path) -> str: 
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()


def get_paragraphs_from_text(text: str) -> list[str]: 
    return text.split('##')


def reduce_paragraph(paragraph: str, chunk_size:int = 500, min_size: int = 20) -> list[str]: 
    window = paragraph[:MAX_CHUNK_SIZE]

    separators = ['\n\n','\n','. ', '? ', '! ', '; ']
    for separator in separators:
        idx = window.rfind(separator)
        if idx > min_size:
            reduced_paragraph = paragraph[:idx + len(separator)]
            if len(paragraph[idx + len(separator):]) > MAX_CHUNK_SIZE:
                others_paragraphs = reduce_paragraph(paragraph[idx + len(separator):], chunk_size)
            else:
                others_paragraphs = [paragraph[idx + len(separator):]]
            return [reduced_paragraph] + others_paragraphs
        
    return [paragraph[:MAX_CHUNK_SIZE], paragraph[MAX_CHUNK_SIZE:]]

def get_chunks_from_text(text: str, chunk_size: int = 500) -> list[str]:
    final_paragraphs = []

    paragraphs = get_paragraphs_from_text(text)
    for paragraph in paragraphs:

        if len(paragraph) > chunk_size:
            new_paragraphs = reduce_paragraph(paragraph, chunk_size)

            for new_paragraph in new_paragraphs:
                final_paragraphs.append(new_paragraph)

        else:
            final_paragraphs.append(paragraph)

    return final_paragraphs


def chunk_markdown(file_path: Path) -> list[str]:
    text = mardown_file_read(file_path)
    chunks = get_chunks_from_text(text)
    return chunks
