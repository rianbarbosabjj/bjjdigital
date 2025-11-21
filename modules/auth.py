import bcrypt
import sqlite3
from config.constants import PATHS
from utils.validators import formatar_e_validar_cpf
from modules.database import db_manager

class AuthManager:
    def __init__(self):
        self.db_path = PATHS["database"]
    
    def autenticar_local(self, usuario_email_ou_cpf, senha):
        """Autentica por email, nome ou CPF"""
        cpf_formatado = formatar_e_validar_cpf(usuario_email_ou_cpf)
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        if cpf_formatado:
            cursor.execute("""
                SELECT id, nome, tipo_usuario, senha 
                FROM usuarios 
                WHERE (email=? OR nome=? OR cpf=?) AND auth_provider='local'
            """, (usuario_email_ou_cpf, usuario_email_ou_cpf, cpf_formatado))
        else:
            cursor.execute("""
                SELECT id, nome, tipo_usuario, senha 
                FROM usuarios 
                WHERE (email=? OR nome=?) AND auth_provider='local'
            """, (usuario_email_ou_cpf, usuario_email_ou_cpf))
            
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and bcrypt.checkpw(senha.encode(), user_data[3].encode()):
            return {
                "id": user_data[0],
                "nome": user_data[1], 
                "tipo": user_data[2]
            }
        return None
    
    def buscar_usuario_por_email(self, email_ou_cpf):
        """Busca um usuário pelo email ou CPF (principalmente para Auth Social)"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cpf_formatado = formatar_e_validar_cpf(email_ou_cpf)

        if cpf_formatado:
            cursor.execute(
                "SELECT id, nome, tipo_usuario, perfil_completo FROM usuarios WHERE email=? OR cpf=?", 
                (email_ou_cpf, cpf_formatado)
            )
        else:
            cursor.execute(
                "SELECT id, nome, tipo_usuario, perfil_completo FROM usuarios WHERE email=?", 
                (email_ou_cpf,)
            )
            
        dados = cursor.fetchone()
        conn.close()
        
        if dados:
            return {
                "id": dados[0], 
                "nome": dados[1], 
                "tipo": dados[2], 
                "perfil_completo": bool(dados[3])
            }
            
        return None

    def criar_usuario_parcial_google(self, email, nome):
        """Cria um registro inicial para um novo usuário do Google"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios (email, nome, auth_provider, perfil_completo)
                VALUES (?, ?, 'google', 0)
                """, (email, nome)
            )
            conn.commit()
            novo_id = cursor.lastrowid
            conn.close()
            return {"id": novo_id, "email": email, "nome": nome}
        except sqlite3.IntegrityError:
            conn.close()
            return None

# Instância global do gerenciador de autenticação
auth_manager = AuthManager()
