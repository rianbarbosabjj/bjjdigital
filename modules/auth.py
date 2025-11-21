class AuthManager:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def authenticate(self, identifier, password):
        """Autentica por email, nome ou CPF"""
        cpf_formatted = self.format_cpf(identifier)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Busca flexível por múltiplos campos
            if cpf_formatted:
                cursor.execute("""
                    SELECT id, nome, tipo_usuario, senha 
                    FROM usuarios 
                    WHERE (email=? OR nome=? OR cpf=?) AND auth_provider='local'
                """, (identifier, identifier, cpf_formatted))
            else:
                cursor.execute("""
                    SELECT id, nome, tipo_usuario, senha 
                    FROM usuarios 
                    WHERE (email=? OR nome=?) AND auth_provider='local'
                """, (identifier, identifier))
                
            user_data = cursor.fetchone()
            
        if user_data and bcrypt.checkpw(password.encode(), user_data[3].encode()):
            return {
                "id": user_data[0],
                "nome": user_data[1], 
                "tipo": user_data[2]
            }
        return None
