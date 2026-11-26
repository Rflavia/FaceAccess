"""FaceAccess - terminal facial demonstrativo. Tecla Q fecha a janela."""
from pathlib import Path
from datetime import datetime
import tempfile
import shutil
import cv2
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
FUNDO_IMAGEM = BASE / 'assets' / 'images' / 'fundo_catracas.png'
MODELO_ROSTO = BASE / 'modelos' / 'haarcascade_frontalface_default.xml'
VERDE = '#32FF80'


def cobrir(imagem, largura, altura):
    largura, altura = max(1, int(largura)), max(1, int(altura))
    escala = max(largura / imagem.width, altura / imagem.height)
    tamanho = (max(1, round(imagem.width * escala)), max(1, round(imagem.height * escala)))
    redimensionada = imagem.resize(tamanho, Image.Resampling.LANCZOS)
    x = (redimensionada.width - largura) // 2
    y = (redimensionada.height - altura) // 2
    return redimensionada.crop((x, y, x + largura, y + altura))


def fonte(tamanho, negrito=False):
    nomes = ['arialbd.ttf', 'DejaVuSans-Bold.ttf'] if negrito else ['arial.ttf', 'DejaVuSans.ttf']
    for nome in nomes:
        try:
            return ImageFont.truetype(nome, tamanho)
        except OSError:
            pass
    return ImageFont.load_default()


class TerminalAcesso(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='#000000', corner_radius=0)
        self.ativo = True
        self.camera = None
        self.detector = None
        self.segmentador = None
        self.imagem_camera = None
        self._temporario = None
        self._frame_job = None
        self._clock_job = None
        self._fundo_cache = None
        self._tamanho_cache = None
        self._ultimo_rosto = None
        self._ultimo_frame_detectado = 0
        self._quadros = 0
        self._scanner = 0.20
        self._direcao = 1
        self.nome_identificado = None
        self.resultado_acesso = None

        self.fundo_original = Image.open(FUNDO_IMAGEM).convert('RGB')
        # Remove o topo azul/escuro do arquivo de fundo.
        w, h = self.fundo_original.size
        self.fundo_original = self.fundo_original.crop((0, int(h * .20), w, h))

        lente = ctk.CTkFrame(self, height=19, fg_color='#000000', corner_radius=0)
        lente.pack(fill='x')
        lente.pack_propagate(False)
        ctk.CTkFrame(lente, width=10, height=10, corner_radius=5,
                     fg_color='#172733', border_width=1, border_color='#415665').place(
                         relx=.5, rely=.5, anchor='center')

        topo = ctk.CTkFrame(self, height=106, fg_color='#000000', corner_radius=0)
        topo.pack(fill='x')
        topo.pack_propagate(False)
        logo = Image.new('RGBA', (90, 90), (0, 0, 0, 0))
        d = ImageDraw.Draw(logo)
        cor = (245, 248, 250, 255)
        d.line([(5, 82), (85, 82)], fill=cor, width=4)
        d.line([(14, 80), (14, 29), (49, 16), (49, 80)], fill=cor, width=4)
        d.line([(49, 80), (49, 39), (76, 46), (76, 80)], fill=cor, width=4)
        for x in (24, 38):
            for y in (38, 53, 68):
                d.rectangle((x, y, x + 4, y + 6), fill=cor)
        for x in (58, 69):
            for y in (55, 69):
                d.rectangle((x, y, x + 4, y + 5), fill=cor)
        self.logo = ctk.CTkImage(light_image=logo, dark_image=logo, size=(46, 46))
        ctk.CTkLabel(topo, image=self.logo, text='').place(x=12, rely=.5, anchor='w')
        ctk.CTkLabel(topo, text='FaceAccess', font=('Arial', 24, 'bold'),
                     text_color='white').place(x=62, rely=.40, anchor='w')
        ctk.CTkLabel(topo, text='Controle de Acesso', font=('Arial', 11),
                     text_color='#D1D5DB').place(x=63, rely=.68, anchor='w')
        ctk.CTkFrame(topo, width=1, height=52, fg_color='#7E858B',
                     corner_radius=0).place(relx=.66, rely=.5, anchor='center')
        self.data = ctk.CTkLabel(topo, text='', font=('Arial', 10), text_color='white')
        self.data.place(relx=.975, rely=.34, anchor='e')
        self.relogio = ctk.CTkLabel(topo, text='', font=('Arial', 25, 'bold'), text_color='white')
        self.relogio.place(relx=.975, rely=.65, anchor='e')