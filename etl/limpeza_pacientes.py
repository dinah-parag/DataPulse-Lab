import pandas as pd
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding="utf-8")

caminho_arquivo = "C:\\Users\\Dinah\\Documents\\projects\\DataPulseLab\\dados\\pacientes_brutos.csv"

dados = pd.read_csv(
    caminho_arquivo,
    encoding="utf-8",
    sep=","
)

print("Registros antes da limpeza:")
print(len(dados))

# Padronizar nomes
dados["nome"] = dados["nome"].str.strip()
dados["nome"] = dados["nome"].str.title()


# Tratar dados
dados["data_nascimento"] = pd.to_datetime(
    dados["data_nascimento"],
    errors="coerce"
)

# Remover datas inválidas
dados = dados.dropna(subset=["data_nascimento"])

# Remover datas futuras
hoje = datetime.today()

dados = dados[
    dados["data_nascimento"] <= hoje
]

# Tratar telefones
dados["telefone"] = dados["telefone"].fillna(
    "Não informado"
)


# Tratar emails
dados["email"] = dados["email"].fillna(
    "Não informado"
)

# Remover CPFs suplicados
dados = dados.drop_duplicates(
    subset=["cpf"]
)

print("\nRegistros após limpeza:")
print(len(dados))

print("\nDados limpos:")
print(dados)