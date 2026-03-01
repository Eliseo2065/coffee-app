import streamlit as st
import pandas as pd
import plotly.express as px
from core.metricas import calcular_metricas
from core.validaciones import validar_excel
from core.alertas import generar_alertas

# ------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------
st.set_page_config(
    page_title="Coffee Intelligence",
    page_icon="☕",
    layout="wide"
)

st.title("Coffee Intelligence")
st.caption("Panel ejecutivo de rendimiento por local")

st.divider()

# ------------------------------------------------
# CARGA DE DATOS
# ------------------------------------------------
RUTA_DATA = "data/ventas_cafeteria.xlsx"

try:
    df = pd.read_excel(RUTA_DATA)
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# ------------------------------------------------
# VALIDACIONES
# ------------------------------------------------
try:
    df = validar_excel(df)
except ValueError as e:
    st.error(f"Error de validación: {e}")
    st.stop()

# ------------------------------------------------
# FILTRO POR LOCAL
# ------------------------------------------------
if "local" in df.columns:
    locales = df["local"].unique()
    seleccion = st.selectbox(
        "Seleccionar local",
        options=["Todos"] + list(locales)
    )

    if seleccion != "Todos":
        df = df[df["local"] == seleccion]

# Si no hay datos después del filtro
if df.empty:
    st.warning("No hay datos para esta selección.")
    st.stop()

# ------------------------------------------------
# CÁLCULO DE MÉTRICAS
# ------------------------------------------------
metricas, df_procesado = calcular_metricas(df)

st.divider()

# ------------------------------------------------
# MÉTRICAS PRINCIPALES
# ------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", f"${metricas['ventas_totales']:,.0f}")
col2.metric("Unidades", f"{metricas['unidades']:,.0f}")
col3.metric("Ticket Promedio", f"${metricas['ticket_promedio']:,.0f}")

col4, col5 = st.columns(2)
col4.metric("Ganancia Total", f"${metricas['ganancia_total']:,.0f}")
col5.metric("Margen (%)", f"{metricas['margen']:.1f}%")

# ------------------------------------------------
# ALERTAS
# ------------------------------------------------
alertas = generar_alertas(df_procesado)

if alertas:
    st.divider()
    st.subheader("Alertas")
    for alerta in alertas:
        st.warning(alerta)

# ------------------------------------------------
# VENTAS POR PRODUCTO
# ------------------------------------------------
st.divider()
st.subheader("Ventas por Producto")

resumen_ventas = (
    df_procesado
    .groupby("producto")["venta_total"]
    .sum()
    .reset_index()
    .sort_values("venta_total", ascending=False)
)

fig_ventas = px.bar(
    resumen_ventas,
    x="producto",
    y="venta_total"
)

fig_ventas.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0E1117",
    plot_bgcolor="#1A1F2B",
    font=dict(color="#EAEAEA"),
    yaxis_title="Venta Total"
)

fig_ventas.update_traces(marker_color="#C49A6C")

st.plotly_chart(fig_ventas, use_container_width=True)

# ------------------------------------------------
# RENTABILIDAD POR PRODUCTO
# ------------------------------------------------
st.divider()
st.subheader("Rentabilidad por Producto")

resumen_rentabilidad = (
    df_procesado
    .groupby("producto")
    .agg({
        "venta_total": "sum",
        "ganancia": "sum"
    })
    .reset_index()
)

resumen_rentabilidad["margen_%"] = (
    resumen_rentabilidad["ganancia"] /
    resumen_rentabilidad["venta_total"] * 100
)

resumen_rentabilidad = resumen_rentabilidad.sort_values(
    "ganancia",
    ascending=False
)

fig_rentabilidad = px.bar(
    resumen_rentabilidad,
    x="producto",
    y="ganancia",
    text="margen_%"
)

fig_rentabilidad.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0E1117",
    plot_bgcolor="#1A1F2B",
    font=dict(color="#EAEAEA"),
    yaxis_title="Ganancia Total"
)

fig_rentabilidad.update_traces(
    marker_color="#4CAF50",
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(fig_rentabilidad, use_container_width=True)

# ------------------------------------------------
# TENDENCIA DE VENTAS
# ------------------------------------------------
st.divider()
st.subheader("Tendencia de Ventas")

resumen_fecha = (
    df_procesado
    .groupby("fecha")["venta_total"]
    .sum()
    .reset_index()
    .sort_values("fecha")
)

fig_fecha = px.line(
    resumen_fecha,
    x="fecha",
    y="venta_total"
)

fig_fecha.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0E1117",
    plot_bgcolor="#1A1F2B",
    font=dict(color="#EAEAEA")
)

fig_fecha.update_traces(line_color="#C49A6C")

st.plotly_chart(fig_fecha, use_container_width=True)

# ------------------------------------------------
# TABLA FINAL
# ------------------------------------------------
st.divider()
st.subheader("Detalle de Datos")

st.dataframe(df_procesado, use_container_width=True)