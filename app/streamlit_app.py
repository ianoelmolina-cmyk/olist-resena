import streamlit as st

st.set_page_config(page_title="OLIST - Riesgos", layout="wide")

pagina_riesgo = st.Page("paginas/riesgo.py", title="Riesgo de un pedido", icon=":material/warning:")
pagina_ficha = st.Page("paginas/ficha.py", title="Ficha del modelo", icon=":material/description:")
pagina_comentarios = st.Page("paginas/comentarios.py", title="Comentarios sobre los pedidos", icon=":material/chat:")

pagina_actual = st.navigation({
                                "Menú":[pagina_riesgo, pagina_comentarios, pagina_ficha]
})


with st.sidebar:
    st.title("OLIST")



pagina_actual.run()