# session_manager.py
import streamlit as st
from typing import Any, Dict, Optional

class SessionManager:
    """Gerenciador centralizado do estado da sessão"""
    
    # Estados padrão da aplicação
    DEFAULT_STATES = {
        "usuario": None,
        "menu_selection": "Início",
        "modo_login": "login", 
        "token": None,
        "registration_pending": None,
        "endereco_cep": {},
        "endereco_cep_cadastro": {},
        "certificado_pronto": False,
        "dados_certificado": None
    }
    
    @classmethod
    def init_session_state(cls):
        """Inicializa todos os estados da sessão com valores padrão"""
        for key, default_value in cls.DEFAULT_STATES.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Recupera um valor do estado da sessão"""
        return st.session_state.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any):
        """Define um valor no estado da sessão"""
        st.session_state[key] = value
    
    @classmethod
    def update_user(cls, user_data: Dict):
        """Atualiza os dados do usuário logado"""
        st.session_state.usuario = user_data
    
    @classmethod
    def clear_user_session(cls):
        """Limpa apenas os dados da sessão do usuário (mantém configurações)"""
        user_specific_keys = [
            "usuario", "menu_selection", "token", "registration_pending",
            "certificado_pronto", "dados_certificado"
        ]
        
        for key in user_specific_keys:
            if key in st.session_state:
                del st.session_state[key]
        
        # Restaura valores padrão
        cls.set("menu_selection", "Início")
        cls.set("modo_login", "login")
        cls.set("usuario", None)
    
    @classmethod
    def clear_all(cls):
        """Limpa completamente a sessão (uso cuidadoso)"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @classmethod
    def is_authenticated(cls) -> bool:
        """Verifica se há um usuário autenticado"""
        return cls.get("usuario") is not None
    
    @classmethod
    def get_user_id(cls) -> Optional[int]:
        """Retorna o ID do usuário logado"""
        return cls.get("usuario", {}).get("id") if cls.is_authenticated() else None
    
    @classmethod
    def get_user_type(cls) -> Optional[str]:
        """Retorna o tipo do usuário logado"""
        return cls.get("usuario", {}).get("tipo") if cls.is_authenticated() else None
    
    @classmethod
    def setup_address_state(cls, prefix: str, initial_data: Dict = None):
        """Configura o estado para formulários de endereço"""
        initial_data = initial_data or {}
        address_key = f"{prefix}_address_data"
        
        if address_key not in st.session_state:
            st.session_state[address_key] = {
                'cep': initial_data.get('cep', ''),
                'logradouro': initial_data.get('logradouro', ''),
                'bairro': initial_data.get('bairro', ''),
                'cidade': initial_data.get('cidade', ''),
                'uf': initial_data.get('uf', '')
            }
        
        # Sincroniza widgets individuais
        for field in ['logradouro', 'bairro', 'cidade', 'uf']:
            widget_key = f"{prefix}_{field}"
            if widget_key not in st.session_state:
                st.session_state[widget_key] = st.session_state[address_key][field]
    
    @classmethod
    def get_address_data(cls, prefix: str) -> Dict:
        """Recupera dados de endereço formatados"""
        address_key = f"{prefix}_address_data"
        return st.session_state.get(address_key, {})
