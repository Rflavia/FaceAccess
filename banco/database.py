
import sqlite3
from pathlib import Path

# Local onde o banco será armazenado
CAMINHO_BANCO = Path(__file__).resolve().parent / "faceaccess.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_banco():
    with conectar() as conexao:

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula TEXT UNIQUE NOT NULL,
                foto_referencia TEXT,
                autorizado INTEGER NOT NULL DEFAULT 0
                    CHECK (autorizado IN (0, 1)),
                data_cadastro TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS registros_acesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pessoa_id INTEGER,
                resultado TEXT NOT NULL
                    CHECK (resultado IN ('AUTORIZADO', 'NEGADO')),
                motivo TEXT,
                data_hora TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pessoa_id)
                    REFERENCES pessoas(id)
            )
        """)

    print("Banco FaceAccess criado com sucesso!")


if __name__ == "__main__":
    criar_banco()
