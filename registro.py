import streamlit as st
import pandas as pd
import datetime
import pytz

def mostrar_tabla(hoja_colaboradores, correo_backoffice):
    """Muestra los registros del usuario autenticado"""
    st.subheader("📄 Datos registrados")
    try:
        registros = hoja_colaboradores.get_all_records()
        if not registros:
            st.info("Aún no hay registros en la hoja.")
            return None, None

        df = pd.DataFrame(registros)
        df_usuario = df[df["correo_backoffice"] == correo_backoffice]

        st.dataframe(df_usuario, use_container_width=True)
        return df, df_usuario

    except Exception as e:
        st.error(f"⚠️ Error al obtener datos: {e}")
        return None, None



def dar_de_baja(df, df_usuario, hoja_colaboradores, correo_backoffice):
    """Permite seleccionar y dar de baja un colaborador"""
    st.markdown("---")
    st.subheader("🔻 Dar de baja a un colaborador")

    if "fecha_baja" not in df.columns or "motivo_baja" not in df.columns:
        st.warning("⚠️ Las columnas 'fecha_baja' y 'motivo_baja' no existen en la hoja.")
        return

    df_usuario_activos = df_usuario[df_usuario["fecha_baja"] == ""]
    nombres_disponibles = df_usuario_activos["nombre_colaborador_agencia"].tolist()

    if not nombres_disponibles:
        st.info("✅ Todos los colaboradores ya fueron dados de baja.")
        return

    seleccionado = st.selectbox("Selecciona al colaborador a dar de baja:", nombres_disponibles)
    motivo_baja = st.text_input("Motivo de baja")

    if st.button("Dar de baja"):
        if motivo_baja.strip() == "":
            st.warning("⚠️ Por favor ingresa un motivo.")
        else:
            index_global = df[
                (df["correo_backoffice"] == correo_backoffice) &
                (df["nombre_colaborador_agencia"] == seleccionado)
            ].index[0]

            fecha_baja = datetime.datetime.now(pytz.timezone("America/Lima")).strftime("%Y-%m-%d")

            hoja_colaboradores.update_cell(index_global + 2, df.columns.get_loc("fecha_baja") + 1, fecha_baja)
            hoja_colaboradores.update_cell(index_global + 2, df.columns.get_loc("motivo_baja") + 1, motivo_baja)

            st.success(f"✅ {seleccionado} fue dado de baja correctamente.")

