import streamlit as st
import datetime
import pytz

from auth import cargar_usuarios, login
from ui_inicio import mostrar_bienvenida
from sheets import conectar_google_sheets
from formulario import mostrar_formulario

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


# Mostrar formulario y guardar si es válido
datos = mostrar_formulario()
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
st.subheader("📄 Datos registrados")

try:
    # Obtiene todas las filas como lista de diccionarios
    registros = hoja_colaboradores.get_all_records()
    
    if registros:
        # Mostrar como DataFrame
        import pandas as pd
        df = pd.DataFrame(registros)

        # Filtrar por el correo del usuario logueado
        correo_backoffice = st.session_state["usuario"]  # debe ser un correo
        df_usuario = df[df["correo_backoffice"] == correo_backoffice]

        st.dataframe(df_usuario, use_container_width=True)

        st.markdown("---")
        st.subheader("🔻 Dar de baja a un colaborador")

        # Seleccion por nombre
        df_usuario_activos = df_usuario[df_usuario["fecha_baja"] == ""]
        nombres_disponibles = df_usuario_activos["nombre_colaborador_agencia"].tolist()
        seleccionado = st.selectbox("Selecciona al colaborador a dar de baja:", nombres_disponibles)

        motivo_baja = st.text_input("Motivo de baja")
        if st.button("Dar de baja"):
            if motivo_baja.strip() == "":
                st.warning("⚠️ Por favor ingresa un motivo.")
            else:
                index_global = df[(df["correo_backoffice"] == correo_backoffice) &
                    (df["nombre_colaborador_agencia"] == seleccionado)].index[0]
                
                tz = pytz.timezone("America/Lima")
                fecha_baja = datetime.datetime.now(tz).strftime("%Y-%m-%d")

                # Actualizar columnas en la hoja (sumar 2 porque .get_all_records() ignora encabezado)
                hoja_colaboradores.update_cell(index_global + 2, df.columns.get_loc("fecha_baja") + 1, fecha_baja)
                hoja_colaboradores.update_cell(index_global + 2, df.columns.get_loc("motivo_baja") + 1, motivo_baja)

                st.success(f"✅ {seleccionado} fue dado de baja correctamente.")
                
    else:
        st.info("Aún no hay registros en la hoja.")
except Exception as e:
    st.error(f"⚠️ Error al obtener datos: {e}")
