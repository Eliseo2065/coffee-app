import streamlit as st
import pandas as pd

# ---------------------------------
# Configuración de la página
# ---------------------------------
st.set_page_config(
    page_title="Coffee App ☕",
    layout="wide"
)

st.title("☕ Coffee App – Dashboard de Ventas")
st.caption("Análisis interactivo para cafeterías")

# ---------------------------------
# Carga optimizada de datos
# ---------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_excel("data/ventas_cafeteria.xlsx")

    # Normalizar columnas
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["venta_total"] = df["cantidad"] * df["precio_unitario"]
    df["costo_total"] = df["cantidad"] * df["costo_unitario"]
    df["ganancia"] = df["venta_total"] - df["costo_total"]

    return df

with st.spinner("Cargando datos..."):
    df = load_data()

# ---------------------------------
# Sidebar - Filtros
# ---------------------------------
st.sidebar.header("🔎 Filtros")

fecha_min, fecha_max = df["fecha"].min(), df["fecha"].max()
rango_fechas = st.sidebar.date_input(
    "📅 Rango de fechas",
    [fecha_min, fecha_max]
)

categorias = st.sidebar.multiselect(
    "🏷️ Categoría",
    options=sorted(df["categoria"].unique()),
    default=sorted(df["categoria"].unique())
)

productos = st.sidebar.multiselect(
    "☕ Producto",
    options=sorted(df["producto"].unique()),
    default=sorted(df["producto"].unique())
)

metrica = st.sidebar.selectbox(
    "📊 Métrica principal",
    {
        "Ventas ($)": "venta_total",
        "Ganancia ($)": "ganancia",
        "Unidades vendidas": "cantidad"
    }
)

# ---------------------------------
# Aplicar filtros
# ---------------------------------
df_filtrado = df[
    (df["fecha"].between(pd.to_datetime(rango_fechas[0]), pd.to_datetime(rango_fechas[1])))
    & (df["categoria"].isin(categorias))
    & (df["producto"].isin(productos))
]

# ---------------------------------
# Validación: datos vacíos
# ---------------------------------
if df_filtrado.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados.")
    st.stop()

# ---------------------------------
# KPIs
# ---------------------------------
ventas_totales = df_filtrado["venta_total"].sum()
unidades = df_filtrado["cantidad"].sum()
ganancia_total = df_filtrado["ganancia"].sum()

ticket_promedio = ventas_totales / len(df_filtrado)
margen = (ganancia_total / ventas_totales) * 100 if ventas_totales > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Ventas Totales", f"${ventas_totales:,.0f}")
col2.metric("📦 Unidades Vendidas", int(unidades))
col3.metric("🧮 Ganancia Total", f"${ganancia_total:,.0f}")
col4.metric("🧾 Ticket Promedio", f"${ticket_promedio:,.0f}")
col5.metric("📈 Margen", f"{margen:.1f}%")

st.divider()

# ---------------------------------
# Ventas por categoría
# ---------------------------------
st.subheader("📊 Ventas por Categoría")

ventas_categoria = (
    df_filtrado
    .groupby("categoria")[metrica]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(ventas_categoria)

# ---------------------------------
# Ventas por producto
# ---------------------------------
st.subheader("🥐 Ventas por Producto")

ventas_producto = (
    df_filtrado
    .groupby("producto")[metrica]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(ventas_producto)

# ---------------------------------
# Top 5 productos
# ---------------------------------
st.subheader("🏆 Top 5 Productos")

top_5 = (
    df_filtrado
    .groupby("producto")[metrica]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(top_5)



# ---------------------------------
# Evolución temporal
# ---------------------------------
st.subheader("📈 Evolución en el Tiempo")

ventas_tiempo = (
    df_filtrado
    .groupby("fecha")[metrica]
    .sum()
)

st.line_chart(ventas_tiempo)

# ---------------------------------
# Tabla final
# ---------------------------------
st.subheader("📋 Datos Detallados")
st.dataframe(df_filtrado, use_container_width=True)


