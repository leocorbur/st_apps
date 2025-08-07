import streamlit as st

from auth import cargar_usuarios, login
from ui_inicio import mostrar_bienvenida
from sheets import conectar_google_sheets
from formulario import mostrar_formulario
from registro import mostrar_tabla, dar_de_baja

st.set_page_config(page_title="Formulario de Registro", page_icon="📝")

USUARIOS = cargar_usuarios()


# --- Comprobación de sesión ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    mostrar_bienvenida()
    login(USUARIOS)
    st.stop()


# Conectar y obtener la hoja
hoja_colaboradores = conectar_google_sheets("maestra_vendedores", "colaboradores")

correo_backoffice = st.session_state["usuario"]

# Mostrar formulario y guardar si es válido
datos = mostrar_formulario(correo_backoffice)
if datos:
    try:
        hoja_colaboradores.append_row([
            datos["etl_timestamp"],
            datos["correo_backoffice"],
            datos["nombre_colaborador_agencia"],
            datos["tipo_documento"],
            datos["numero_documento"],
            datos["correo"],
            datos["celular"],
            datos["cargo"],
            datos["ubicacion_departamento"],
            datos["ubicacion_provincia"],
            datos["ubicacion_distrito"],
            datos["fecha_inicio"]
        ])
        st.success("✅ Datos enviados correctamente.")
    except Exception as e:
        st.error(f"❌ Error al guardar datos: {e}")
            

# Mostrar los datos actuales de la hoja
df, df_usuario = mostrar_tabla(hoja_colaboradores, correo_backoffice)

if df is not None and df_usuario is not None:
    dar_de_baja(df, df_usuario, hoja_colaboradores, correo_backoffice)
