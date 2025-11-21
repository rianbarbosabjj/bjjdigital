import streamlit as st
import os
import sys
import bcrypt
import sqlite3
from session_manager import SessionManager
from config.constants import COLORS, STYLES, PATHS
from modules.auth import auth_manager
from modules.database import db_manager
from modules.pdf_generator import pdf_generator
from modules.question_manager import question_manager
from modules.user_manager import user_manager
from modules.exam_manager import exam_manager
from modules.ui_components import render_card
from utils.validators import formatar_e_validar_cpf, formatar_cep, buscar_cep
from streamlit_option_menu import option_menu

# =========================================
# VERIFICAÇÃO DE DEPENDÊNCIAS
# =========================================

def check_dependencies():
    """Verifica se todas as dependências estão disponíveis"""
    required_packages = {
        'streamlit': '1.28.2',
        'fpdf2': '2.7.4', 
        'Pillow': '9.5.0',
        'qrcode': '7.3.1',
        'bcrypt': '3.2.0',
        'pandas': '1.5.3',
        'plotly': '5.13.1'
    }
    
    missing = []
    for package, version in required_packages.items():
        try:
            if package == 'streamlit':
                import streamlit
                if streamlit.__version__ != version:
                    st.warning(f"{package} versão {streamlit.__version__} (esperada: {version})")
            elif package == 'Pillow':
                from PIL import Image
            else:
                __import__(package)
        except ImportError:
            missing.append(f"{package}>={version}")
    
    if missing:
        st.error(f"Pacotes faltando: {', '.join(missing)}")
        st.stop()
    
    return True

# Executa a verificação
check_dependencies()

# =========================================
# VERIFICAÇÕES DE SEGURANÇA
# =========================================

# Verifica versão do Python
if sys.version_info < (3, 8):
    st.error("Python 3.8 ou superior é necessário")
    st.stop()

# Verifica se estamos no Streamlit Cloud
def is_streamlit_cloud():
    return "STREAMLIT_SHARING" in os.environ or "STREAMLIT_SERVER" in os.environ

if is_streamlit_cloud():
    st.info("🌐 Executando no Streamlit Cloud - Modo otimizado")

# =========================================
# INICIALIZAÇÃO
# =========================================

# Inicialização do estado da sessão
SessionManager.init_session_state()

