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
        datos_usuario = usuarios.get(usuario)
        if datos_usuario and datos_usuario.get("password") == contraseña:
            if datos_usuario.get("estado") == "activo":
                st.session_state["autenticado"] = True
                st.session_state["usuario"] = usuario
                st.session_state["rol"] = datos_usuario.get("rol")
                st.session_state["distribuidor"] = datos_usuario.get("distribuidor", "")
                st.session_state["supervisor"] = datos_usuario.get("supervisor", "")
                st.success("✅ Ingreso exitoso")
                st.rerun()
            else:
                st.sidebar.error("❌ Usuario o contraseña incorrectos")
        else:
            st.sidebar.error("❌ Usuario o contraseña incorrectos")