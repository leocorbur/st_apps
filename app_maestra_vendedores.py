import streamlit as st

from auth import cargar_usuarios, login
from ui_inicio import mostrar_bienvenida
from sheets import conectar_google_sheets
from formulario import mostrar_formulario
from registro import dar_de_baja, mostrar_tabla_por_rol, editar_registros, blacklist

st.set_page_config(page_title="Formulario de Registro", page_icon="📝",layout="wide")

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

hoja_ubicaciones = conectar_google_sheets("maestra_vendedores", "ubicaciones")

# Datos de sesión
correo_usuario = st.session_state["usuario"]
rol_usuario = st.session_state["rol"]
distribuidor_usuario = st.session_state["distribuidor"]



# Mostrar formulario y guardar si es válido
if rol_usuario == "backoffice":
    datos = mostrar_formulario(correo_usuario, distribuidor_usuario, hoja_colaboradores, hoja_ubicaciones)
    if datos:
        try:
            hoja_colaboradores.append_row([
                datos["etl_timestamp"],
                datos["correo_backoffice"],
                datos["distribuidor"],
                datos["nombre_colaborador_agencia"],
                datos["tipo_documento"],
                datos["numero_documento"],
                datos["correo"],
                datos["celular"],
                datos["cargo"],
                datos["ubicacion_departamento"],
                datos["ubicacion_provincia"],
                datos["fecha_inicio"]
            ])
            st.success("✅ Datos enviados correctamente.")
        except Exception as e:
            st.error(f"❌ Error al guardar datos: {e}")
            

# Mostrar los datos actuales de la hoja
df, df_usuario = mostrar_tabla_por_rol(hoja_colaboradores, correo_usuario, rol_usuario, USUARIOS)


if df is not None and df_usuario is not None:
    if rol_usuario == "backoffice":
        editar_registros(df, df_usuario, hoja_colaboradores, correo_usuario, hoja_ubicaciones)

if df is not None and df_usuario is not None:
    if rol_usuario == "backoffice":
        dar_de_baja(df, df_usuario, hoja_colaboradores, correo_usuario)

# Supervisores
if df is not None and df_usuario is not None:
    if rol_usuario == "supervisor":
        blacklist(df_usuario, hoja_colaboradores )