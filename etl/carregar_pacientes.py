import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import pandas as pd
from backend.database import conectar

import sys

sys.stdout.reconfigure(encoding="utf-8")

caminho_arquivo = r"C:\Users\Dinah\Documents\projects\DataPulseLab\pacientes_tratados.csv"

try:

    print("Lendo arquivo...")

    dados = pd.read_csv(
        caminho_arquivo,
        sep=",",
        encoding="utf-8"
    )

    # Padroniza nomes das colunas
    dados.columns = dados.columns.str.strip().str.lower()

    print("Colunas encontradas:")
    print(dados.columns)

    # Converte data
    dados["data_nascimento"] = pd.to_datetime(
        dados["data_nascimento"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    # Cria indicador de validade
    dados["data_valida"] = dados["data_nascimento"].notna()

    # Conta inválidos
    invalidos = dados["data_valida"].value_counts().get(False, 0)

    print(
        "Registros com data inválida:",
        invalidos
    )

    # Filtra apenas registros válidos
    dados_validos = dados[
        dados["data_valida"] == True
    ]

    # Converte formato para MySQL
    dados_validos["data_nascimento"] = dados_validos[
        "data_nascimento"
    ].dt.strftime("%Y-%m-%d")

    print(
        "Registros válidos para inserção:",
        len(dados_validos)
    )

    print("Conectando ao banco...")

    conexao = conectar()

    cursor = conexao.cursor()

    inseridos = 0
    duplicados = 0

    for _, linha in dados_validos.iterrows():

        sql = """
        INSERT INTO pacientes (
            nome,
            cpf,
            data_nascimento,
            sexo,
            telefone,
            email
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nome = VALUES(nome)
        """

        valores = (

            linha["nome"],
            linha["cpf"],
            linha["data_nascimento"],
            linha["sexo"],
            linha["telefone"],
            linha["email"]

        )

        cursor.execute(sql, valores)

        if cursor.rowcount == 1:
            inseridos += 1
        else:
            duplicados += 1

    conexao.commit()

    print("Carga finalizada")

    print("Inseridos:", inseridos)
    print("Duplicados:", duplicados)

    cursor.close()
    conexao.close()

except Exception as erro:

    print("Erro durante carga:")
    print(erro)