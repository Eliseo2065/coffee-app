import pandas as pd

def validar_excel(df):

    df.columns = df.columns.str.strip().str.lower()

    columnas_obligatorias = [
        "fecha",
        "producto",
        "cantidad",
        "precio_venta",
        "costo_unitario"
    ]

    for col in columnas_obligatorias:
        if col not in df.columns:
            raise ValueError(f"Falta la columna {col}")

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    if df["fecha"].isna().any():
        raise ValueError("Hay fechas inválidas en el archivo.")

    return df