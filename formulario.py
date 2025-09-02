
import streamlit as st
import pandas as pd
import datetime
import pytz
import re

from validaciones import validacion_dni

def mostrar_formulario(correo_backoffice,distribuidor_usuario, hoja_colaboradores, hoja_ubicaciones):

    ubicaciones = hoja_ubicaciones.get_all_records()
    df_ubicaciones = pd.DataFrame(ubicaciones)

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

        ubicacion_departamento = st.selectbox(
            "Ubicación departamento",
            options=df_ubicaciones["DEPARTAMENTO"].unique(),
            key="departamento"
        )
        provincias = df_ubicaciones[df_ubicaciones["DEPARTAMENTO"]==ubicacion_departamento]["PROVINCIA"].unique()

        ubicacion_provincia = st.selectbox(
            "Ubicación provincia",
            options=provincias,
            key=f"provincia_{ubicacion_departamento}" # clave dinámica para forzar refresco
        )

        fecha_inicio = str(st.date_input("Fecha de inicio", value=datetime.date.today()))
        submitted = st.form_submit_button("Enviar")

    dominios_permitidos = [
        'relevantperu.com','2connect.pe','virtualbusiness.pe','nortealto.net','forzacorp.pe','dynatech.pro',
        'sefab.net','peru-b2b.com','vortexwow.com.pe','zilicom.com','raydrs.com','programming.pe','sergap.pe',
        'myztelecom.com', 'wowempresario.com'
    ]

    if submitted:
        # --- Validación número documento ---
        if not numero_documento.isdigit() or len(numero_documento) != 8:
            st.error("❌ El número de documento debe contener solo números y 8 dígitos.")
            return None
        # --- Validación correo ---
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            st.error("❌ El correo electrónico no tiene un formato válido.")
            return None
        
        dominio = correo.split("@")[-1].lower()
        if dominio not in dominios_permitidos and cargo != "Freelance":
            st.error("❌ Solo se permiten correos corporativos.")
            return None

        # --- Validación celular ---
        if not celular.isdigit() or len(celular) != 9 or not celular.startswith("9"):
            st.error("❌ El número de celular debe tener 9 dígitos y empezar con 9.")
            return None
        
        # --- Validación DNI ---
        estado_dni = validacion_dni(hoja_colaboradores, numero_documento)
        if estado_dni == "activo":
            st.error("❌ El número de documento ya está ACTIVO, no se puede registrar.")
            return None
        if estado_dni == "observado":
            st.error("❌ El número de documento está en OBSERVACIÓN, no se puede registrar.")
            return None
        if estado_dni == "baja":
            st.warning("⚠ El número documento estuvo dado de baja recientemente")
            return None
        if estado_dni == "error":
            st.error("⚠ Error al validar el documento.")
            return None

        # --- Si pasó todas las validaciones ---

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