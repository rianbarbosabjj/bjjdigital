import streamlit as st
from session_manager import SessionManager
from modules.auth import AuthManager
from modules.database import DatabaseManager
from modules.ui_components import render_card, render_address_form
from config.constants import COLORS, STYLES

def main():
    # Inicialização
    SessionManager.init_session_state()
    
    # Configuração da página
    st.set_page_config(
        page_title="BJJ Digital", 
        page_icon="🥋", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS global
    st.markdown(f"<style>{STYLES['global']}</style>", unsafe_allow_html=True)
    
    # Roteamento principal
    if not SessionManager.is_authenticated():
        render_login_screen()
    else:
        render_main_application()

def render_login_screen():
    """Tela de login/cadastro"""
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    # Logo centralizada
    st.image("assets/logo.png", width=200)
    st.markdown("<h1 class='login-title'>BJJ Digital</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_registration_form()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_main_application():
    """Aplicação principal após login"""
    usuario = SessionManager.get("usuario")
    
    # Sidebar
    with st.sidebar:
        render_sidebar(usuario)
    
    # Conteúdo principal baseado na seleção
    pagina_selecionada = SessionManager.get("menu_selection", "Início")
    render_page_content(pagina_selecionada, usuario)

if __name__ == "__main__":
    main()
