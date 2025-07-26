import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os

st.set_page_config(page_title="Formulario de Registro", page_icon="📝")

credenciales_json = os.environ.get("GOOGLE_CREDENTIALS")

if credenciales_json is None:
    st.error("No se encontró la variable de entorno GOOGLE_CREDENTIALS.")
    st.stop()

try:
    info = json.loads(credenciales_json)
    creds = Credentials.from_service_account_info(info, scopes=[
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