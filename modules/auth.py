import bcrypt
import sqlite3
from config.constants import PATHS
from utils.validators import formatar_e_validar_cpf

class AuthManager:
    def __init__(self):
        self.db_path = PATHS["database"]
    
    def autenticar_local(self, usuario_email_ou_cpf, senha):
        """Autentica por email, nome ou CPF"""
        cpf_formatado = formatar_e_validar_cpf(usuario_email_ou_cpf)
        
        with sqlite3.connect(self.db_path) as conn:
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
            
        if user_data and bcrypt.checkpw(password.encode(), user_data[3].encode()):
            return {
                "id": user_data[0],
                "nome": user_data[1], 
                "tipo": user_data[2]
            }
        return None
    
    # ... outros métodos de autenticação
