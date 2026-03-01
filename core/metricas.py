def calcular_metricas(df):

    df = df.copy()

    # Cálculos base
    df["venta_total"] = df["cantidad"] * df["precio_venta"]
    df["costo_total"] = df["cantidad"] * df["costo_unitario"]
    df["ganancia"] = df["venta_total"] - df["costo_total"]

    ventas_totales = df["venta_total"].sum()
    unidades = df["cantidad"].sum()
    ticket_promedio = ventas_totales / unidades if unidades > 0 else 0
    ganancia_total = df["ganancia"].sum()
    margen = (ganancia_total / ventas_totales * 100) if ventas_totales > 0 else 0

    metricas = {
        "ventas_totales": ventas_totales,
        "unidades": unidades,
        "ticket_promedio": ticket_promedio,
        "ganancia_total": ganancia_total,
        "margen": margen
    }

    return metricas, df