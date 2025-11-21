import streamlit as st
import pandas as pd
from modules.database import db_manager
from utils.validators import formatar_e_validar_cpf, formatar_cep, buscar_cep

class UserManager:
    def __init__(self):
        self.db_manager = db_manager
    
    def render_gestao_usuarios(self, usuario_logado):
        """Página de gerenciamento de usuários, restrita ao Admin."""
        if usuario_logado["tipo"] != "admin":
            st.error("Acesso negado. Esta página é restrita aos administradores.")
            return

        st.markdown("<h1 style='color:#FFD700;'>🔑 Gestão de Usuários</h1>", unsafe_allow_html=True)
        
        conn = self.db_manager.get_connection()
        df = pd.read_sql_query(
            "SELECT id, nome, email, cpf, tipo_usuario, auth_provider, perfil_completo FROM usuarios ORDER BY nome", 
            conn
        )

        st.subheader("Visão Geral dos Usuários")
        st.dataframe(df, use_container_width=True)
        st.markdown("---")

        st.subheader("Editar Usuário")
        lista_nomes = df["nome"].tolist()
        nome_selecionado = st.selectbox(
            "Selecione um usuário para gerenciar:",
            options=lista_nomes,
            index=None,
            placeholder="Selecione..."
        )

        if nome_selecionado:
            self.render_user_edit_form(nome_selecionado, df, conn)
        
        conn.close()

    def render_user_edit_form(self, nome_selecionado, df, conn):
        """Renderiza o formulário de edição de usuário"""
        user_id_selecionado = int(df[df["nome"] == nome_selecionado]["id"].values[0])
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id=?", (user_id_selecionado,))
        user_data = cursor.fetchone()
        
        if not user_data:
            st.error("Usuário não encontrado no banco de dados.")
            return

        with st.expander(f"Gerenciando: {user_data['nome']}", expanded=True):
            col1, col2 = st.columns(2)
            novo_nome = col1.text_input("Nome:", value=user_data['nome'])
            novo_email = col2.text_input("Email:", value=user_data['email'])
            
            novo_cpf_input = st.text_input("CPF:", value=user_data['cpf'] or "")
            
            opcoes_tipo = ["aluno", "professor", "admin"]
            tipo_atual_db = user_data['tipo_usuario']
            
            index_atual = 0 
            if tipo_atual_db:
                try:
                    index_atual = [t.lower() for t in opcoes_tipo].index(tipo_atual_db.lower())
                except ValueError:
                    index_atual = 0 
            
            novo_tipo = st.selectbox(
                "Tipo de Usuário:",
                options=opcoes_tipo,
                index=index_atual 
            )
            
            st.text_input("Provedor de Auth:", value=user_data['auth_provider'], disabled=True)
            
            if st.button("💾 Salvar Alterações", key="salvar_alteracoes", use_container_width=True):
                cpf_editado = formatar_e_validar_cpf(novo_cpf_input) if novo_cpf_input else None

                if novo_cpf_input and not cpf_editado:
                    st.error("CPF inválido na edição. Por favor, corrija o formato (11 dígitos).")
                    return
                    
                try:
                    cursor.execute(
                        "UPDATE usuarios SET nome=?, email=?, cpf=?, tipo_usuario=? WHERE id=?",
                        (novo_nome.upper(), novo_email.upper(), cpf_editado, novo_tipo, user_id_selecionado)
                    )
                    conn.commit()
                    st.success("Dados do usuário atualizados com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")

# Instância global do gerenciador de usuários
user_manager = UserManager()
