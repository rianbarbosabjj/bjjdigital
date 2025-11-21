import streamlit as st
from typing import Any, Dict, Optional

class SessionManager:
    """Gerenciador centralizado do estado da sessão"""
    
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
        """Limpa apenas os dados da sessão do usuário"""
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
