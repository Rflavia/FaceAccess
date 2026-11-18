
import sqlite3
from datetime import datetime
from tkinter import messagebox
from pathlib import Path
from tkinter import filedialog
from uuid import uuid4
from PIL import Image

import customtkinter as ctk

from banco.database import conectar, criar_banco
from banco.historico import consultar_historico


ctk.set_appearance_mode("dark")

FUNDO = "#0C1013"
LATERAL = "#141B1F"
PAINEL = "#1D2529"
ITEM = "#26343A"
VERDE = "#258A50"
VERDE_CLARO = "#31C76A"
VERMELHO = "#EF5350"
TEXTO_SECUNDARIO = "#A8B6BD"

class PainelAdmin(ctk.CTk):

    def __init__(self):
        super().__init__()

        criar_banco()

        self.title("FaceAccess | Administração")
        self.geometry("1100x720")
        self.minsize(850, 580)
        self.configure(fg_color=FUNDO)

        self.menu_botoes = {}

        # Menu lateral
        self.lateral = ctk.CTkFrame(
            self, width=230, fg_color=LATERAL,
            corner_radius=0
        )
        self.lateral.pack(side="left", fill="y")
        self.lateral.pack_propagate(False)

        ctk.CTkLabel(
            self.lateral,
            text="◉  FaceAccess",
            font=("Arial", 23, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=20, pady=(30, 5))

        ctk.CTkLabel(
            self.lateral,
            text="PAINEL ADMINISTRATIVO",
            font=("Arial", 10),
            text_color=TEXTO_SECUNDARIO
        ).pack(anchor="w", padx=22, pady=(0, 35))

        for nome, icone in [
            ("Início", "⌂"),
            ("Cadastrar pessoa", "+"),
            ("Pessoas", "♙"),
            ("Histórico", "◷")
        ]:
            botao = ctk.CTkButton(
                self.lateral,
                text=f"{icone}   {nome}",
                anchor="w",
                height=45,
                fg_color="transparent",
                hover_color=ITEM,
                text_color="#DCE1E3",
                font=("Arial", 13),
                command=lambda pagina=nome: 
                
            self.mostrar_pagina(pagina)
            )
            botao.pack(fill="x", padx=12, pady=4)
            self.menu_botoes[nome] = botao

        ctk.CTkLabel(
            self.lateral,
            text="Controle de acesso ao prédio",
            font=("Arial", 10),
            text_color=TEXTO_SECUNDARIO
        ).pack(side="bottom", pady=25)

        # Área central
        self.conteudo = ctk.CTkFrame(
            self,
            fg_color=FUNDO,
            corner_radius=0
        )
        self.conteudo.pack(
            side="left",
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        self.mostrar_pagina("Início")

    def limpar_conteudo(self):
        for widget in self.conteudo.winfo_children():
            widget.destroy()

    def titulo(self, titulo, subtitulo):
        ctk.CTkLabel(
            self.conteudo,
            text=titulo,
            font=("Arial", 27, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(5, 5))

        ctk.CTkLabel(
            self.conteudo,
            text=subtitulo,
            text_color=TEXTO_SECUNDARIO
        ).pack(anchor="w", pady=(0, 25))

    def mostrar_pagina(self, pagina):
        self.limpar_conteudo()

        for nome, botao in self.menu_botoes.items():
            botao.configure(
                fg_color="#174D35" if nome == pagina else "transparent",
                text_color="white" if nome == pagina else "#DCE1E3"
            )

        if pagina == "Início":
            self.pagina_inicio()
        elif pagina == "Cadastrar pessoa":
            self.pagina_cadastro()
        elif pagina == "Pessoas":
            self.pagina_pessoas()
        elif pagina == "Histórico":
            self.pagina_historico()

    
    def criar_cartao(self, pai, titulo, valor, icone, cor):
        cartao = ctk.CTkFrame(
            pai,
            fg_color=PAINEL,
            corner_radius=15,
            border_width=1,
            border_color="#303D42"
        )
        cartao.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        ctk.CTkLabel(
            cartao,
            text=icone,
            font=("Arial", 25),
            text_color=cor
        ).pack(anchor="w", padx=20, pady=(17, 5))

        ctk.CTkLabel(
            cartao,
            text=str(valor),
            font=("Arial", 34, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=20)

        ctk.CTkLabel(
            cartao,
            text=titulo,
            font=("Arial", 12),
            text_color=TEXTO_SECUNDARIO
        ).pack(anchor="w", padx=20, pady=(2, 18))

    
    def pagina_inicio(self):
        self.titulo(
            "Visão geral",
            "Acompanhe os cadastros e acessos do FaceAccess."
        )

        with conectar() as conexao:
            total = conexao.execute(
                "SELECT COUNT(*) FROM pessoas"
            ).fetchone()[0]

            autorizados = conexao.execute(
                "SELECT COUNT(*) FROM pessoas WHERE autorizado = 1"
            ).fetchone()[0]

            acessos = conexao.execute(
                "SELECT COUNT(*) FROM registros_acesso"
            ).fetchone()[0]

        # Indicadores
        indicadores = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )
        indicadores.pack(fill="x", pady=(0, 25))

        self.criar_cartao(
            indicadores, "Pessoas cadastradas",
            total, "♙", "#DCE5E9"
        )

        self.criar_cartao(
            indicadores, "Pessoas autorizadas",
            autorizados, "✓", VERDE_CLARO
        )

        self.criar_cartao(
            indicadores, "Registros de acesso",
            acessos, "◷", "#67C5DF"
        )

        # Acesso rápido
        ctk.CTkLabel(
            self.conteudo,
            text="Acesso rápido",
            font=("Arial", 19, "bold"),
            text_color="white"
        ).pack(anchor="w", pady=(0, 12))

        atalhos = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )
        atalhos.pack(fill="x", pady=(0, 25))

        for nome, icone in [
            ("Cadastrar pessoa", "+"),
            ("Pessoas", "♙"),
            ("Histórico", "◷")
        ]:
            ctk.CTkButton(
                atalhos,
                text=f"{icone}   {nome}",
                height=50,
                corner_radius=12,
                fg_color=ITEM,
                hover_color="#34474D",
                font=("Arial", 13, "bold"),
                command=lambda p=nome: self.mostrar_pagina(p)
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=5
            )

        # Últimos acessos
        cabecalho = ctk.CTkFrame(
            self.conteudo,
            fg_color="transparent"
        )
        cabecalho.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            cabecalho,
            text="Últimos acessos",
            font=("Arial", 19, "bold"),
            text_color="white"
        ).pack(side="left")

        ctk.CTkButton(
            cabecalho,
            text="Ver histórico",
            width=120,
            height=32,
            fg_color=ITEM,
            hover_color="#34474D",
            command=lambda: self.mostrar_pagina("Histórico")
        ).pack(side="right")

        lista = ctk.CTkScrollableFrame(
            self.conteudo,
            fg_color=PAINEL,
            corner_radius=14,
            height=175
        )
        lista.pack(fill="both", expand=True)

        registros = consultar_historico()[:5]

        if not registros:
            ctk.CTkLabel(
                lista,
                text="Nenhum acesso registrado.",
                text_color=TEXTO_SECUNDARIO
            ).pack(pady=25)
            return

        for nome, data_hora, resultado in registros:
            linha = ctk.CTkFrame(
                lista,
                fg_color=ITEM,
                corner_radius=9
            )
            linha.pack(fill="x", padx=6, pady=5)

            data = datetime.strptime(
                data_hora, "%Y-%m-%d %H:%M:%S"
            )

            autorizado = resultado == "AUTORIZADO"

            ctk.CTkLabel(
                linha,
                text=nome,
                font=("Arial", 12, "bold"),
                anchor="w"
            ).pack(side="left", padx=15, pady=12)

            ctk.CTkLabel(
                linha,
                text="AUTORIZADO" if autorizado else "NÃO AUTORIZADO",
                text_color=VERDE_CLARO if autorizado else VERMELHO,
                font=("Arial", 11, "bold")
            ).pack(side="right", padx=15)

            ctk.CTkLabel(
                linha,
                text=data.strftime("%d/%m/%Y  %H:%M"),
                text_color=TEXTO_SECUNDARIO,
                font=("Arial", 11)
            ).pack(side="right", padx=15)

    def pagina_cadastro(self):
        self.titulo(
            "Cadastrar pessoa",
            "Adicione uma pessoa ao controle de acesso."
        )

        formulario = ctk.CTkFrame(
            self.conteudo,
            fg_color=PAINEL,
            corner_radius=14
        )
        formulario.pack(fill="x")

        ctk.CTkLabel(
            formulario,
            text="Dados do cadastro",
            font=("Arial", 19, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 15))

        self.nome = ctk.CTkEntry(
            formulario,
            placeholder_text="Nome completo",
            height=44
        )
        self.nome.pack(fill="x", padx=25, pady=7)

        self.matricula = ctk.CTkEntry(
            formulario,
            placeholder_text="Matrícula",
            height=44
        )
        self.matricula.pack(fill="x", padx=25, pady=7)


        # Fotografia facial
        self.caminho_foto = None
        self.imagem_preview = None

        ctk.CTkLabel(
            formulario,
            text="Fotografia facial",
            font=("Arial", 13, "bold"),
            text_color="white"
        ).pack(anchor="w", padx=25, pady=(15, 8))

        self.preview_foto = ctk.CTkLabel(
            formulario,
            text="Nenhuma fotografia selecionada",
            width=150,
            height=115,
            fg_color=ITEM,
            corner_radius=10,
            text_color=TEXTO_SECUNDARIO
        )
        self.preview_foto.pack(anchor="w", padx=25, pady=(0, 10))

        ctk.CTkButton(
            formulario,
            text="Selecionar fotografia",
            height=38,
            width=190,
            fg_color=ITEM,
            hover_color="#34474D",
            command=self.selecionar_foto
        ).pack(anchor="w", padx=25, pady=(0, 10))


        self.autorizado = ctk.CTkCheckBox(
            formulario,
            text="Autorizar entrada no prédio",
            fg_color=VERDE
        )
        self.autorizado.pack(anchor="w", padx=25, pady=20)

        ctk.CTkButton(
            formulario,
            text="Salvar cadastro",
            height=44,
            fg_color=VERDE,
            hover_color="#1B6D3F",
            command=self.salvar
        ).pack(fill="x", padx=25, pady=(0, 25))

        self.mensagem = ctk.CTkLabel(
            self.conteudo,
            text=""
        )
        self.mensagem.pack(pady=15)

    def salvar(self):
        nome = self.nome.get().strip()
        matricula = self.matricula.get().strip()

        if not nome or not matricula:
            self.mensagem.configure(
                text="Preencha nome e matrícula.",
                text_color=VERMELHO
            )
            return

        
        caminho_salvo = None

        try:
            with conectar() as conexao:
                # Primeiro, salva o cadastro no banco
                cursor = conexao.execute(
                    """
                    INSERT INTO pessoas
                        (nome, matricula, autorizado)
                    VALUES (?, ?, ?)
                    """,
                    (nome, matricula, self.autorizado.get())
                )

                pessoa_id = cursor.lastrowid

                if self.caminho_foto:
                    pasta_fotos = (
                        Path(__file__).resolve().parent.parent
                        / "assets" / "rostos_cadastrados"
                    )
                    pasta_fotos.mkdir(
                        parents=True, exist_ok=True
                    )

                    nome_arquivo = (
                        f"pessoa_{pessoa_id}_{uuid4().hex[:8]}.jpg"
                    )
                    destino = pasta_fotos / nome_arquivo

                    # Cria uma cópia padronizada da foto
                    with Image.open(self.caminho_foto) as imagem:
                        imagem = imagem.convert("RGB")
                        imagem.thumbnail((1200, 1200))
                        imagem.save(
                            destino,
                            format="JPEG",
                            quality=90
                        )

                    caminho_salvo = destino

                    # Vincula a fotografia ao cadastro
                    conexao.execute(
                        """
                        UPDATE pessoas
                        SET foto_referencia = ?
                        WHERE id = ?
                        """,
                        (str(destino), pessoa_id)
                    )

        except sqlite3.IntegrityError:
            self.mensagem.configure(
                text="Essa matrícula já existe.",
                text_color=VERMELHO
            )
            return

        except (OSError, ValueError) as erro:
            if caminho_salvo is not None:
                caminho_salvo.unlink(missing_ok=True)

            self.mensagem.configure(
                text=f"Não foi possível salvar a foto: {erro}",
                text_color=VERMELHO
            )
            return


        self.nome.delete(0, "end")
        self.matricula.delete(0, "end")
        self.autorizado.deselect()
        self.caminho_foto = None
        self.imagem_preview = None
        self.preview_foto.configure(
            image=None,
            text="Nenhuma fotografia selecionada"
        )

        self.mensagem.configure(
            text="Pessoa cadastrada com sucesso!",
            text_color=VERDE_CLARO
        )

    def pagina_pessoas(self):
        self.titulo(
            "Pessoas cadastradas",
            "Consulte e gerencie as permissões de entrada."
        )

        self.busca = ctk.CTkEntry(
            self.conteudo,
            placeholder_text="Buscar por nome ou matrícula...",
            height=42
        )
        self.busca.pack(fill="x", pady=(0, 15))
        self.busca.bind(
            "<KeyRelease>",
            lambda evento: self.atualizar_pessoas()
        )

        self.lista_pessoas = ctk.CTkScrollableFrame(
            self.conteudo,
            fg_color=PAINEL
        )
        self.lista_pessoas.pack(fill="both", expand=True)

        self.atualizar_pessoas()

    def atualizar_pessoas(self):
        for widget in self.lista_pessoas.winfo_children():
            widget.destroy()

        termo = f"%{self.busca.get().strip()}%"

        with conectar() as conexao:
            pessoas = conexao.execute(
                """
                SELECT id, nome, matricula, autorizado
                FROM pessoas
                WHERE nome LIKE ? OR matricula LIKE ?
                ORDER BY nome
                """,
                (termo, termo)
            ).fetchall()

        if not pessoas:
            ctk.CTkLabel(
                self.lista_pessoas,
                text="Nenhuma pessoa encontrada."
            ).pack(pady=25)
            return

        for pessoa_id, nome, matricula, autorizado in pessoas:
            linha = ctk.CTkFrame(
                self.lista_pessoas,
                fg_color=ITEM,
                corner_radius=10
            )
            linha.pack(fill="x", padx=6, pady=5)

            ctk.CTkLabel(
                linha,
                text=f"{nome}\n{matricula}",
                anchor="w",
                justify="left",
                font=("Arial", 13)
            ).pack(side="left", padx=15, pady=10)

            texto = "AUTORIZADO" if autorizado else "NÃO AUTORIZADO"
            cor = VERDE_CLARO if autorizado else VERMELHO

            ctk.CTkLabel(
                linha,
                text=texto,
                text_color=cor,
                font=("Arial", 11, "bold")
            ).pack(side="right", padx=15)

            ctk.CTkButton(
                linha,
                text="Bloquear" if autorizado else "Autorizar",
                width=90,
                height=30,
                fg_color="#40474B",
                hover_color="#515B60",
                command=lambda pid=pessoa_id, atual=autorizado:
                    self.alterar_permissao(pid, atual)
            ).pack(side="right", padx=5)


            ctk.CTkButton(
                linha,
                text="Editar",
                width=65,
                height=30,
                fg_color="#34474D",
                hover_color="#456068",
                command=lambda pid=pessoa_id: self.editar_pessoa(pid)
            ).pack(side="right", padx=4)

            ctk.CTkButton(
                linha,
                text="Excluir",
                width=65,
                height=30,
                fg_color="#603238",
                hover_color="#824047",
                command=lambda pid=pessoa_id: self.excluir_pessoa(pid)
            ).pack(side="right", padx=4)


    def alterar_permissao(self, pessoa_id, autorizado_atual):
        with conectar() as conexao:
            conexao.execute(
                "UPDATE pessoas SET autorizado = ? WHERE id = ?",
                (0 if autorizado_atual else 1, pessoa_id)
            )

        self.atualizar_pessoas()

    def pagina_historico(self):
        self.titulo(
            "Histórico de acessos",
            "Consulte as tentativas de acesso ao prédio."
        )

        lista = ctk.CTkScrollableFrame(
            self.conteudo,
            fg_color=PAINEL
        )
        lista.pack(fill="both", expand=True)

        registros = consultar_historico()

        if not registros:
            ctk.CTkLabel(
                lista,
                text="Nenhum acesso registrado."
            ).pack(pady=30)
            return

        for nome, data_hora, resultado in registros:
            linha = ctk.CTkFrame(
                lista,
                fg_color=ITEM,
                corner_radius=10
            )
            linha.pack(fill="x", padx=6, pady=5)

            data = datetime.strptime(
                data_hora, "%Y-%m-%d %H:%M:%S"
            )

            ctk.CTkLabel(
                linha,
                text=nome,
                anchor="w",
                font=("Arial", 13, "bold")
            ).pack(side="left", padx=15, pady=13)

            autorizado = resultado == "AUTORIZADO"

            ctk.CTkLabel(
                linha,
                text="AUTORIZADO" if autorizado else "NÃO AUTORIZADO",
                text_color=VERDE_CLARO if autorizado else VERMELHO,
                font=("Arial", 11, "bold")
            ).pack(side="right", padx=15)

            ctk.CTkLabel(
                linha,
                text=data.strftime("%d/%m/%Y  %H:%M"),
                text_color=TEXTO_SECUNDARIO
            ).pack(side="right", padx=15)


    def editar_pessoa(self, pessoa_id):
        with conectar() as conexao:
            pessoa = conexao.execute(
                "SELECT nome, matricula FROM pessoas WHERE id = ?",
                (pessoa_id,)
            ).fetchone()

        if pessoa is None:
            messagebox.showerror(
                "FaceAccess", "Cadastro não encontrado.",
                parent=self
            )
            self.atualizar_pessoas()
            return

        janela = ctk.CTkToplevel(self)
        janela.title("FaceAccess | Editar pessoa")
        janela.geometry("450x340")
        janela.resizable(False, False)
        janela.configure(fg_color=FUNDO)
        janela.transient(self)
        janela.grab_set()
        janela.lift()

        ctk.CTkLabel(
            janela,
            text="Editar cadastro",
            font=("Arial", 23, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 20))

        campo_nome = ctk.CTkEntry(
            janela, height=42
        )
        campo_nome.pack(fill="x", padx=25, pady=6)
        campo_nome.insert(0, pessoa[0])

        campo_matricula = ctk.CTkEntry(
            janela, height=42
        )
        campo_matricula.pack(fill="x", padx=25, pady=6)
        campo_matricula.insert(0, pessoa[1])

        mensagem = ctk.CTkLabel(janela, text="")
        mensagem.pack(pady=6)

        def salvar_edicao():
            nome = campo_nome.get().strip()
            matricula = campo_matricula.get().strip()

            if not nome or not matricula:
                mensagem.configure(
                    text="Preencha os dois campos.",
                    text_color=VERMELHO
                )
                return

            try:
                with conectar() as conexao:
                    conexao.execute(
                        """
                        UPDATE pessoas
                        SET nome = ?, matricula = ?
                        WHERE id = ?
                        """,
                        (nome, matricula, pessoa_id)
                    )
            except sqlite3.IntegrityError:
                mensagem.configure(
                    text="Essa matrícula já existe.",
                    text_color=VERMELHO
                )
                return

            janela.destroy()
            self.atualizar_pessoas()

        ctk.CTkButton(
            janela,
            text="Salvar alterações",
            height=42,
            fg_color=VERDE,
            hover_color="#1B6D3F",
            command=salvar_edicao
        ).pack(fill="x", padx=25, pady=8)

        def excluir_pessoa(self, pessoa_id):
            with conectar() as conexao:
                pessoa = conexao.execute(
                    "SELECT nome FROM pessoas WHERE id = ?",
                    (pessoa_id,)
                ).fetchone()

                if pessoa is None:
                    messagebox.showerror(
                        "FaceAccess", "Cadastro não encontrado.",
                        parent=self
                    )
                    self.atualizar_pessoas()
                    return

                registros = conexao.execute(
                    """
                    SELECT COUNT(*)
                    FROM registros_acesso
                    WHERE pessoa_id = ?
                    """,
                    (pessoa_id,)
                ).fetchone()[0]

            if registros > 0:
                messagebox.showwarning(
                    "FaceAccess",
                    "Esta pessoa possui histórico de acesso.\n"
                    "Para preservar os registros, bloqueie "
                    "o acesso em vez de excluir.",
                    parent=self
                )
                return

            confirmar = messagebox.askyesno(
                "Confirmar exclusão",
                f"Deseja excluir o cadastro de {pessoa[0]}?",
                parent=self
            )

            if not confirmar:
                return

            with conectar() as conexao:
                conexao.execute(
                    "DELETE FROM pessoas WHERE id = ?",
                    (pessoa_id,)
                )

            self.atualizar_pessoas()


    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(
            parent=self,
            title="Selecionar fotografia facial",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not caminho:
            return

        try:
            with Image.open(caminho) as imagem:
                imagem = imagem.convert("RGB")
                imagem.thumbnail((150, 115))

                preview = ctk.CTkImage(
                    light_image=imagem,
                    dark_image=imagem,
                    size=imagem.size
                )

            self.caminho_foto = caminho
            self.imagem_preview = preview

            self.preview_foto.configure(
                image=preview,
                text=""
            )

        except (OSError, ValueError):
            self.caminho_foto = None
            self.preview_foto.configure(
                image=None,
                text="Imagem inválida"
            )


if __name__ == "__main__":
    app = PainelAdmin()
    app.mainloop()
