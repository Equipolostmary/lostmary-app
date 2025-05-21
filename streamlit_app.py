
import streamlit as st
from google_sheets import cargar_datos_hoja
import pandas as pd

# CONFIGURA TU GOOGLE SHEET
SHEET_URL = "https://docs.google.com/spreadsheets/d/1a14wIe2893oS7zhicvT4mU0N_dM3vqItkTfJdHB325A"
PESTAÑA = "Registro"

# CARGAR DATOS DESDE GOOGLE SHEET
@st.cache_data
def cargar_datos():
    return cargar_datos_hoja(SHEET_URL, pestaña=PESTAÑA)

# INTERFAZ DE STREAMLIT
st.set_page_config(page_title="Lost Mary - Área de Puntos", layout="centered")

st.image("https://lostmary-es.com/cdn/shop/files/logo_lostmary.png", width=150)
st.title("Área de Puntos de Venta")
st.write("Introduce tu correo para acceder a tu área personalizada:")

correo = st.text_input("Correo electrónico").strip().lower()

if correo:
    datos = cargar_datos()
    if correo in datos["Correo electrónico"].str.lower().values:
        punto = datos[datos["Correo electrónico"].str.lower() == correo].iloc[0]
        st.success(f"¡Bienvenido, {punto['Nombre del punto de venta']}!")

        promociones = st.number_input("¿Cuántas promociones vas a subir?", min_value=1, step=1)
        imagenes = st.file_uploader("Sube las fotos de los tickets o promociones", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if st.button("Subir promociones"):
            st.info("Funcionalidad de subida en desarrollo. Tus archivos se guardarían en tu carpeta de Google Drive asignada.")
            st.write("Número de promociones:", promociones)
            st.write("Archivos subidos:", [img.name for img in imagenes])

    else:
        st.error("Correo no encontrado. Asegúrate de que el correo esté registrado en el formulario.")
