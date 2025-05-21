import streamlit as st
import pandas as pd
from google_sheets import cargar_datos_hoja
from paginas.panel_punto import mostrar_panel

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
