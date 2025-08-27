
import streamlit as st
import datetime
import pytz
import re

from validaciones import validacion_dni

def mostrar_formulario(correo_backoffice,distribuidor_usuario, hoja_colaboradores):
    st.title("📋 Formulario de Registro de Vendedores")

    with st.form("formulario_registro"):
        tz = pytz.timezone("America/Lima")
        etl_timestamp = str(datetime.datetime.now(tz).date())

        nombre_colaborador_agencia = st.text_input("Nombre colaborador")
        tipo_documento = st.selectbox("Tipo documento:", ["DNI", "CE"])
        numero_documento = st.text_input("Número documento")
        correo = st.text_input("Correo electrónico")
        celular = st.text_input("Celular")
        cargo = st.selectbox("Cargo:", ["Backoffice", "Supervisor", "Vendedor", "Freelance"])
        ubicacion_departamento = st.text_input("Ubicación departamento")
        ubicacion_provincia = st.text_input("Ubicación provincia")
        fecha_inicio = str(st.date_input("Fecha de inicio", value=datetime.date.today()))
        submitted = st.form_submit_button("Enviar")

    dominios_permitidos = [
        'relevantperu.com','2connect.pe','virtualbusiness.pe','nortealto.net','forzacorp.pe','dynatech.pro',
        'sefab.net','peru-b2b.com','vortexwow.com.pe','zilicom.com','raydrs.com','programming.pe','sergap.pe'
    ]

    if submitted:
        if not numero_documento.isdigit() or len(numero_documento) != 8:
            st.error("❌ El número de documento debe contener solo números y 8 dígitos.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            st.error("❌ El correo electrónico no tiene un formato válido.")
        else:
            dominio = correo.split("@")[-1].lower()
            if dominio not in dominios_permitidos:
                st.error("❌ Solo se permiten correos corporativos.")
            elif not celular.isdigit() or len(celular) != 9 or not celular.startswith("9"):
                st.error("❌ El número de celular debe tener 9 dígitos y empezar con 9.")
            else:
                validacion_dni(hoja_colaboradores, numero_documento)

                campos = [
                    nombre_colaborador_agencia,
                    tipo_documento,
                    numero_documento,
                    correo,
                    celular,
                    cargo,
                    ubicacion_departamento,
                    ubicacion_provincia,
                    fecha_inicio
                ]

                if all(campos):
                    return {
                        "etl_timestamp": etl_timestamp,
                        "correo_backoffice": correo_backoffice,
                        "distribuidor": distribuidor_usuario,
                        "nombre_colaborador_agencia": nombre_colaborador_agencia,
                        "tipo_documento": tipo_documento,
                        "numero_documento": numero_documento,
                        "correo": correo,
                        "celular": celular,
                        "cargo": cargo,
                        "ubicacion_departamento": ubicacion_departamento,
                        "ubicacion_provincia": ubicacion_provincia,
                        "fecha_inicio": fecha_inicio
                    }
                else:
                    st.warning("⚠ Por favor completa todos los campos antes de enviar.")

    return None