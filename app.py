import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from core.metricas import calcular_metricas
from core.validaciones import validar_excel
from core.alertas import generar_alertas

# ------------------------------------------------
# CONSTANTES
# ------------------------------------------------
RUTA_DATA = "data/ventas_cafeteria.xlsx"

COL_PRODUCTO = "producto"
COL_FECHA = "fecha"
COL_LOCAL = "local"
COL_VENTA_TOTAL = "venta_total"
COL_GANANCIA = "ganancia"

COLOR_FONDO_PAPEL = "#0E1117"
COLOR_FONDO_GRAFICO = "#1A1F2B"
COLOR_FUENTE = "#EAEAEA"
COLOR_ACENTO_VENTAS = "#C49A6C"
COLOR_ACENTO_GANANCIA = "#4CAF50"


# ------------------------------------------------
# HELPERS
# ------------------------------------------------
def aplicar_estilo_oscuro(fig: go.Figure, titulo_eje_y: str | None = None) -> go.Figure:
    """Aplica el tema oscuro estándar de la app a cualquier gráfico Plotly."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_FUENTE),
    )
    if titulo_eje_y:
        fig.update_layout(yaxis_title=titulo_eje_y)
    return fig


@st.cache_data
def cargar_y_procesar_datos(ruta: str) -> pd.DataFrame:
    """
    Carga el Excel, lo valida y calcula métricas base. Cacheado: solo se
    vuelve a ejecutar si cambia el archivo, no en cada interacción del usuario.
    """
    df = pd.read_excel(ruta)
    df = validar_excel(df)
    return df


# ------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------
st.set_page_config(page_title="Coffee Intelligence", page_icon="☕", layout="wide")
st.title("Coffee Intelligence")
st.caption("Panel ejecutivo de rendimiento por local")
st.divider()

# ------------------------------------------------
# CARGA Y VALIDACIÓN DE DATOS (cacheado)
# ------------------------------------------------
try:
    df = cargar_y_procesar_datos(RUTA_DATA)
except FileNotFoundError:
    st.error(f"No se encontró el archivo de datos en '{RUTA_DATA}'.")
    st.stop()
except ValueError as e:
    st.error(f"Error de validación: {e}")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# ------------------------------------------------
# FILTRO POR LOCAL
# ------------------------------------------------
if COL_LOCAL in df.columns:
    locales = df[COL_LOCAL].unique()
    seleccion = st.selectbox("Seleccionar local", options=["Todos"] + list(locales))
    if seleccion != "Todos":
        df = df[df[COL_LOCAL] == seleccion]

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
    df_procesado.groupby(COL_PRODUCTO)[COL_VENTA_TOTAL]
    .sum()
    .reset_index()
    .sort_values(COL_VENTA_TOTAL, ascending=False)
)

fig_ventas = px.bar(resumen_ventas, x=COL_PRODUCTO, y=COL_VENTA_TOTAL)
fig_ventas.update_traces(marker_color=COLOR_ACENTO_VENTAS)
aplicar_estilo_oscuro(fig_ventas, titulo_eje_y="Venta Total")
st.plotly_chart(fig_ventas, use_container_width=True)

# ------------------------------------------------
# RENTABILIDAD POR PRODUCTO
# ------------------------------------------------
st.divider()
st.subheader("Rentabilidad por Producto")

resumen_rentabilidad = (
    df_procesado.groupby(COL_PRODUCTO)
    .agg({COL_VENTA_TOTAL: "sum", COL_GANANCIA: "sum"})
    .reset_index()
)
resumen_rentabilidad["margen_%"] = (
    resumen_rentabilidad[COL_GANANCIA] / resumen_rentabilidad[COL_VENTA_TOTAL] * 100
)
resumen_rentabilidad = resumen_rentabilidad.sort_values(COL_GANANCIA, ascending=False)

fig_rentabilidad = px.bar(
    resumen_rentabilidad, x=COL_PRODUCTO, y=COL_GANANCIA, text="margen_%"
)
fig_rentabilidad.update_traces(
    marker_color=COLOR_ACENTO_GANANCIA,
    texttemplate="%{text:.1f}%",
    textposition="outside",
)
aplicar_estilo_oscuro(fig_rentabilidad, titulo_eje_y="Ganancia Total")
st.plotly_chart(fig_rentabilidad, use_container_width=True)

# ------------------------------------------------
# TENDENCIA DE VENTAS
# ------------------------------------------------
st.divider()
st.subheader("Tendencia de Ventas")

resumen_fecha = (
    df_procesado.groupby(COL_FECHA)[COL_VENTA_TOTAL]
    .sum()
    .reset_index()
    .sort_values(COL_FECHA)
)

fig_fecha = px.line(resumen_fecha, x=COL_FECHA, y=COL_VENTA_TOTAL)
fig_fecha.update_traces(line_color=COLOR_ACENTO_VENTAS)
aplicar_estilo_oscuro(fig_fecha)
st.plotly_chart(fig_fecha, use_container_width=True)

# ------------------------------------------------
# TABLA FINAL
# ------------------------------------------------
st.divider()
st.subheader("Detalle de Datos")
st.dataframe(df_procesado, use_container_width=True)
