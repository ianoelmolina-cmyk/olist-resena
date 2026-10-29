import numpy as np
import pandas as pd

COLUMNAS_DE_FECHA = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

def crear_variables(pedidos_del_contrato):
    variables = pedidos_del_contrato.copy()

    for nombre_columna in COLUMNAS_DE_FECHA:
        variables[nombre_columna] = pd.to_datetime(variables[nombre_columna])

    variables["dias_de_retraso"] = (variables["order_delivered_customer_date"] - variables["order_estimated_delivery_date"]).dt.days
    variables["dias_aprobacion"] = (variables["order_approved_at"] - variables["order_purchase_timestamp"]).dt.days
    variables["dia_hasta_despacho"] = (variables["order_delivered_carrier_date"] - variables["order_approved_at"]).dt.days
    variables["mes_de_compra"] = (variables["order_purchase_timestamp"]).dt.month
    variables["dia_de_compra"] = (variables["order_purchase_timestamp"]).dt.dayofweek

    

    return variables