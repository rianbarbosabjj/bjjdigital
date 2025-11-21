import streamlit as st
from config.constants import COLORS, STYLES

def render_card(title, description, button_text, on_click, key):
    """Componente de card reutilizável"""
    with st.container(border=True):
        st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; min-height: 50px;'>{description}</p>", unsafe_allow_html=True)
        st.button(button_text, key=key, on_click=on_click, use_container_width=True)

def render_address_form(prefix="", existing_data=None):
    """Formulário de endereço reutilizável"""
    existing_data = existing_data or {}
    
    col_cep, col_btn = st.columns([3, 1])
    with col_cep:
        cep = st.text_input("CEP:", value=existing_data.get('cep', ''), 
                           key=f"{prefix}_cep", max_chars=9)
    
    with col_btn:
        st.markdown("<div style='height: 29px;'></div>", unsafe_allow_html=True)
        if st.button("Buscar CEP 🔍", key=f"{prefix}_btn_cep", use_container_width=True):
            # Lógica de busca CEP
            pass
            
    col1, col2 = st.columns(2)
    with col1:
        logradouro = st.text_input("Logradouro:", value=existing_data.get('logradouro', ''),
                                  key=f"{prefix}_logradouro")
    with col2:
        bairro = st.text_input("Bairro:", value=existing_data.get('bairro', ''),
                              key=f"{prefix}_bairro")
    
    return {
        'cep': cep,
        'logradouro': logradouro,
        'bairro': bairro
    }
