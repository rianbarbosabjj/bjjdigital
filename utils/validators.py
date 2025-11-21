import re
import requests
from typing import Optional, Dict

def formatar_e_validar_cpf(cpf: str) -> Optional[str]:
    """Valida e formata CPF (apenas números, 11 dígitos)"""
    if not cpf:
        return None
    
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf_limpo) == 11:
        return cpf_limpo
    return None

def formatar_cep(cep: str) -> Optional[str]:
    """Valida e formata CEP (apenas números, 8 dígitos)"""
    if not cep:
        return None
    
    cep_limpo = ''.join(filter(str.isdigit, cep))
    
    if len(cep_limpo) == 8:
        return cep_limpo
    return None

def buscar_cep(cep: str) -> Optional[Dict]:
    """Busca endereço por CEP usando ViaCEP"""
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

def normalizar_nome(nome: str) -> str:
    """Remove acentos e formata o nome para uso em arquivos"""
    import unicodedata
    return "_".join(
        unicodedata.normalize("NFKD", nome)
        .encode("ASCII", "ignore")
        .decode()
        .split()
    ).lower()
