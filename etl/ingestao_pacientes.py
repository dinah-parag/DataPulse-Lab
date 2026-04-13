import pandas as pd

caminho_arquivo = "C:\\Users\\Dinah\\Documents\\projects\\DataPulseLab\\dados\\pacientes_brutos.csv"

dados = pd.read_csv(caminho_arquivo)

print("Dados carregados:")
print(dados.head())
print("\nQuantidade de registros:")
print(len(dados))