import streamlit as st
from modules.auth import AuthManager
from modules.ui_components import render_card, render_address_form
from utils.validators import Validators
from config.constants import COLORS
from session_state import SessionState

def main():
    # Inicialização
    SessionState.init_defaults()
    
    # Configuração da página
    st.set_page_config(page_title="BJJ Digital", page_icon="🥋", layout="wide")
    
    # CSS global
    st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)
    
    # Roteamento principal
    if not st.session_state.usuario:
        render_login_screen()
    else:
        render_main_application()

def render_login_screen():
    """Tela de login/cadastro simplificada"""
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_registration_form()

def render_main_application():
    """Aplicação principal após login"""
    usuario = st.session_state.usuario
    
    # Sidebar
    with st.sidebar:
        render_sidebar(usuario)
    
    # Conteúdo principal
    render_main_content(usuario)

if __name__ == "__main__":
    main()
