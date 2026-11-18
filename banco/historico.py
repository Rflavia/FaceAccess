
from datetime import datetime
from banco.database import conectar


def registrar_acesso(pessoa_id, autorizado):
    """Registra uma tentativa de acesso."""

    resultado = "AUTORIZADO" if autorizado else "NEGADO"

    with conectar() as conexao:
        conexao.execute(
            """
            INSERT INTO registros_acesso
                (pessoa_id, resultado, data_hora)
            VALUES (?, ?, ?)
            """,
            (
                pessoa_id,
                resultado,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )


def consultar_historico():
    """Consulta os acessos mais recentes."""

    with conectar() as conexao:
        registros = conexao.execute(
            """
            SELECT
                COALESCE(p.nome, 'Não identificado'),
                r.data_hora,
                r.resultado
            FROM registros_acesso r
            LEFT JOIN pessoas p
                ON p.id = r.pessoa_id
            ORDER BY r.id DESC
            """
        ).fetchall()

    return registros


if __name__ == "__main__":
    # Teste: registra um acesso de uma pessoa existente.
    with conectar() as conexao:
        pessoa = conexao.execute(
            "SELECT id FROM pessoas ORDER BY id LIMIT 1"
        ).fetchone()

    if pessoa:
        registrar_acesso(pessoa[0], True)
        print("Acesso de teste registrado!")
    else:
        print("Cadastre uma pessoa antes de testar.")

    print("\nHISTÓRICO DE ACESSOS")

    for nome, data_hora, resultado in consultar_historico():
        status = (
            "AUTORIZADO"
            if resultado == "AUTORIZADO"
            else "NÃO AUTORIZADO"
        )

        print(f"{nome} | {data_hora} | {status}")
