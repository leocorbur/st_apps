import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os

st.set_page_config(page_title="Formulario de Registro", page_icon="📝")

SECRETO_PATH = "/etc/secrets/GOOGLE_CREDENTIALS"

if not os.path.exists(SECRETO_PATH):
    st.error("❌ No se encontró el archivo de credenciales.")
    st.stop()

try:
    with open(SECRETO_PATH) as f:
        credenciales_json = json.load(f)

    creds = Credentials.from_service_account_info(credenciales_json, scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(creds)
    sheet = client.open("maestra_vendedores").sheet1
except Exception as e:
    st.error(f"⚠️ Error al conectar con Google Sheets: {e}")
    st.stop()


st.title("📋 Formulario de Registro de Vendedores")

with st.form("formulario_registro"):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo electrónico")
    dni = st.text_input("DNI")

    submitted = st.form_submit_button("Enviar")

    if submitted:
        if nombre and correo and dni:
            try:
                sheet.append_row([nombre, correo, dni])
                st.success("✅ Datos enviados correctamente.")
            except Exception as e:
                st.error(f"❌ Error al guardar datos: {e}")
        else:
            st.warning("Por favor completa todos los campos.")
            

# Mostrar los datos actuales de la hoja
st.subheader("📄 Datos registrados")

try:
    # Obtiene todas las filas como lista de diccionarios
    registros = sheet.get_all_records()
    
    if registros:
        # Mostrar como DataFrame
        import pandas as pd
        df = pd.DataFrame(registros)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay registros en la hoja.")
except Exception as e:
    st.error(f"⚠️ Error al obtener datos: {e}")
