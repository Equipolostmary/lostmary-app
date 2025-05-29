import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread

st.set_page_config(page_title="Buscador de Puntos", layout="centered")

# ======== ESTILO VISUAL GENERAL ========
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

# ======== LOGO Y TÍTULO ========
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("logo.png", width=300)
st.markdown('</div>', unsafe_allow_html=True)
st.title("BUSCADOR DE PUNTOS")

# ======== AUTENTICACIÓN ========
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
    # ======== CONEXIÓN CON GOOGLE SHEETS ========
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)

    SHEET_ID = "1a14wIe2893oS7zhicvT4mU0N_dM3vqItkTfJdHB325A"
    try:
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet("Registro")
        df = pd.DataFrame(worksheet.get_all_records())
        df.columns = df.columns.str.strip()  # LIMPIA LOS NOMBRES DE COLUMNAS
    except Exception as e:
        st.error(f"Error al cargar la hoja de cálculo: {e}")
        st.stop()

    # ======== BUSCADOR MULTICAMPO ========
    termino = st.text_input("Buscar por Usuario, Teléfono, Expendiduría o Nombre").strip().lower()

    if termino:
        resultados = df[
            (df["Usuario"].str.lower() != "equipolostmary@gmail.com") & (
                df["Usuario"].str.lower().str.contains(termino) |
                df["TELÉFONO"].astype(str).str.lower().str.contains(termino) |
                df["Expendiduría"].astype(str).str.lower().str.contains(termino) |
                df["Nombre"].str.lower().str.contains(termino)
            )
        ]

        if not resultados.empty:
            st.success(f"{len(resultados)} resultado(s) encontrado(s):")
            for _, row in resultados.iterrows():
                st.markdown("---")
                st.markdown(f"**Usuario:** {row.get('Usuario', '')}")
                st.markdown(f"**Contraseña:** {row.get('Contraseña', '')}")
                st.markdown(f"**Expendiduría:** {row.get('Expendiduría', '')}")
                st.markdown(f"**Teléfono:** {row.get('TELÉFONO', '')}")
                st.markdown(f"**Nombre:** {row.get('Nombre', '')}")
                st.markdown(f"**Promoción 3x10 TAPPO:** {row.get('Promoción 3x10 TAPPO', '')}")
                st.markdown(f"**Promoción 3×21 BM1000:** {row.get('Promoción 3×21 BM1000', '')}")
                st.markdown(f"**TOTAL PROMOS:** {row.get('TOTAL PROMOS', '')}")
                st.markdown(f"**PENDIENTE DE REPONER:** {row.get('PENDIENTE DE REPONER', '')}")
                st.markdown(f"**REPUESTOS:** {row.get('REPUESTOS', '')}")
        else:
            st.warning("No se encontró ningún punto con ese dato.")
