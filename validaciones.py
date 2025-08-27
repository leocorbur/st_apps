import streamlit as st
import pandas as pd
import datetime
import pytz



def validacion_dni(hoja_colaboradores, numero_documento):

    registros = hoja_colaboradores.get_all_records()
    df = pd.DataFrame(registros)

    tz = pytz.timezone("America/Lima")
    hoy = datetime.datetime.now(tz).date()

    # Filtrar por DNI
    registros = df[df["numero_documento"] == numero_documento]

    if registros.empty:
        return  # no existe en la base

    # Ordenar por timestamp (más reciente primero)
    registros = registros.sort_values("etl_timestamp", ascending=False)

    # Tomar el último registro válido
    registro = registros.iloc[0]

    # Caso 1: activo
    if registro["fecha_baja"] == "" and registro["blacklist"] == "":
        st.warning("El número de documento está activo")

    # Caso 2: en blacklist
    elif registro["blacklist"] != "":
        st.warning("El número de documento está observado")

    # Caso 3: baja reciente (≤ 2 meses)
    elif registro["fecha_baja"] != "" and registro["blacklist"] == "":
        try:
            fecha_baja = pd.to_datetime(registro["fecha_baja"]).date()
            diferencia_meses = (hoy.year - fecha_baja.year) * 12 + (hoy.month - fecha_baja.month)
            if diferencia_meses <= 2:
                st.warning("El número de documento está de baja (reciente)")
        except Exception as e:
            st.error(f"Error al interpretar fecha_baja: {e}")

