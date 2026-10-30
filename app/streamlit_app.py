import streamlit as st

pagina_riesgo = st.Page("paginas/riesgo.py", title="Riesgo de un pedido", icon=":material/warning:")
pagina_ficha = st.Page(..., title="Ficha del modelo", icon=":material/description:")

pagina_actual = st.navigation([..., ...])
pagina_actual.run()