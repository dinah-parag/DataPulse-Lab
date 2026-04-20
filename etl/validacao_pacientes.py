import pandas as pd
import re
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Caminho do arquivo
caminho_arquivo = "C:\\Users\\Dinah\\Documents\\projects\\DataPulseLab\\dados\\pacientes_brutos.csv"

# Ler dados
dados = pd.read_csv(
    caminho_arquivo,
    encoding="utf-8"
)

# Validação de e-mail

def validar_email(email):

    if pd.isna(email):
        return False

    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return bool(re.match(padrao, str(email)))

dados["email_valido"] = dados["email"].apply(validar_email)

# Validação de CPF

def validar_cpf(cpf):

    if pd.isna(cpf):
        return False

    padrao = r"\d{3}\.\d{3}\.\d{3}-\d{2}"

    return bool(re.fullmatch(padrao, str(cpf)))

dados["cpf_valido"] = dados["cpf"].apply(validar_cpf)

# Calculo de idade

dados["data_nascimento"] = pd.to_datetime(
    dados["data_nascimento"],
    errors="coerce"
)

hoje = datetime.today()

dados["idade"] = (
    hoje.year
    - dados["data_nascimento"].dt.year
)

# Detecção de anomalias em idades

dados["anomalia_idade"] = (
    (dados["idade"] < 0)
    |
    (dados["idade"] > 120)
)

# Score sobre a qualidade de dados

dados["score_qualidade"] = (
    dados["email_valido"].astype(int)
    +
    dados["cpf_valido"].astype(int)
    +
    (~dados["anomalia_idade"]).astype(int)
)

print("\nResultado da validação:")

print(
    dados[
        [
            "nome",
            "email",
            "email_valido",
            "cpf",
            "cpf_valido",
            "idade",
            "anomalia_idade",
            "score_qualidade"
        ]
    ]
)