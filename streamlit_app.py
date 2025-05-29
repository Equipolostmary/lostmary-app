import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread

st.set_page_config(page_title="Buscador de Puntos", layout="centered")

# Estilo simple con el logo y título
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
body, .stApp {
    background-color: #e6e0f8;
    font-family: 'Montserrat', sans-serif;
}
h1 {
    color: #3f0071;
    font-weight: 700;
    text-align: center;
    margin-bottom: 20px;
}
.logo-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("logo.png", width=300)
st.markdown('</div>', unsafe_allow_html=True)

st.title("BUSCADOR DE PUNTOS")

# Contraseña fija para entrar
password_input = st.text_input("Introduce la contraseña para acceder:", type="password")
if "access_granted" not in st.session_state:
    st.session_state["access_granted"] = False

if not st.session_state["access_granted"]:
    if st.button("Entrar"):
        if password_input == "Lostmary.elfbar25":
            st.session_state["access_granted"] = True
            st.experimental_rerun()
        else:
            st.error("Contraseña incorrecta.")
else:
    # Acceso concedido, mostrar buscador

    # Conexión Google Sheets
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)

    # ID fijo de la hoja (puedes reemplazar por el tuyo si es otro)
    SHEET_ID = "1CpHwmPrRYqqMtXrZBZV7-nQOeEH6Z-RWtpnT84ztVB0"
    try:
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet("Registro")
        df = pd.DataFrame(worksheet.get_all_records())
    except Exception as e:
        st.error(f"Error al cargar la hoja de cálculo: {e}")
        st.stop()

    # Buscador simple por teléfono, correo, expendiduría o usuario
    termino = st.text_input("Buscar por teléfono, correo, expendiduría o usuario").strip().lower()

    if termino:
        resultados = df[df.apply(lambda row: termino in str(row.get("TELÉFONO", "")).lower()
                                              or termino in str(row.get("Usuario", "")).lower()
                                              or termino in str(row.get("Expendiduría", "")).lower()
                                              or termino in str(row.get("Usuario", "")).lower(), axis=1)]

        if not resultados.empty:
            st.info(f"{len(resultados)} resultado(s) encontrado(s).")
            for _, row in resultados.iterrows():
                st.markdown(f"- **Usuario:** {row.get('Usuario','')}")
                st.markdown(f"- **Contraseña:** {row.get('Contraseña','')}")
                st.markdown(f"- **Expendiduría:** {row.get('Expendiduría','')}")
                st.markdown(f"- **Teléfono:** {row.get('TELÉFONO','')}")
                st.markdown("---")
        else:
            st.warning("No se encontró ningún punto con ese dato.")
