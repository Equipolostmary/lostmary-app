import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account

# Configuración de página
st.set_page_config(page_title="Buscador de Puntos", layout="centered")

# Estilo simple
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
body, .stApp {
    background-color: #e6e0f8 !important;
    font-family: 'Montserrat', sans-serif;
}
.logo-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
.titulo {
    text-align: center;
    font-weight: bold;
    font-size: 28px;
    color: #3d0075;
    margin-top: 20px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Mostrar logo
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("logo.png", width=300)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="titulo">BUSCADOR DE PUNTOS</div>', unsafe_allow_html=True)

# Contraseña fija
password = st.text_input("Introduce la contraseña para acceder:", type="password")

if password != "Lostmary.elfbar25":
    st.warning("Contraseña incorrecta o no ingresada.")
    st.stop()

# Ya dentro de la app:
# Autenticación con cuenta fija para el buscador
USUARIO_FIJO = "equipolostmary@gmail.com"

# Autenticación Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scopes)
client = gspread.authorize(creds)

# Abrir hoja y cargar datos
sheet = client.open_by_key(st.secrets["gcp_service_account"]["sheet_id"])
worksheet = sheet.worksheet("Registro")
df = pd.DataFrame(worksheet.get_all_records())

def buscar_usuario(email):
    mask = df["Usuario"].astype(str).str.lower() == email.lower().strip()
    return df[mask].iloc[0] if mask.any() else None

# Buscar el usuario fijo
user = buscar_usuario(USUARIO_FIJO)
if user is None:
    st.error("Usuario fijo no encontrado en la base de datos.")
    st.stop()

# Input para búsqueda
termino = st.text_input("Buscar por teléfono, correo, expendiduría o usuario").strip().lower()

if termino:
    resultados = df[df.apply(lambda row: termino in str(row.get("TELÉFONO", "")).lower()
                                        or termino in str(row.get("Usuario", "")).lower()
                                        or termino in str(row.get("Expendiduría", "")).lower(), axis=1)]
    if not resultados.empty:
        st.info(f"{len(resultados)} resultado(s) encontrado(s).")
        for _, row in resultados.iterrows():
            st.markdown(f"- **Usuario:** {row['Usuario']}")
            st.markdown(f"  - Expendiduría: {row['Expendiduría']}")
            st.markdown(f"  - Teléfono: {row['TELÉFONO']}")
            st.markdown("---")
    else:
        st.warning("No se encontró ningún punto con ese dato.")
