import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Buscador de Puntos", layout="centered")

# Estilo básico
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
html, body, .block-container, .stApp {
    background-color: #f5f0ff !important;
    font-family: 'Montserrat', sans-serif;
}
.logo-container {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    margin-bottom: 20px;
}
.logo-frame {
    background-color: white;
    padding: 15px;
    border-radius: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    width: 50%;
    max-width: 400px;
    margin: auto;
}
.titulo {
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: #3f007f;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Contraseña fija
PASSWORD = "Lostmary.elfbar25"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="titulo">BUSCADOR DE PUNTOS</div>', unsafe_allow_html=True)
    password_input = st.text_input("Introduce la contraseña para acceder:", type="password")
    if st.button("Entrar"):
        if password_input == PASSWORD:
            st.session_state.auth = True
            st.experimental_rerun()
        else:
            st.error("Contraseña incorrecta")
else:
    st.markdown('<div class="logo-container"><div class="logo-frame">', unsafe_allow_html=True)
    st.image("logo.png", use_container_width=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="titulo">BUSCADOR DE PUNTOS</div>', unsafe_allow_html=True)

    # Carga de datos (Ejemplo: desde CSV local o desde URL pública)
    # Aquí debes adaptar con la ruta correcta o URL pública de tu Excel convertido a CSV o Google Sheets export
    # Ejemplo: df = pd.read_csv('datos_puntos.csv')

    # Para demo, pongo unos datos de ejemplo
    data = {
        "Usuario": ["usuario1@gmail.com", "usuario2@gmail.com", "usuario3@gmail.com"],
        "Expendiduría": ["Expendiduría A", "Expendiduría B", "Expendiduría C"],
        "TELÉFONO": ["600123456", "600654321", "600789123"]
    }
    df = pd.DataFrame(data)

    busqueda = st.text_input("Busca por teléfono, usuario o expendiduría").lower().strip()

    if busqueda:
        resultados = df[
            df["Usuario"].str.lower().str.contains(busqueda) |
            df["Expendiduría"].str.lower().str.contains(busqueda) |
            df["TELÉFONO"].str.lower().str.contains(busqueda)
        ]
        if not resultados.empty:
            st.table(resultados)
        else:
            st.info("No se encontraron resultados para esa búsqueda.")
