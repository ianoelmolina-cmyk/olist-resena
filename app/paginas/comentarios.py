from pathlib import Path
import pandas as pd
import streamlit as st

def estrellas_a_sentimiento(puntaje):
    if puntaje <= 2:
        return "negative"
    elif puntaje == 3:
        return "neutral"
    else:
        return "positive"

@st.cache_data
def cargar_comentarios():
    ruta_del_archivo = Path(__file__).parent.parent / "data" / "sentimiento_comentarios_cache.csv"
    tabla_de_comentarios = pd.read_csv(ruta_del_archivo)
    tabla_de_comentarios["sentimiento_por_estrellas"] = tabla_de_comentarios["review_score"].apply(estrellas_a_sentimiento)
    return tabla_de_comentarios

comentarios = cargar_comentarios()

st.title("Qué dicen los clientes")
st.caption("Sentimiento de los comentarios según un modelo de lenguaje, comparado con las estrellas que pusieron.")

# 1. Dos métricas
coinciden = comentarios["sentimiento_por_estrellas"] == comentarios["label_modelo"]
columna_total, columna_coincidencia = st.columns(2)
columna_total.metric("Comentarios analizados", len(comentarios))
columna_coincidencia.metric("Coincidencia con las estrellas", f"{coinciden.mean():.1%}")

# 2. Tabla cruzada
st.subheader("Estrellas contra sentimiento del modelo")
tabla_cruzada = pd.crosstab(comentarios["sentimiento_por_estrellas"], comentarios["label_modelo"])
st.dataframe(tabla_cruzada)

# 3. Desacuerdos para explorar
st.subheader("Desacuerdos")
desacuerdos = comentarios[~coinciden]

estrellas_elegidas = st.multiselect(
    "Estrellas del cliente",
    options=sorted(desacuerdos["review_score"].unique()),
    default=sorted(desacuerdos["review_score"].unique()),
)
desacuerdos_filtrados = desacuerdos[desacuerdos["review_score"].isin(estrellas_elegidas)]
st.write(f"{len(desacuerdos_filtrados)} desacuerdos")

st.dataframe(
    desacuerdos_filtrados[["review_score", "label_modelo", "sentimiento_por_estrellas" , "review_comment_message", "confianza"]],
    hide_index=True,
    column_config={
        "confianza": st.column_config.ProgressColumn("Confianza del modelo", min_value=0, max_value=1),
        "review_comment_message": st.column_config.TextColumn("Comentario", width="large"),
    },
)