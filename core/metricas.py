import pandas as pd


def calcular_metricas(df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    """
    Calcula métricas agregadas de ventas a partir de un DataFrame ya
    validado (ver validaciones.validar_excel).

    Columnas requeridas en df: cantidad, precio_venta, costo_unitario.

    Nota sobre "ticket_promedio": en estos datos, cada fila representa la
    venta de una unidad específica de un producto (confirmado), por lo que
    "ticket_promedio" se define como el precio promedio de venta por unidad:
    ventas_totales / unidades totales vendidas.

    Returns:
        (metricas, df_enriquecido): dict con métricas agregadas y el
        DataFrame original con columnas venta_total, costo_total y
        ganancia añadidas.
    """
    df = df.copy()

    df["venta_total"] = df["cantidad"] * df["precio_venta"]
    df["costo_total"] = df["cantidad"] * df["costo_unitario"]
    df["ganancia"] = df["venta_total"] - df["costo_total"]

    ventas_totales = df["venta_total"].sum()
    unidades = df["cantidad"].sum()
    ganancia_total = df["ganancia"].sum()

    ticket_promedio = ventas_totales / unidades if unidades > 0 else 0
    margen = (ganancia_total / ventas_totales * 100) if ventas_totales > 0 else 0

    metricas = {
        "ventas_totales": ventas_totales,
        "unidades": unidades,
        "ticket_promedio": ticket_promedio,
        "ganancia_total": ganancia_total,
        "margen": margen,
    }
    return metricas, df
