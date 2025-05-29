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

# ======== SESIÓN ========
if "access_granted" not in st.session_state:
    st.session_state["access_granted"] = False

# ======== LOGIN ========
if not st.session_state["access_granted"]:
    password_input = st.text_input("Introduce la contraseña para acceder:", type="password")
    if st.button("Entrar"):
        if password_input == "Lostmary.elfbar25":
            st.session_state["access_granted"] = True
        else:
            st.error("Contraseña incorrecta.")

else:
    # ======== BOTÓN DE CIERRE DE SESIÓN ========
    if st.button("Cerrar sesión"):
        st.session_state["access_granted"] = False
        st.experimental_rerun()

    # ======== CONEXIÓN GOOGLE SHEETS ========
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)

    SHEET_ID = "1a14wIe2893oS7zhicvT4mU0N_dM3vqItkTfJdHB325A"
    try:
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet("Registro")
        df = pd.DataFrame(worksheet.get_all_records())
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"Error al cargar la hoja de cálculo: {e}")
        st.stop()

    # ======== BUSCADOR ========
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

            if len(resultados) == 1:
                fila = resultados.iloc[0]
            else:
                opciones = [f"{row['Usuario']} - {row['Expendiduría']}" for _, row in resultados.iterrows()]
                seleccion = st.selectbox("Selecciona un punto:", opciones)
                fila = resultados.iloc[opciones.index(seleccion)]

            st.markdown("---")
            st.markdown(f"**Usuario:** {fila.get('Usuario', '')}")
            st.markdown(f"**Contraseña:** {fila.get('Contraseña', '')}")
            st.markdown(f"**Expendiduría:** {fila.get('Expendiduría', '')}")
            st.markdown(f"**Teléfono:** {fila.get('TELÉFONO', '')}")
            st.markdown(f"**Nombre:** {fila.get('Nombre', '')}")
            st.markdown(f"**Responsable de zona:** {fila.get('RESPONSABLE DE ZONA', '')}")
            st.markdown(f"**Promoción 3x10 TAPPO:** {fila.get('Promoción 3x10 TAPPO', '')}")
            st.markdown(f"**Promoción 3×21 BM1000:** {fila.get('Promoción 3×21 BM1000', '')}")
            st.markdown(f"**TOTAL PROMOS:** {fila.get('TOTAL PROMOS', '')}")
            st.markdown(f"**PENDIENTE DE REPONER:** {fila.get('PENDIENTE DE REPONER', '')}")
            st.markdown(f"**REPUESTOS:** {fila.get('REPUESTOS', '')}")
        else:
            st.warning("No se encontró ningún punto con ese dato.")
