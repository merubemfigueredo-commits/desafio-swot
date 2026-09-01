"""Ponto de entrada visível para o DESAFIO SWOT no Streamlit Cloud."""

from pathlib import Path
import runpy


runpy.run_path(
    str(Path(__file__).parent / "streamlit_app.py"),
    run_name="__main__",
)
