import pytest
from pathlib import Path

from domain.parsers.pdf_parser import (
    pdf_to_text, 
    pdf_processing,
)

#TODO fix issues with docling ...


# import os
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# @pytest.fixture
# def pdf_file():
#     return Path("tests/fixtures/test_generated_pdf.pdf")

# def test_pdf_to_text(pdf_file):
#     result = pdf_to_text(pdf_file)
    
#     assert result is not None
#     assert "Le document test" in result
#     assert "Première sous partie" in result

# def test_pdf_processing(pdf_file, tmp_path):
#     output_file = tmp_path / "result_real.md"
    
#     pdf_processing(pdf_file, output_file)
    
#     assert output_file.exists()
#     assert output_file.stat().st_size > 0
    
#     with open(output_file, 'r', encoding='utf-8') as f:
#         content = f.read()
#         assert "Le document test" in content