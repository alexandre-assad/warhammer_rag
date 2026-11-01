pip install uv 
app:
	uv run streamlit run .\main.py
tests:
	tests: uv run python -m pytest -v