# Configuração da página
st.set_page_config(
    page_title="BJJ Digital", 
    page_icon="🥋", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS global
st.markdown(STYLES["global"], unsafe_allow_html=True)

# =========================================
# FUNÇÕES PRINCIPAIS
# =========================================

def main():
    """Função principal do aplicativo"""
    # Roteamento principal
    if not SessionManager.is_authenticated():
        render_login_screen()
    else:
        render_main_application()

def render_login_screen():
    """Tela de login/cadastro"""
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    # Logo centralizada
    if os.path.exists(PATHS["logo"]):
        st.image(PATHS["logo"], width=200)
    
    st.markdown("<h1 class='login-title'>BJJ Digital</h1>", unsafe_allow_html=True)
    
    modo_login = SessionManager.get("modo_login", "login")
    
    if modo_login == "login":
        render_login_form()
    elif modo_login == "cadastro":
        render_registration_form()
    elif modo_login == "recuperar":
        render_password_recovery_form()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_login_form():
    """Formulário de login simplificado sem Google OAuth"""
    with st.form(key="form_login"):
        st.subheader("🔐 Login")
        
        usuario_email_ou_cpf = st.text_input("Nome de Usuário, Email ou CPF:")
        senha = st.text_input("Senha:", type="password")
        
        submit_login = st.form_submit_button("Entrar", use_container_width=True)
        
        if submit_login:
            if not usuario_email_ou_cpf or not senha:
                st.error("Por favor, preencha todos os campos.")
            else:
                usuario = auth_manager.autenticar_local(usuario_email_ou_cpf.strip(), senha.strip())
                if usuario:
                    SessionManager.update_user(usuario)
                    SessionManager.set("menu_selection", "Início")
                    st.success(f"Login realizado com sucesso! Bem-vindo(a), {usuario['nome'].title()}.")
                    st.rerun()
                else:
                    st.error("Usuário/Email/CPF ou senha incorretos. Tente novamente.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Criar Conta", use_container_width=True):
            SessionManager.set("modo_login", "cadastro")
            st.rerun()
    with col2:
        if st.button("🔑 Esqueci Senha", use_container_width=True):
            SessionManager.set("modo_login", "recuperar")
            st.rerun()

def render_registration_form():
    """Formulário de cadastro"""
    st.subheader("📋 Cadastro de Novo Usuário")
    
    with st.form(key="form_cadastro"):
        nome = st.text_input("Nome de Usuário (login):")
        email = st.text_input("E-mail:")
        cpf_input = st.text_input("CPF (somente números ou formato padrão):")
        senha = st.text_input("Senha:", type="password")
        confirmar = st.text_input("Confirmar senha:", type="password")
        
        tipo_usuario = st.selectbox("Tipo de Usuário:", ["Aluno", "Professor"])
        
        # Campos específicos por tipo
        if tipo_usuario == "Aluno":
            faixa = st.selectbox("Graduação (faixa):", [
                "Branca", "Cinza", "Amarela", "Laranja", "Verde",
                "Azul", "Roxa", "Marrom", "Preta"
            ])
        else:
            faixa = st.selectbox("Graduação (faixa):", ["Marrom", "Preta"])
            st.info("Professores devem ser Marrom ou Preta.")
        
        # Formulário de endereço simplificado
        st.markdown("#### 📍 Endereço")
        col_cep, col_btn = st.columns([3, 1])
        with col_cep:
            cep = st.text_input("CEP:", max_chars=9, key="cadastro_cep")
        with col_btn:
            st.markdown("<div style='height: 29px;'></div>", unsafe_allow_html=True)
            buscar_cep_clicked = st.button("Buscar CEP 🔍", key="btn_buscar_cep", use_container_width=True)
        
        col_logr, col_bairro = st.columns(2)
        with col_logr:
            logradouro = st.text_input("Logradouro:", key="cadastro_logradouro")
        with col_bairro:
            bairro = st.text_input("Bairro:", key="cadastro_bairro")
        
        col_cidade, col_uf = st.columns(2)
        with col_cidade:
            cidade = st.text_input("Cidade:", key="cadastro_cidade")
        with col_uf:
            uf = st.text_input("UF:", key="cadastro_uf")
        
        col_num, col_comp = st.columns(2)
        with col_num:
            numero = st.text_input("Número:", key="cadastro_numero")
        with col_comp:
            complemento = st.text_input("Complemento:", key="cadastro_complemento")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_cadastro = st.form_submit_button("Cadastrar", use_container_width=True)
        with col2:
            voltar_login = st.form_submit_button("⬅️ Voltar para Login", use_container_width=True)
        
        # Lógica de busca de CEP (fora do form submit principal)
        if buscar_cep_clicked and cep:
            endereco = buscar_cep(cep)
            if endereco:
                st.success("Endereço encontrado! Preencha Número e Complemento.")
                # Atualiza os campos via session state
                st.session_state.cadastro_logradouro = endereco['logradouro']
                st.session_state.cadastro_bairro = endereco['bairro']
                st.session_state.cadastro_cidade = endereco['cidade']
                st.session_state.cadastro_uf = endereco['uf']
                st.rerun()
            else:
                st.error("CEP inválido ou não encontrado.")
        
        if submit_cadastro:
            # Validações e criação do usuário
            cpf_final = formatar_e_validar_cpf(cpf_input)
            cep_final = formatar_cep(cep)
            
            if not (nome and email and cpf_input and senha and confirmar):
                st.warning("Preencha todos os campos de contato e senha obrigatórios.")
            elif senha != confirmar:
                st.error("As senhas não coincidem.")
            elif not cpf_final:
                st.error("CPF inválido. Por favor, corrija o formato (11 dígitos).")
            elif not (cep_final and logradouro and bairro and cidade and uf):
                st.error("O Endereço (CEP, Logradouro, Bairro, Cidade e UF) é obrigatório.")
            else:
                # Criação do usuário no banco
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    # Verifica se usuário já existe
                    cursor.execute("SELECT id FROM usuarios WHERE nome=? OR email=? OR cpf=?", (nome, email, cpf_final))
                    if cursor.fetchone():
                        st.error("Nome de usuário, e-mail ou CPF já cadastrado.")
                    else:
                        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
                        tipo_db = "aluno" if tipo_usuario == "Aluno" else "professor"
                        
                        cursor.execute(
                            """
                            INSERT INTO usuarios (
                                nome, email, cpf, tipo_usuario, senha, auth_provider, perfil_completo,
                                cep, logradouro, numero, complemento, bairro, cidade, uf
                            )
                            VALUES (?, ?, ?, ?, ?, 'local', 1, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                nome.upper(), email.upper(), cpf_final, tipo_db, hashed,
                                cep_final, 
                                logradouro.upper(),
                                numero.upper() if numero else None,
                                complemento.upper() if complemento else None,
                                bairro.upper(),
                                cidade.upper(),
                                uf.upper()
                            )
                        )
                        
                        novo_id = cursor.lastrowid
                        
                        # Cria vínculo na tabela apropriada
                        if tipo_db == "aluno":
                            cursor.execute(
                                """
                                INSERT INTO alunos (usuario_id, faixa_atual, status_vinculo) 
                                VALUES (?, ?, 'pendente')
                                """,
                                (novo_id, faixa)
                            )
                        else:
                            cursor.execute(
                                """
                                INSERT INTO professores (usuario_id, status_vinculo) 
                                VALUES (?, 'pendente')
                                """,
                                (novo_id,)
                            )
                        
                        conn.commit()
                        conn.close()
                        
                        st.success("Cadastro realizado! Seu vínculo está **PENDENTE**...")
                        SessionManager.set("modo_login", "login")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")
        
        if voltar_login:
            SessionManager.set("modo_login", "login")
            st.rerun()

def render_password_recovery_form():
    """Formulário de recuperação de senha"""
    st.subheader("🔑 Recuperar Senha")
    email = st.text_input("Digite o e-mail cadastrado:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enviar Instruções", use_container_width=True, type="primary"):
            st.info("Em breve será implementado o envio de recuperação de senha.")
    with col2:
        if st.button("⬅️ Voltar para Login", use_container_width=True):
            SessionManager.set("modo_login", "login")
            st.rerun()

def render_main_application():
    """Aplicação principal após login"""
    usuario = SessionManager.get("usuario")
    
    # Sidebar
    with st.sidebar:
        render_sidebar(usuario)
    
    # Conteúdo principal
    pagina_selecionada = SessionManager.get("menu_selection", "Início")
    render_page_content(pagina_selecionada, usuario)

def render_sidebar(usuario):
    """Renderiza a sidebar"""
    if os.path.exists(PATHS["logo"]):
        st.image(PATHS["logo"], use_container_width=True)
    st.markdown(f"<h3 style='color:{COLORS[\"accent\"]};'>{usuario['nome'].title()}</h3>", unsafe_allow_html=True)
    st.markdown(f"<small style='color:#ccc;'>Perfil: {usuario['tipo'].capitalize()}</small>", unsafe_allow_html=True)
    
    # Botões de navegação
    st.button("👤 Meu Perfil", on_click=lambda: SessionManager.set("menu_selection", "Meu Perfil"), use_container_width=True)
    
    if usuario["tipo"] in ["admin", "professor"]:
        st.button("👩‍🏫 Painel do Professor", on_click=lambda: SessionManager.set("menu_selection", "Painel do Professor"), use_container_width=True)
    
    if usuario["tipo"] == "admin":
        st.button("🔑 Gestão de Usuários", on_click=lambda: SessionManager.set("menu_selection", "Gestão de Usuários"), use_container_width=True)
    
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        SessionManager.clear_user_session()
        st.rerun()

def render_page_content(pagina_selecionada, usuario):
    """Renderiza o conteúdo baseado na página selecionada"""
    if pagina_selecionada in ["Meu Perfil", "Gestão de Usuários", "Painel do Professor"]:
        render_sidebar_pages(pagina_selecionada, usuario)
    else:
        render_main_pages(pagina_selecionada, usuario)

def render_sidebar_pages(pagina_selecionada, usuario):
    """Renderiza páginas da sidebar"""
    if pagina_selecionada == "Meu Perfil":
        render_tela_meu_perfil(usuario)
    elif pagina_selecionada == "Gestão de Usuários":
        user_manager.render_gestao_usuarios(usuario)
    elif pagina_selecionada == "Painel do Professor":
        render_painel_professor(usuario)
    
    # Botão de voltar
    if st.button("⬅️ Voltar ao Início", use_container_width=True):
        SessionManager.set("menu_selection", "Início")
        st.rerun()

def render_main_pages(pagina_selecionada, usuario):
    """Renderiza páginas do menu principal"""
    # Define opções do menu
    if usuario["tipo"] in ["admin", "professor"]:
        opcoes = ["Início", "Modo Rola", "Exame de Faixa", "Ranking", "Gestão de Questões", "Gestão de Equipes", "Gestão de Exame"]
        icons = ["house-fill", "people-fill", "journal-check", "trophy-fill", "cpu-fill", "building-fill", "file-earmark-check-fill"]
    else:
        opcoes = ["Início", "Modo Rola", "Ranking", "Meus Certificados"]
        icons = ["house-fill", "people-fill", "trophy-fill", "patch-check-fill"]
        
        # Adiciona Exame de Faixa se aluno estiver habilitado
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT exame_habilitado FROM alunos WHERE usuario_id=?", (usuario["id"],))
        dado = cursor.fetchone()
        conn.close()
        
        if dado and dado[0] == 1:
            opcoes.insert(2, "Exame de Faixa")
            icons.insert(2, "journal-check")
    
    # Menu horizontal
    menu_selecionado = option_menu(
        menu_title=None,
        options=opcoes,
        icons=icons,
        key="menu_horizontal",
        orientation="horizontal",
        default_index=opcoes.index(pagina_selecionada) if pagina_selecionada in opcoes else 0,
        styles={
            "container": {"padding": "0!important", "background-color": COLORS["primary"], "border-radius": "10px", "margin-bottom": "20px"},
            "icon": {"color": COLORS["accent"], "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#1a4d40", "color": COLORS["text"], "font-weight": "600"},
            "nav-link-selected": {"background-color": COLORS["secondary"], "color": COLORS["accent"]},
        }
    )
    
    # Atualiza a seleção
    SessionManager.set("menu_selection", menu_selecionado)
    
    # Renderiza a página correspondente
    if menu_selecionado == "Início":
        render_tela_inicio()
    elif menu_selecionado == "Modo Rola":
        exam_manager.render_modo_rola(usuario)
    elif menu_selecionado == "Exame de Faixa":
        exam_manager.render_exame_de_faixa(usuario)
    elif menu_selecionado == "Ranking":
        exam_manager.render_ranking()
    elif menu_selecionado == "Gestão de Questões":
        render_gestao_questoes(usuario)
    elif menu_selecionado == "Gestão de Equipes":
        render_gestao_equipes()
    elif menu_selecionado == "Gestão de Exame":
        render_gestao_exame_de_faixa()
    elif menu_selecionado == "Meus Certificados":
        render_meus_certificados(usuario)

def render_tela_inicio():
    """Tela inicial"""
    usuario = SessionManager.get("usuario")
    
    # Logo centralizada
    if os.path.exists(PATHS["logo"]):
        st.image(PATHS["logo"], width=180)
    
    st.markdown(f"<h2 style='color:{COLORS[\"accent\"]};text-align:center;'>Painel BJJ Digital</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{COLORS[\"text\"]};text-align:center;font-size:1.1em;'>Bem-vindo(a), {usuario['nome'].title()}!</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Cartões Principais
    col1, col2, col3 = st.columns(3)
    with col1:
        render_card(
            "🤼 Modo Rola",
            "Treino livre com questões aleatórias de todos os temas.",
            "Acessar",
            lambda: SessionManager.set("menu_selection", "Modo Rola"),
            "nav_rola"
        )
    with col2:
        render_card(
            "🥋 Exame de Faixa", 
            "Realize sua avaliação teórica oficial quando liberada.",
            "Acessar",
            lambda: SessionManager.set("menu_selection", "Exame de Faixa"),
            "nav_exame"
        )
    with col3:
        render_card(
            "🏆 Ranking",
            "Veja sua posição e a dos seus colegas no Modo Rola.",
            "Acessar", 
            lambda: SessionManager.set("menu_selection", "Ranking"),
            "nav_ranking"
        )

    # Cartões de Gestão (Admin/Professor)
if SessionManager.get_user_type() in ["admin", "professor"]:
    st.markdown("---")
    st.markdown(f"<h2 style='color:{COLORS[\"accent\"]};text-align:center; margin-top:30px;'>Painel de Gestão</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        render_card(
            "🧠 Gestão de Questões",
            "Adicione, edite ou remova questões dos temas.",
            "Gerenciar",
            lambda: SessionManager.set("menu_selection", "Gestão de Questões"),
            "nav_gest_questoes"
        )
    with c2:
        render_card(
            "🏛️ Gestão de Equipes",
            "Gerencie equipes, professores e alunos vinculados.",
            "Gerenciar",
            lambda: SessionManager.set("menu_selection", "Gestão de Equipes"),
            "nav_gest_equipes"
        )
    with c3:
        render_card(
            "📜 Gestão de Exame", 
            "Monte as provas oficiais selecionando questões.",
            "Gerenciar",
            lambda: SessionManager.set("menu_selection", "Gestão de Exame"),
            "nav_gest_exame"
        )
# =========================================
# FUNÇÕES DE PÁGINAS (PLACEHOLDERS)
# =========================================

def render_tela_meu_perfil(usuario):
    """Tela Meu Perfil - placeholder"""
    st.markdown("<h1 style='color:#FFD700;'>👤 Meu Perfil</h1>", unsafe_allow_html=True)
    st.info("Funcionalidade em desenvolvimento...")
    st.write(f"Usuário: {usuario['nome']}")
    st.write(f"Tipo: {usuario['tipo']}")
    st.write(f"ID: {usuario['id']}")

def render_painel_professor(usuario):
    """Painel do Professor - placeholder"""
    st.markdown("<h1 style='color:#FFD700;'>👩‍🏫 Painel do Professor</h1>", unsafe_allow_html=True)
    st.info("Funcionalidade em desenvolvimento...")

def render_gestao_questoes(usuario):
    """Gestão de Questões - placeholder"""
    st.markdown("<h1 style='color:#FFD700;'>🧠 Gestão de Questões</h1>", unsafe_allow_html=True)
    st.info("Funcionalidade em desenvolvimento...")

def render_gestao_equipes():
    """Gestão de Equipes - placeholder"""
    st.markdown("<h1 style='color:#FFD700;'>🏛️ Gestão de Equipes</h1>", unsafe_allow_html=True)
    st.info("Funcionalidade em desenvolvimento...")

def render_gestao_exame_de_faixa():
    """Gestão de Exame - placeholder"""
    st.markdown("<h1 style='color:#FFD700;'>📜 Gestão de Exame</h1>", unsafe_allow_html=True)
    st.info("Funcionalidade em desenvolvimento...")

def render_meus_certificados(usuario):
    """Meus Certificados - placeholder"""
    st.markdown("<h1 style='color:#FFD700;'>📜 Meus Certificados</h1>", unsafe_allow_html=True)
    st.info("Funcionalidade em desenvolvimento...")

# =========================================
# EXECUÇÃO PRINCIPAL
# =========================================

if __name__ == "__main__":
    # Cria usuários de teste se necessário
    if not os.path.exists(PATHS["database"]):
        db_manager.criar_usuarios_teste()
        st.success("Banco de dados e usuários de teste criados com sucesso!")
    
    main()
