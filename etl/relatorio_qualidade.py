import pandas as pd
import sys

sys.stdout.reconfigure(encoding="utf-8")

caminho_arquivo = "C:\\Users\\Dinah\\Documents\\projects\\DataPulseLab\\dados\\pacientes_brutos.csv"

dados = pd.read_csv(
    caminho_arquivo,
    encoding="utf-8"
)

# Recalcular validações
dados["email_valido"] = dados["email"].str.contains("@", na=False)

dados["cpf_valido"] = dados["cpf"].str.len() == 14

# Métrica de qualidade
total_registros = len(dados)

emails_validos = dados["email_valido"].sum()

cpfs_validos = dados["cpf_valido"].sum()

registros_completos = dados.dropna().shape[0]

percentual_emails_validos = (
    emails_validos / total_registros
) * 100

percentual_cpfs_validos = (
    cpfs_validos / total_registros
) * 100

percentual_completos = (
    registros_completos / total_registros
) * 100

# Relatório
relatorio = pd.DataFrame({

    "Métrica": [

        "Total de registros",
        "Emails válidos",
        "CPFs válidos",
        "Registros completos",
        "Percentual emails válidos",
        "Percentual CPFs válidos",
        "Percentual registros completos"

    ],

    "Valor": [

        total_registros,
        emails_validos,
        cpfs_validos,
        registros_completos,
        round(percentual_emails_validos, 2),
        round(percentual_cpfs_validos, 2),
        round(percentual_completos, 2)

    ]

})

print("\nRelatório de Qualidade:")

print(relatorio)

# EXPORTAR RELATÓRIO
relatorio.to_csv(

    "relatorio_qualidade_dados.csv",

    index=False,
    encoding="utf-8"

)

print("\nArquivo gerado:")

print("relatorio_qualidade_dados.csv")

# EXPORTAR DADOS LIMPOS
dados.to_csv(

    "pacientes_tratados.csv",

    index=False,
    encoding="utf-8"

)

print("\nArquivo gerado:")

print("pacientes_tratados.csv")