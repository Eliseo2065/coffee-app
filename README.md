# ☕ Coffee App – Análisis de Ventas

### 🔗 Demo Online

👉 [https://coffee-app-coffee-sales-dashboard.streamlit.app/](https://coffee-app-coffee-sales-dashboard.streamlit.app/)

## 📌 Descripción

Coffee App es una aplicación interactiva desarrollada en **Python** y **Streamlit** que permite analizar las ventas de una cafetería a partir de datos almacenados en un archivo Excel. La app transforma datos crudos en información útil mediante KPIs, gráficos y visualizaciones claras.

El objetivo del proyecto es simular un flujo real de trabajo de análisis de datos: carga, limpieza, transformación y visualización.

---

## 🚀 Funcionalidades

* Visualización completa de los datos de ventas
* KPIs clave:

  * Ventas totales
  * Unidades vendidas
  * Ganancia total
* Gráficos interactivos:

  * Ventas por categoría
  * Ventas por producto
  * Evolución de ventas en el tiempo
* Cálculo automático de ventas, costos y ganancias

---

## 🛠️ Tecnologías utilizadas

* Python
* pandas
* Streamlit
* Excel (fuente de datos)

---

## ▶️ Cómo ejecutar el proyecto

1. Clonar el repositorio
2. Crear y activar un entorno virtual (opcional)
3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:

   ```bash
   streamlit run src/app.py
   ```

---

## 📊 Dataset

El archivo `ventas_cafeteria.xlsx` contiene las siguientes columnas:

* `fecha`
* `producto`
* `categoria`
* `cantidad`
* `precio_unitario`
* `costo_unitario`

A partir de estas columnas, la aplicación calcula métricas clave de negocio.

---

## 🧠 Aprendizajes del proyecto

* Diseño de dashboards interactivos con Streamlit
* Aplicación de KPIs de negocio (ventas, ganancia, margen)
* Uso de filtros dinámicos para análisis exploratorio
* Limpieza y transformación de datos con pandas
* Flujo de trabajo profesional con Git y GitHub
* Deploy de aplicaciones de datos en Streamlit Cloud

---

## 🌐 Próximos pasos

* Agregar filtros interactivos por fecha, producto y categoría
* Desplegar la app en Streamlit Cloud
* Incorporar más métricas de negocio


