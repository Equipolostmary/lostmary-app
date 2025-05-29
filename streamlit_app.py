import streamlit as st 
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2 import service_account
from drive_upload import conectar_drive, subir_archivo_a_drive
import time
import uuid
import re
import os

st.set_page_config(page_title="Lost Mary - Buscador de Puntos", layout="centered")
ADMIN_EMAIL = "equipolostmary@gmail.com"

# ======== ESTILO VISUAL GENERAL ========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
html, body, .block-container, .stApp {
    background-color: #e6e0f8 !important;
    font-family: 'Montserrat', sans-serif;
}
section[data-testid="stSidebar"], #MainMenu, header, footer {
    display: none !important;
}
.logo-container {
    display: flex;
    justify-content: center;
    margin-top: 30px;
    margin-bottom: 10px;
}
.logo-frame {
    background-color: white;
    padding: 10px;
    border-radius: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    width: 60%;
    max-width: 600px;
    margin: auto;
}
.titulo {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: black;
    margin: 20px 0 10px 0;
    background-color: #cdb4f5;
    padding: 10px;
    border-radius: 10px;
}
.seccion {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-top: 30px;
    margin-bottom: 10px;
    border-bottom: 2px solid #bbb;
    padding-bottom: 5px;
}
button[kind="primary"] {
    font-family: 'Montserrat', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# Mostrar logo
st.markdown('<div class="logo-container"><div class="logo-frame">', unsafe_allow_html=True)
st.image("logo.png", use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# Título
st.markdown('<div class="titulo">BUSCADOR DE PUNTOS</div>', unsafe_allow_html=True)

# ============ AUTENTICACIÓN Y DATOS ============

# Contraseña fija para acceder
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    clave = st.text_input("Introduce la contraseña para acceder:", type="password")
    if st.button("Entrar"):
        if clave == "Lostmary.elfbar25":
            st.session_state["autenticado"] = True
            st.experimental_rerun()
        else:
            st.error("Contraseña incorrecta.")
else:
    # Solo carga datos si está autenticado
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(st.secrets["gcp_service_account"]["sheet_id"])
    worksheet = sheet.worksheet("Registro")
    df = pd.DataFrame(worksheet.get_all_records())

    # Campo búsqueda
    termino = st.text_input("Buscar por teléfono, correo, expendiduría o usuario").strip().lower()

    if termino:
        resultados = df[df.apply(lambda row: termino in str(row.get("TELÉFONO", "")).lower()
                                            or termino in str(row.get("Usuario", "")).lower()
                                            or termino in str(row.get("Expendiduría", "")).lower(), axis=1)]
        if not resultados.empty:
            st.info(f"{len(resultados)} resultado(s) encontrado(s).")
            for _, row in resultados.iterrows():
                st.markdown(f"- **Usuario:** {row['Usuario']}")
                st.markdown(f"- **Contraseña:** {row.get('Contraseña', 'No disponible')}")
                st.markdown(f"- Expendiduría: {row['Expendiduría']}")
                st.markdown(f"- Teléfono: {row['TELÉFONO']}")
                st.markdown("---")
        else:
            st.warning("No se encontró ningún punto con ese dato.")
    else:
        # Si no hay término, no mostrar nada
        st.write("")
