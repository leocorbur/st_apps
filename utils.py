import re
import streamlit as st

# Validadores

def validar_correo(correo: str, cargo:str, dominios_permitidos: list[str]) -> bool:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        st.error("❌ El correo electrónico no tiene un formato válido.")
        return False
    
    dominio = correo.split("@")[-1]
    if dominio not in dominios_permitidos and cargo != "Freelance":
        st.error(f"❌ El dominio '{dominio}' no está permitido.")
        return False
    
    return True