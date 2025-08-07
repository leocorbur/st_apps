
import streamlit as st
import datetime
import pytz
import re

def mostrar_formulario():
    st.title("📋 Formulario de Registro de Vendedores")

    with st.form("formulario_registro"):
        tz = pytz.timezone("America/Lima")
        etl_timestamp = str(datetime.datetime.now(tz).date())
        correo_backoffice = st.session_state["usuario"]

        nombre_colaborador_agencia = st.text_input("Nombre colaborador")
        tipo_documento = st.selectbox("Tipo documento:", ["DNI", "CE"])
        numero_documento = st.text_input("Número documento")
        correo = st.text_input("Correo electrónico")
        celular = st.text_input("Celular")
        cargo = st.selectbox("Cargo:", ["Backoffice", "Supervisor", "Vendedor"])
        ubicacion_departamento = st.text_input("Ubicación departamento")
        ubicacion_provincia = st.text_input("Ubicación provincia")
        ubicacion_distrito = st.text_input("Ubicación distrito")
        fecha_inicio = str(st.date_input("Fecha de inicio", value=datetime.date.today()))
        submitted = st.form_submit_button("Enviar")

    if submitted:
        if not numero_documento.isdigit() or len(numero_documento) != 8:
            st.error("❌ El número de documento debe contener solo números y 8 dígitos.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            st.error("❌ El correo electrónico no tiene un formato válido.")
        elif not celular.isdigit() or len(celular) != 9 or not celular.startswith("9"):
            st.error("❌ El número de celular debe tener 9 dígitos y empezar con 9.")
        else:
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
                return {
                    "etl_timestamp": etl_timestamp,
                    "correo_backoffice": correo_backoffice,
                    "nombre_colaborador_agencia": nombre_colaborador_agencia,
                    "tipo_documento": tipo_documento,
                    "numero_documento": numero_documento,
                    "correo": correo,
                    "celular": celular,
                    "cargo": cargo,
                    "ubicacion_departamento": ubicacion_departamento,
                    "ubicacion_provincia": ubicacion_provincia,
                    "ubicacion_distrito": ubicacion_distrito,
                    "fecha_inicio": fecha_inicio
                }
            else:
                st.warning("⚠ Por favor completa todos los campos antes de enviar.")

    return None