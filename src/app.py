import pandas as pd
import streamlit as st

st.set_page_config(page_title="Coffee App")

st.title("☕ Coffee App")

df = pd.read_excel("data/ventas_cafeteria.xlsx")

st.write("Vista previa de los datos")
st.dataframe(df.head())
