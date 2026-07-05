import pandas as pd


def generar_alertas(
    df: pd.DataFrame,
    umbral_outlier: float = 3.0,
    umbral_volumen_bajo: float = 1.0,
) -> list[str]:
    """
    Genera alertas descriptivas sobre patrones inusuales en las ventas.

    Args:
        df: DataFrame con columnas venta_total y/o cantidad (ya calculadas
            por metricas.calcular_metricas).
        umbral_outlier: múltiplo de la mediana por encima del cual una
            venta se considera inusualmente alta. Default 3.0.
        umbral_volumen_bajo: cantidad promedio por debajo de la cual se
            alerta bajo volumen. Ajusta este valor si tu negocio vende
            productos por fracciones (ej. por kilo), donde promedios
            menores a 1 pueden ser normales.

    Returns:
        Lista de strings con alertas legibles y con datos concretos
        (producto, fecha, monto), no solo genéricas.
    """
    alertas = []

    if "venta_total" in df.columns and len(df) > 0:
        mediana = df["venta_total"].median()
        maximo = df["venta_total"].max()
        if mediana > 0 and maximo > mediana * umbral_outlier:
            fila_max = df.loc[df["venta_total"].idxmax()]
            producto = fila_max.get("producto", "producto sin identificar")
            fecha = fila_max.get("fecha", "fecha desconocida")
            alertas.append(
                f"Venta inusualmente alta: {producto} el {fecha} "
                f"por ${maximo:,.0f} (mediana: ${mediana:,.0f})."
            )

    if "cantidad" in df.columns and len(df) > 0:
        promedio_cantidad = df["cantidad"].mean()
        if promedio_cantidad < umbral_volumen_bajo:
            alertas.append(
                f"El volumen promedio de venta es bajo: {promedio_cantidad:.2f} "
                f"unidades por transacción (umbral: {umbral_volumen_bajo})."
            )

    return alertas
