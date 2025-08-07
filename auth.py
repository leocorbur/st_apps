import json
import os
import streamlit as st

USUARIOS_PATH = "/etc/secrets/USUARIOS_CONTRASENAS"

def cargar_usuarios():
    """Carga el archivo de usuarios y contraseñas desde el path secreto"""
    if not os.path.exists(USUARIOS_PATH):
        st.error("❌ Archivo de usuarios no encontrado.")
        st.stop()

    try:
        with open(USUARIOS_PATH) as f:
            usuarios = json.load(f)
        return usuarios
    except Exception as e:
        st.error(f"❌ Error al leer archivo de usuarios: {e}")
        st.stop()

def login(usuarios: dict):
    """Muestra el formulario de login y autentica al usuario"""
    st.sidebar.title("🔐 Ingreso de usuario")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    ingresar = st.sidebar.button("Ingresar")

    if ingresar:
        if usuario in usuarios and contraseña == usuarios[usuario]:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.rerun()
        else:
            st.sidebar.error("❌ Usuario o contraseña incorrectos")