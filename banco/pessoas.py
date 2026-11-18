
from database import conectar


def cadastrar_pessoa(nome, matricula, foto_referencia=None, autorizado=False):
    nome = nome.strip()
    matricula = matricula.strip()

    if not nome or not matricula:
        print("Nome e matrícula são obrigatórios.")
        return

    try:
        with conectar() as conexao:
            conexao.execute(
                """
                INSERT INTO pessoas
                    (nome, matricula, foto_referencia, autorizado)
                VALUES (?, ?, ?, ?)
                """,
                (nome, matricula, foto_referencia, int(autorizado))
            )

        print(f"Pessoa cadastrada: {nome}")

    except __import__("sqlite3").IntegrityError:
        print("Já existe uma pessoa com essa matrícula.")


def listar_pessoas():
    with conectar() as conexao:
        pessoas = conexao.execute(
            """
            SELECT id, nome, matricula, autorizado
            FROM pessoas
            ORDER BY nome
            """
        ).fetchall()

    for id_pessoa, nome, matricula, autorizado in pessoas:
        status = "AUTORIZADO" if autorizado else "BLOQUEADO"
        print(f"{id_pessoa} | {nome} | {matricula} | {status}")


if __name__ == "__main__":
    cadastrar_pessoa(
        nome="Pessoa Teste",
        matricula="TESTE001",
        autorizado=True
    )

    listar_pessoas()
