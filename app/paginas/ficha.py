from pathlib import Path
import streamlit as st

ruta_de_la_ficha = Path(__file__).parent.parent / "data" / "ficha_modelo.md"
st.markdown(ruta_de_la_ficha.read_text(encoding="utf-8"))