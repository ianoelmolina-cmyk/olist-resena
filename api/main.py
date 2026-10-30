from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
import joblib, json, pandas as pd

import preparacion            # IMPORTANTE: antes de cargar el .joblib
import numpy as np
from fastapi import FastAPI, HTTPException      # añade HTTPException al import existente

COLUMNAS_FECHA = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
                  "order_delivered_customer_date", "order_estimated_delivery_date"]
COLUMNAS_NUM = ["n_items", "n_vendedores", "precio_total", "flete_total",
                "peso_total_g", "fotos_promedio", "cuotas_max"]

CONTRATO = ["order_id", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
            "order_delivered_customer_date", "order_estimated_delivery_date", "estado_cliente", "n_items",
            "n_vendedores", "precio_total", "flete_total", "peso_total_g", "fotos_promedio", "categoria",
            "estado_vendedor", "tipo_pago", "cuotas_max"]

app = FastAPI(title="Riesgo de mala reseña")
modelo = joblib.load("modelo_riesgo.joblib")
with open("umbral_riesgo.json") as f:
    datos_umbral = json.load(f)                # leer el JSON del umbral

umbral = datos_umbral["umbral"]      # ajusta la clave al nombre real en tu JSON
class Pedido(BaseModel):
    order_id: str
    order_purchase_timestamp: str          # fechas como texto
    order_approved_at: Optional[str] = None
    order_delivered_carrier_date: Optional[str] = None
    order_delivered_customer_date: str
    order_estimated_delivery_date: str
    estado_cliente: str
    n_items: Optional[int] = None
    n_vendedores: Optional[int] = None
    flete_total: Optional[float] = Field(default=None, ge=0)
    peso_total_g: Optional[float] = Field(default=None, ge=0) 
    fotos_promedio: Optional[float] = Field(default=None, ge=0) 
    categoria: Optional[str] = None
    estado_vendedor: Optional[str] = None
    tipo_pago: Optional[str] = None
    cuotas_max: Optional[float] = Field(default=None, ge=0)                               # las 17 columnas del contrato
    precio_total: Optional[float] = Field(default=None, ge=0)      # ge=0 -> un precio negativo da 422
    

@app.get("/")
def raiz():
    return {
        "estado": "ok",
        "mensaje": "API Riesgo de mala reseña",
    }                           # un JSON que confirma que está viva

@app.post("/riesgo")
def riesgo(pedido: Pedido):
    # 1) Los campos opcionales que no llegaron vienen como None; el pipeline espera NaN
    datos = {k: (np.nan if v is None else v) for k, v in pedido.model_dump().items()}
    fila = pd.DataFrame([datos])

    # 2) Fechas: de texto a datetime (las vacías quedan como NaT)
    try:
        for col in COLUMNAS_FECHA:
            fila[col] = pd.to_datetime(fila[col])
    except (ValueError, TypeError):
        raise HTTPException(status_code=422,
                            detail="Fecha con formato inválido. Usa 'AAAA-MM-DD HH:MM:SS'.")

    # 3) Numéricas: aseguramos que sean números
    for col in COLUMNAS_NUM:
        fila[col] = pd.to_numeric(fila[col], errors="coerce")

    # 4) Mismas columnas y mismo orden que el contrato
    fila = fila[CONTRATO]

    # 5) Predicción y decisión
    probabilidad = float(modelo.predict_proba(fila)[:, 1][0])
    return {
        "probabilidad": round(probabilidad, 4),
        "riesgo_alto": bool(probabilidad >= umbral),
        "umbral": umbral,
    }