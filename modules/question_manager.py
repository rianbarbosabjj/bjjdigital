import json
import os
import random
from config.constants import PATHS
from modules.database import db_manager

class QuestionManager:
    def __init__(self):
        self.questions_dir = PATHS["questions_dir"]
        self.exams_dir = PATHS["exams_dir"]
        os.makedirs(self.questions_dir, exist_ok=True)
        os.makedirs(self.exams_dir, exist_ok=True)
    
    def carregar_questoes(self, tema):
        """Carrega as questões do arquivo JSON correspondente."""
        path = f"{self.questions_dir}/{tema}.json"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def salvar_questoes(self, tema, questoes):
        """Salva lista de questões no arquivo JSON."""
        with open(f"{self.questions_dir}/{tema}.json", "w", encoding="utf-8") as f:
            json.dump(questoes, f, indent=4, ensure_ascii=False)

    def carregar_todas_questoes(self):
        """Carrega todas as questões de todos os temas, adicionando o campo 'tema'."""
        todas = []
        for arquivo in os.listdir(self.questions_dir):
            if arquivo.endswith(".json"):
                tema = arquivo.replace(".json", "")
                caminho = f"{self.questions_dir}/{arquivo}"

                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        questoes = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Erro ao carregar o arquivo '{arquivo}': {e}")
                    continue

                for q in questoes:
                    q["tema"] = tema
                    todas.append(q)

        return todas

    def gerar_codigo_verificacao(self):
        """Gera código de verificação único no formato BJJDIGITAL-ANO-XXXX."""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM resultados")
        total = cursor.fetchone()[0] + 1
        conn.close()

        from datetime import datetime
        ano = datetime.now().year
        codigo = f"BJJDIGITAL-{ano}-{total:04d}"
        return codigo

# Instância global do gerenciador de questões
question_manager = QuestionManager()
