import bcrypt
from modules.database import db_manager
from utils.validators import formatar_e_validar_cpf, formatar_cep
import streamlit as st # Necessário para o st.error/success se for chamado aqui

class RegistrationManager:
    """Gerencia a lógica de negócio para criação e vínculo de novos usuários."""
    
    def criar_novo_usuario_e_vinculo(self, dados_form):
        """
        Recebe os dados do formulário e realiza as validações e inserts no DB.
        Retorna (sucesso, mensagem)
        """
        nome = dados_form['nome']
        email = dados_form['email']
        cpf_input = dados_form['cpf_input']
        senha = dados_form['senha']
        confirmar = dados_form['confirmar']
        tipo_usuario = dados_form['tipo_usuario']
        faixa = dados_form['faixa']
        
        # Dados de endereço
        cep = dados_form['cep']
        logradouro = dados_form['logradouro']
        bairro = dados_form['bairro']
        cidade = dados_form['cidade']
        uf = dados_form['uf']
        numero = dados_form['numero']
        complemento = dados_form['complemento']
        
        # 1. VALIDAÇÕES BÁSICAS
        if senha != confirmar:
            return False, "As senhas não coincidem."
        
        cpf_final = formatar_e_validar_cpf(cpf_input)
        if not cpf_final:
            return False, "CPF inválido. Por favor, corrija o formato (11 dígitos)."
            
        cep_final = formatar_cep(cep)
        if not (cep_final and logradouro and bairro and cidade and uf):
            return False, "O Endereço (CEP, Logradouro, Bairro, Cidade e UF) é obrigatório."
            
        # 2. INSERÇÃO NO BANCO DE DADOS
        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            
            # Verifica se usuário já existe
            cursor.execute("SELECT id FROM usuarios WHERE nome=? OR email=? OR cpf=?", (nome.upper(), email.upper(), cpf_final))
            if cursor.fetchone():
                conn.close()
                return False, "Nome de usuário, e-mail ou CPF já cadastrado."
            
            # Cria o hash da senha
            hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
            tipo_db = "aluno" if tipo_usuario == "Aluno" else "professor"
            
            # INSERT na tabela 'usuarios'
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
            
            # Cria vínculo na tabela 'alunos' ou 'professores'
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
            
            return True, "Cadastro realizado! Seu vínculo está **PENDENTE** de aprovação."
            
        except Exception as e:
            # Em um sistema real, você registraria este erro em logs
            return False, f"Erro interno ao cadastrar: {e}"

# Instância global do gerenciador de registro
registration_manager = RegistrationManager()
