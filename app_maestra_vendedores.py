import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os
import datetime
import pytz

st.set_page_config(page_title="Formulario de Registro", page_icon="📝")

# --- Leer archivo secreto con usuarios y contraseñas ---
USUARIOS_PATH = "/etc/secrets/USUARIOS_CONTRASENAS"

if not os.path.exists(USUARIOS_PATH):
    st.error("❌ Archivo de usuarios no encontrado.")
    st.stop()

try:
    with open(USUARIOS_PATH) as f:
        USUARIOS = json.load(f)
except Exception as e:
    st.error(f"❌ Error al leer archivo de usuarios: {e}")
    st.stop()

# --- Función para login ---
def login():
    st.sidebar.title("🔐 Ingreso de usuario")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    ingresar = st.sidebar.button("Ingresar")

    if ingresar:
        if usuario in USUARIOS and contraseña == USUARIOS[usuario]:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.rerun()
        else:
            st.sidebar.error("❌ Usuario o contraseña incorrectos")

# --- Comprobación de sesión ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    login()
    st.stop()


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
    sheet = client.open("maestra_vendedores").worksheet("colaboradores")
except Exception as e:
    st.error(f"⚠️ Error al conectar con Google Sheets: {e}")
    st.stop()


st.title("📋 Formulario de Registro de Vendedores")

with st.form("formulario_registro"):
    tz = pytz.timezone("America/Lima")
    etl_timestamp = datetime.datetime.now(tz).date()
    etl_timestamp = str(etl_timestamp)
    correo_backoffice = st.session_state["usuario"]
    nombre_colaborador_agencia = st.text_input("Nombre colaborador")
    tipo_documento = st.selectbox("Tipo documento:", ["DNI", "CE"])
    numero_documento = st.text_input("Número documento")
    correo = st.text_input("Correo electrónico")
    celular = st.text_input("Celular")
    cargo = st.selectbox("Cargo:", ["Backoffice", "Supervisor", "Vendedor"])
    ubicacion_departamento = st.text_input("Ubicación departamento")
    ubicacion_provincia	 = st.text_input("Ubicación provincia")
    ubicacion_distrito = st.text_input("Ubicación distrito")
    fecha_inicio = st.date_input("Fecha de inicio", value=datetime.date.today())
    fecha_inicio =  str(fecha_inicio)
                                 
    
    

    submitted = st.form_submit_button("Enviar")

    if submitted:
        campos = [
            nombre_colaborador_agencia,
            tipo_documento,
            numero_documento,
            correo,
            celular,
            cargo,
            ubicacion_departamento,
            ubicacion_provincia,
            ubicacion_distrito,
            fecha_inicio
        ]

        if all(campos):
            try:
                sheet.append_row([
                    etl_timestamp,
                    correo_backoffice,
                    nombre_colaborador_agencia,
                    tipo_documento,
                    numero_documento,
                    correo,
                    celular,
                    cargo,
                    ubicacion_departamento,
                    ubicacion_provincia,
                    ubicacion_distrito,
                    fecha_inicio
                ])
                st.success("✅ Datos enviados correctamente.")
            except Exception as e:
                st.error(f"❌ Error al guardar datos: {e}")
        else:
            st.warning("⚠ Por favor completa todos los campos antes de enviar.")
            

# Mostrar los datos actuales de la hoja
st.subheader("📄 Datos registrados")

try:
    # Obtiene todas las filas como lista de diccionarios
    registros = sheet.get_all_records()
    
    if registros:
        # Mostrar como DataFrame
        import pandas as pd
        df = pd.DataFrame(registros)

        # Filtrar por el correo del usuario logueado
        #correo_usuario = st.session_state["usuario"]  # debe ser un correo
        df_usuario = df[df["correo_backoffice"] == correo_backoffice]

        st.dataframe(df_usuario, use_container_width=True)
    else:
        st.info("Aún no hay registros en la hoja.")
except Exception as e:
    st.error(f"⚠️ Error al obtener datos: {e}")
