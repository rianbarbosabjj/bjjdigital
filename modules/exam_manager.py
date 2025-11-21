import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import db_manager
from modules.question_manager import question_manager
from modules.pdf_generator import pdf_generator

class ExamManager:
    def __init__(self):
        self.db_manager = db_manager
        self.question_manager = question_manager
        self.pdf_generator = pdf_generator
    
    def render_modo_rola(self, usuario_logado):
        """Renderiza o modo Rola"""
        st.markdown("<h1 style='color:#FFD700;'>🤼 Modo Rola - Treino Livre</h1>", unsafe_allow_html=True)

        temas = [f.replace(".json", "") for f in os.listdir("questions") if f.endswith(".json")]
        temas.append("Todos os Temas")

        col1, col2 = st.columns(2)
        with col1:
            tema = st.selectbox("Selecione o tema:", temas)
        with col2:
            faixa = st.selectbox("Sua faixa:", ["Branca", "Cinza", "Amarela", "Laranja", "Verde", "Azul", "Roxa", "Marrom", "Preta"])

        if st.button("Iniciar Treino 🤼", use_container_width=True):
            # Implementação do modo Rola (similar à original)
            pass

    def render_exame_de_faixa(self, usuario_logado):
        """Renderiza o exame de faixa"""
        st.markdown("<h1 style='color:#FFD700;'>🥋 Exame de Faixa</h1>", unsafe_allow_html=True)
        
        # Verifica se o aluno foi liberado para o exame
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT exame_habilitado FROM alunos WHERE usuario_id=?", (usuario_logado["id"],))
        dado = cursor.fetchone()
        conn.close()

        # Restante da implementação do exame
        pass

    def render_ranking(self):
        """Renderiza o ranking"""
        st.markdown("<h1 style='color:#FFD700;'>🏆 Ranking do Modo Rola</h1>", unsafe_allow_html=True)
        
        conn = self.db_manager.get_connection()
        df = pd.read_sql_query("SELECT * FROM rola_resultados", conn)
        conn.close()

        # Restante da implementação do ranking
        pass

# Instância global do gerenciador de exames
exam_manager = ExamManager()
