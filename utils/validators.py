import re
import requests

def formatar_e_validar_cpf(cpf: str) -> str:
    """Valida e formata CPF"""
    if not cpf:
        return None
    
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf_limpo) == 11:
        return cpf_limpo
    return None

def formatar_cep(cep: str) -> str:
    """Valida e formata CEP"""
    if not cep:
        return None
    
    cep_limpo = ''.join(filter(str.isdigit, cep))
    
    if len(cep_limpo) == 8:
        return cep_limpo
    return None

def buscar_cep(cep: str) -> dict:
    """Busca endereço por CEP"""
    cep_limpo = formatar_cep(cep)
    if not cep_limpo:
        return None

    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('erro'):
            return None
        
        return {
            "logradouro": data.get('logradouro', ''),
            "bairro": data.get('bairro', ''),
            "cidade": data.get('localidade', ''),
            "uf": data.get('uf', ''),
        }
    except requests.exceptions.RequestException:
        return None
