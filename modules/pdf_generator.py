from fpdf import FPDF
import os
import qrcode
from config.constants import PATHS
from utils.validators import normalizar_nome

class PDFGenerator:
    def __init__(self):
        self.paths = PATHS
    
    def gerar_pdf(self, usuario, faixa, pontuacao, total, codigo, professor=None):
        """Gera certificado oficial do exame de faixa com assinatura caligráfica"""
        pdf = FPDF("L", "mm", "A4")
        pdf.set_auto_page_break(False)
        pdf.add_page()

        # Cores
        dourado, preto, branco = (218, 165, 32), (40, 40, 40), (255, 255, 255)
        percentual = int((pontuacao / total) * 100)
        from datetime import datetime
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Fundo e moldura
        pdf.set_fill_color(*branco)
        pdf.rect(0, 0, 297, 210, "F")
        pdf.set_draw_color(*dourado)
        pdf.set_line_width(2)
        pdf.rect(8, 8, 281, 194)
        pdf.set_line_width(0.8)
        pdf.rect(11, 11, 275, 188)

        # Cabeçalho
        pdf.set_text_color(*dourado)
        pdf.set_font("Helvetica", "BI", 30)
        pdf.set_y(25)
        pdf.cell(0, 10, "CERTIFICADO DE EXAME TEÓRICO DE FAIXA", align="C")
        pdf.set_draw_color(*dourado)
        pdf.line(30, 35, 268, 35)

        # Logo
        if os.path.exists(self.paths["logo"]):
            pdf.image(self.paths["logo"], x=133, y=40, w=32)

        # Conteúdo central
        pdf.set_text_color(*preto)
        pdf.set_font("Helvetica", "", 16)
        pdf.set_y(80)
        pdf.cell(0, 10, "Certificamos que o(a) aluno(a)", align="C")

        pdf.set_text_color(*dourado)
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_y(92)
        pdf.cell(0, 10, usuario.upper(), align="C")

        cores_faixa = {
            "Cinza": (169, 169, 169),
            "Amarela": (255, 215, 0),
            "Laranja": (255, 140, 0),
            "Verde": (0, 128, 0),
            "Azul": (30, 144, 255),
            "Roxa": (128, 0, 128),
            "Marrom": (139, 69, 19),
            "Preta": (0, 0, 0),
        }
        cor_faixa = cores_faixa.get(faixa, preto)

        pdf.set_text_color(*preto)
        pdf.set_font("Helvetica", "", 16)
        pdf.set_y(108)
        pdf.cell(0, 8, "concluiu o exame teórico para a faixa", align="C")

        pdf.set_text_color(*cor_faixa)
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_y(118)
        pdf.cell(0, 8, faixa.upper(), align="C")

        pdf.set_text_color(*dourado)
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_y(132)
        pdf.cell(0, 8, "APROVADO", align="C")

        pdf.set_text_color(*preto)
        pdf.set_font("Helvetica", "", 14)
        texto_final = f"obtendo {percentual}% de aproveitamento, realizado em {data_hora}."
        pdf.set_y(142)
        pdf.cell(0, 6, texto_final, align="C")

        # Selo e QR Code
        if os.path.exists(self.paths["selo"]):
            pdf.image(self.paths["selo"], x=23, y=155, w=30)

        caminho_qr = self.gerar_qrcode(codigo)
        pdf.image(caminho_qr, x=245, y=155, w=25)

        pdf.set_text_color(*preto)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_xy(220, 180)
        pdf.cell(60, 6, f"Código: {codigo}", align="R")

        # Assinatura do professor
        if professor:
            fonte_assinatura = self.paths["fonte_assinatura"]
            if os.path.exists(fonte_assinatura):
                try:
                    pdf.add_font("Assinatura", "", fonte_assinatura, uni=True)
                    pdf.set_font("Assinatura", "", 30)
                except Exception:
                    pdf.set_font("Helvetica", "I", 18)
            else:
                pdf.set_font("Helvetica", "I", 18)

            pdf.set_text_color(*preto)
            pdf.set_y(158)
            pdf.cell(0, 12, professor, align="C")

            pdf.set_draw_color(*dourado)
            pdf.line(100, 173, 197, 173)

            pdf.set_font("Helvetica", "", 10)
            pdf.set_y(175)
            pdf.cell(0, 6, "Assinatura do Professor Responsável", align="C")

        # Rodapé
        pdf.set_draw_color(*dourado)
        pdf.line(30, 190, 268, 190)
        pdf.set_text_color(*dourado)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_y(190)
        pdf.cell(0, 6, "Plataforma BJJ Digital", align="C")

        # Exportação
        os.makedirs(self.paths["reports_dir"], exist_ok=True)
        nome_
