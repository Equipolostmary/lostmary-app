import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
import time
import re

st.set_page_config(page_title="Buscador de Puntos", layout="centered")

# ====== Estilo simple ======
st.markdown("""
<style>
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
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 30px;
    color: #4B0082;
}
</style>
""", unsafe_allow_html=True)

# Mostrar logo
st.markdown('<div class="logo-container"><div class="logo-frame">', unsafe_allow_html=True)
st.image("logo.png", use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="titulo">BUSCADOR DE PUNTOS</div>', unsafe_allow_html=True)

# Contraseña fija
PASSWORD = "Lostmary.elfbar25"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    pwd = st.text_input("Introduce la contraseña para acceder:", type="password")
    if st.button("Entrar"):
        if pwd == PASSWORD:
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Contraseña incorrecta.")
else:
    # Conexión a Google Sheets
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(st.secrets["gcp_service_account"]["sheet_id"])
    worksheet = sheet.worksheet("Registro")
    df = pd.DataFrame(worksheet.get_all_records())

    st.markdown("### 🔎 Buscar por teléfono, correo, expendiduría o usuario")
    termino = st.text_input("Escribe para buscar").strip().lower()

    if termino:
        resultados = df[df.apply(lambda row: termino in str(row.get("TELÉFONO", "")).lower()
                                            or termino in str(row.get("Usuario", "")).lower()
                                            or termino in str(row.get("Expendiduría", "")).lower(), axis=1)]
        if not resultados.empty:
            opciones = [f"{row['Usuario']} - {row['Expendiduría']} - {row['TELÉFONO']}" for _, row in resultados.iterrows()]
            seleccion = st.selectbox("Selecciona un punto para editar:", opciones)
            index = resultados.index[opciones.index(seleccion)]

            with st.form(f"editar_usuario_{index}"):
                nuevos_valores = {}
                for col in df.columns:
                    if col != "Carpeta privada":
                        nuevos_valores[col] = st.text_input(col, str(df.at[index, col]), key=f"{col}_{index}")
                guardar = st.form_submit_button("Guardar cambios")
                if guardar:
                    try:
                        for col, nuevo_valor in nuevos_valores.items():
                            worksheet.update_cell(index + 2, df.columns.get_loc(col) + 1, nuevo_valor)
                        st.success("✅ Datos actualizados correctamente.")
                        time.sleep(2)
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
        else:
            st.warning("No se encontró ningún punto con ese dato.")

    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.experimental_rerun()
