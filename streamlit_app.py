import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread

# Configuración de página
st.set_page_config(page_title="Buscador de Puntos - Lost Mary", layout="centered")

# Estilo general
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
html, body, .block-container, .stApp {
    background-color: #e6e0f8 !important;
    font-family: 'Montserrat', sans-serif;
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
    color: #3b0061;
    margin: 20px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Mostrar logo
st.markdown('<div class="logo-container"><div class="logo-frame">', unsafe_allow_html=True)
st.image("logo.png", use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div class="titulo">BUSCADOR DE PUNTOS</div>', unsafe_allow_html=True)

# Estado de autenticación en session_state
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# Contraseña para acceso
if not st.session_state["autenticado"]:
    clave = st.text_input("Introduce la contraseña para acceder:", type="password")
    if st.button("Entrar"):
        if clave == "Lostmary.elfbar25":
            st.session_state["autenticado"] = True
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

    termino = st.text_input("Buscar por teléfono, correo, expendiduría o usuario").strip().lower()

    if termino:
        resultados = df[df.apply(lambda row: termino in str(row.get("TELÉFONO", "")).lower()
                                            or termino in str(row.get("Usuario", "")).lower()
                                            or termino in str(row.get("Expendiduría", "")).lower(), axis=1)]

        if not resultados.empty:
            st.info(f"{len(resultados)} resultado(s) encontrado(s).")
            for i, row in resultados.iterrows():
                st.markdown(f"- **Usuario:** {row['Usuario']}")
                st.markdown(f"- **Contraseña:** {row.get('Contraseña', 'No disponible')}")
                st.markdown(f"- **Expendiduría:** {row['Expendiduría']}")
                st.markdown(f"- **Teléfono:** {row['TELÉFONO']}")
                st.markdown("---")
        else:
            st.warning("No se encontró ningún punto con ese dato.")
