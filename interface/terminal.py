
from pathlib import Path
from datetime import datetime

import customtkinter as ctk
from PIL import Image


PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_FUNDO = (
    PASTA_PROJETO / "assets" / "images" / "fundo_catracas.png"
)


class TerminalAcesso(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#101214",
            corner_radius=20
        )

        self.pack_propagate(False)

        # Cabeçalho do terminal
        cabecalho = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        cabecalho.pack(fill="x", padx=20, pady=(18, 10))

        ctk.CTkLabel(
            cabecalho,
            text="FaceAccess",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(side="left")

        self.relogio = ctk.CTkLabel(
            cabecalho,
            text="",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        self.relogio.pack(side="right")

        # Imagem do ambiente empresarial
        imagem = Image.open(CAMINHO_FUNDO)

        self.fundo = ctk.CTkImage(
            light_image=imagem,
            dark_image=imagem,
            size=(380, 440)
        )

        # Área que contém o fundo e o scanner
        self.area_camera = ctk.CTkFrame(
            self,
            width=380,
            height=440,
            fg_color="#101214"
        )
        self.area_camera.pack(expand=True, padx=15, pady=10)
        self.area_camera.pack_propagate(False)

        self.imagem_fundo = ctk.CTkLabel(
            self.area_camera,
            image=self.fundo,
            text=""
        )
        self.imagem_fundo.place(x=0, y=0)

        # Linha do scanner
        self.linha_scanner = ctk.CTkFrame(
            self.area_camera,
            width=300,
            height=3,
            fg_color="#32FF80",
            corner_radius=2
        )
        self.linha_scanner.place(x=40, y=60)

        self.posicao_scanner = 60
        self.direcao_scanner = 1
        self.animar_scanner()

        # Mensagem inferior
        self.status = ctk.CTkLabel(
            self,
            text="Aguardando identificação facial...",
            font=("Arial", 15),
            text_color="#AAB2B7"
        )
        self.status.pack(pady=(5, 20))

        self.atualizar_relogio()

    def atualizar_relogio(self):
        horario = datetime.now().strftime("%H:%M:%S")
        self.relogio.configure(text=horario)
        self.after(1000, self.atualizar_relogio)

    def animar_scanner(self):
        self.posicao_scanner += 3 * self.direcao_scanner

        if self.posicao_scanner >= 380:
            self.direcao_scanner = -1

        elif self.posicao_scanner <= 60:
            self.direcao_scanner = 1

        self.linha_scanner.place(
            x=40,
            y=self.posicao_scanner
        )

        self.after(25, self.animar_scanner)