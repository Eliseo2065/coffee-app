import pandas as pd


def validar_excel(df: pd.DataFrame, permitir_negativos: bool = False) -> pd.DataFrame:
    """
    Normaliza nombres de columnas y valida que el DataFrame tenga la
    estructura mínima requerida para el análisis de ventas.

    Columnas obligatorias: fecha, producto, cantidad, precio_venta, costo_unitario.

    Valida:
        - Presencia de todas las columnas obligatorias (reporta todas las
          faltantes de una vez, no solo la primera).
        - Que no existan columnas duplicadas tras normalizar nombres.
        - Que cantidad, precio_venta y costo_unitario sean numéricas.
        - Que no haya negativos en esas columnas (salvo que
          permitir_negativos=True, por ejemplo si tu negocio registra
          devoluciones como cantidad negativa).
        - Que todas las fechas sean parseables.

    Args:
        df: DataFrame crudo leído del Excel.
        permitir_negativos: si False (default), lanza error ante valores
            negativos en cantidad/precio_venta/costo_unitario. Cambia a
            True si tu negocio usa negativos intencionalmente (devoluciones).

    Returns:
        Una copia del DataFrame con columnas normalizadas y tipos corregidos.

    Raises:
        ValueError: si falta alguna columna, hay columnas duplicadas,
            valores no numéricos, negativos no permitidos, o fechas inválidas.
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    if df.columns.duplicated().any():
        duplicadas = df.columns[df.columns.duplicated()].unique().tolist()
        raise ValueError(
            f"El archivo tiene columnas duplicadas tras normalizar nombres: "
            f"{', '.join(duplicadas)}"
        )

    columnas_obligatorias = [
        "fecha",
        "producto",
        "cantidad",
        "precio_venta",
        "costo_unitario",
    ]
    faltantes = [col for col in columnas_obligatorias if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan las columnas: {', '.join(faltantes)}")

    columnas_numericas = ["cantidad", "precio_venta", "costo_unitario"]
    for col in columnas_numericas:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        n_invalidos = df[col].isna().sum()
        if n_invalidos > 0:
            raise ValueError(
                f"Hay {n_invalidos} valor(es) no numérico(s) o vacío(s) "
                f"en la columna '{col}'."
            )
        if not permitir_negativos and (df[col] < 0).any():
            n_negativos = (df[col] < 0).sum()
            raise ValueError(
                f"Hay {n_negativos} valor(es) negativo(s) en la columna '{col}'. "
                f"Si son devoluciones intencionales, llama a validar_excel "
                f"con permitir_negativos=True."
            )

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    n_fechas_invalidas = df["fecha"].isna().sum()
    if n_fechas_invalidas > 0:
        raise ValueError(f"{n_fechas_invalidas} fecha(s) inválida(s) en el archivo.")

    return df
