
import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("dark")

FUNDO = "#101214"
PAINEL = "#1B1F22"
VERDE = "#31C76A"
VERMELHO = "#EF5350"

app = ctk.CTk()
app.title("FaceAccess | Controle de Acesso")
app.geometry("1000x760")
app.minsize(780, 650)
app.configure(fg_color=FUNDO)

# Cabeçalho
cabecalho = ctk.CTkFrame(app, fg_color="transparent")
cabecalho.pack(fill="x", padx=45, pady=(30, 20))

marca = ctk.CTkFrame(cabecalho, fg_color="transparent")
marca.pack(side="left")

ctk.CTkLabel(
    marca, text="▥  FaceAccess",
    font=("Arial", 30, "bold"),
    text_color="white"
).pack(anchor="w")

ctk.CTkLabel(
    marca, text="CONTROLE DE ACESSO",
    font=("Arial", 12),
    text_color="#929A9F"
).pack(anchor="w")

relogio = ctk.CTkLabel(
    cabecalho, text="",
    font=("Arial", 32, "bold"),
    text_color="white"
)
relogio.pack(side="right")


def atualizar_relogio():
    relogio.configure(text=datetime.now().strftime("%H:%M:%S"))
    app.after(1000, atualizar_relogio)


# Área principal: receberá a webcam futuramente
camera = ctk.CTkFrame(
    app, fg_color=PAINEL,
    corner_radius=22,
    border_width=1,
    border_color="#343A3F"
)
camera.pack(fill="both", expand=True, padx=45, pady=10)

ctk.CTkLabel(
    camera, text="⌗",
    font=("Arial", 100),
    text_color="#657078"
).pack(expand=True, pady=(35, 0))

ctk.CTkLabel(
    camera, text="ÁREA DE IDENTIFICAÇÃO FACIAL",
    font=("Arial", 16, "bold"),
    text_color="#D8DDE0"
).pack(pady=(0, 8))

ctk.CTkLabel(
    camera, text="Câmera indisponível neste computador",
    font=("Arial", 13),
    text_color="#8E999F"
).pack(pady=(0, 35))


# Painel de resultado
resultado = ctk.CTkFrame(
    app, fg_color=PAINEL,
    corner_radius=18, height=105
)
resultado.pack(fill="x", padx=45, pady=(12, 15))
resultado.pack_propagate(False)

titulo_status = ctk.CTkLabel(
    resultado, text="Aguardando identificação",
    font=("Arial", 23, "bold"),
    text_color="white"
)
titulo_status.pack(pady=(20, 4))

detalhe_status = ctk.CTkLabel(
    resultado, text="Aproxime seu rosto do terminal",
    font=("Arial", 14),
    text_color="#A0A8AD"
)
detalhe_status.pack()


def alterar_status(autorizado):
    if autorizado:
        titulo_status.configure(
            text="✓  Acesso autorizado",
            text_color=VERDE
        )
        detalhe_status.configure(text="Bem-vinda, Flávia")
        resultado.configure(border_width=1, border_color=VERDE)
    else:
        titulo_status.configure(
            text="✕  Acesso negado",
            text_color=VERMELHO
        )
        detalhe_status.configure(text="Usuário não autorizado")
        resultado.configure(border_width=1, border_color=VERMELHO)

    app.after(4000, restaurar_status)


def restaurar_status():
    titulo_status.configure(
        text="Aguardando identificação",
        text_color="white"
    )
    detalhe_status.configure(
        text="Aproxime seu rosto do terminal"
    )
    resultado.configure(border_width=0)


# Botões exclusivos do modo de demonstração
testes = ctk.CTkFrame(app, fg_color="transparent")
testes.pack(pady=(0, 12))

ctk.CTkButton(
    testes, text="Simular autorizado",
    fg_color="#176C3B",
    hover_color="#21864C",
    command=lambda: alterar_status(True)
).pack(side="left", padx=8)

ctk.CTkButton(
    testes, text="Simular negado",
    fg_color="#843030",
    hover_color="#A63A3A",
    command=lambda: alterar_status(False)
).pack(side="left", padx=8)

ctk.CTkLabel(
    app, text="FACEACCESS  •  MODO DE DEMONSTRAÇÃO",
    font=("Arial", 11),
    text_color="#717B80"
).pack(pady=(0, 15))

atualizar_relogio()
app.mainloop()
