import pandas as pd
from sqlalchemy import create_engine

def importarCsv(caminho_csv, nome_tabela):
    # Ler o arquivo CSV com a codificação correta
    df = pd.read_csv(caminho_csv, encoding='utf-8', low_memory=False, sep=';')

    # Conectar ao banco de dados PostgreSQL
    engine = create_engine('postgresql+psycopg2://veiculos:veiculos@localhost:5432/veiculos_locacao')

    # Importar os dados e criar a tabela automaticamente
    df.to_sql(nome_tabela, engine, index=False, if_exists='replace', chunksize=1000)

    print(f"Tabela '{nome_tabela}' criada e dados importados com sucesso!")

# Exemplo de uso da função
print("Iniciando o script...")
#print("Dados de abastecimento: ")
#importarCsv('dados_brutos_abastecimento.csv', 'abastecimento')
#print("Concluído!")