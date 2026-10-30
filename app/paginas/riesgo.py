from pathlib import Path
import pandas as pd
import requests
import streamlit as st

@st.cache_data
def cargar_pedidos_de_ejemplo():
    ruta_del_archivo = Path(__file__).parent.parent / "data" / "pedidos_de_ejemplo.csv"
    return pd.read_csv(ruta_del_archivo)

pedidos_de_ejemplo = cargar_pedidos_de_ejemplo()

st.title("Riesgo de mala reseña")

identificador_elegido = st.selectbox("Pedido de ejemplo", pedidos_de_ejemplo["order_id"])
fila_elegida = pedidos_de_ejemplo[pedidos_de_ejemplo["..."] == identificador_elegido]
st.dataframe(fila_elegida.T)

if st.button("Calcular riesgo"):
    pedido = fila_elegida.astype(object).where(fila_elegida.notna(), None).iloc[0].to_dict()
    try:
        with st.spinner("Consultando la API (puede tardar hasta un minuto si estaba dormida)..."):
            respuesta = requests.post(f"{st.secrets['API_URL']}/...", json=pedido, timeout=90)
            respuesta.raise_for_status()
    except requests.RequestException as error:
        st.error("...")
        st.caption(f"Detalle: {error}")
        st.stop()

    resultado = respuesta.json()
    columna_probabilidad, columna_umbral = st.columns(2)
    columna_probabilidad.metric("Probabilidad de 1 o 2 estrellas", f"{resultado['probabilidad']:.0%}")
    columna_umbral.metric("Umbral de riesgo alto", f"{resultado['...']:.0%}")

    if resultado["riesgo_alto"]:
        st.error("Riesgo alto: contactar al cliente")
    else:
        st.success("Riesgo bajo: no hace falta llamar")

    with st.expander("Respuesta completa de la API"):
        st.json(resultado)