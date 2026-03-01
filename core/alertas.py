def generar_alertas(df):
    alertas = []

    if "venta_total" in df.columns:
        promedio = df["venta_total"].mean()
        maximo = df["venta_total"].max()

        if maximo > promedio * 3:
            alertas.append("Se detectó una venta inusualmente alta.")

    if "cantidad" in df.columns:
        if df["cantidad"].mean() < 1:
            alertas.append("El volumen promedio de venta es bajo.")

    if not alertas:
        return []

    return alertas