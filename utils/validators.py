import re
import requests

class Validators:
    @staticmethod
    def validar_cpf(cpf):
        """Validação completa de CPF"""
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf) != 11:
            return False
            
        # Verifica dígitos repetidos
        if cpf == cpf[0] * 11:
            return False
            
        # Cálculo dos dígitos verificadores
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if digito != int(cpf[i]):
                return False
                
        return cpf

    @staticmethod
    def buscar_cep(cep):
        """Busca CEP com tratamento de erro robusto"""
        cep_limpo = ''.join(filter(str.isdigit, cep))
        if len(cep_limpo) != 8:
            return None
            
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'erro' in data:
                return None
                
            return {
                "logradouro": data.get('logradouro', ''),
                "bairro": data.get('bairro', ''),
                "cidade": data.get('localidade', ''),
                "uf": data.get('uf', '')
            }
        except requests.exceptions.RequestException:
            return None
