import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
import pandas as pd
import random
from faker import Faker

# ===================== CONFIGURAÇÕES =========================

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "root"  # Altere para sua senha do PostgreSQL
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
DATABASE_NAME = "dim_credor_db"
TABELA_NOME = "dim_credor"

# ==================== CRIAÇÃO DO BANCO =======================

def criar_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(DATABASE_NAME)
            ))
            print(f"Database '{DATABASE_NAME}' criado com sucesso!")
        else:
            print(f"Database '{DATABASE_NAME}' já existe.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar database: {e}")

# ================= GERAR DADOS E IMPORTAR ====================

fake = Faker('pt_BR')

colunas = [
    "SK_CREDOR", "BK_CREDOR", "NM_CREDOR", "NU_CPF", "NU_CNPJ", "CPF_CNPJ", "DE_ENDERECO",
    "CD_ESTADO", "CD_MUNICIPIO", "NM_MUNICIPIO", "NM_TIPO_LOGRADOURO", "NM_LOGRADOURO",
    "NU_LOGRADOURO", "NM_COMPLEMENTO", "CD_LOCALIDADE", "NU_INSCRICAO_GENERICA",
    "NM_BAIRRO", "NU_CEP_CREDOR", "NU_TELEFONE_COM", "NU_INSCRICAO_ESTADUAL",
    "NU_TELEFONE_RES", "NU_INSCRICAO_MUNIC", "NU_TELEFONE_CEL", "DE_EMAIL",
    "NU_TELEFONE_CONT", "DE_OBS", "NU_FAX", "FL_STATUS", "DT_ULT_ALTERACAO",
    "DE_PONTO_REFERENCIA", "NU_NIT_PISPASEP", "FL_AUSENCIA_CONTA", "CD_TIPO_CREDOR",
    "NU_CPFRESPONSAVEL_PJ", "NM_RESPONSAVEL_PJ", "CD_TIPO_INSCRICAO", "CD_CREDOR_CONTADOR",
    "NM_FANTASIA", "CD_SIT_CADASTRO_CNPJ", "DT_SIT_CADASTRO_CNPJ", "NM_CIDADE_EXTERIOR_CNPJ",
    "CD_PAIS_EXTERIOR_CNPJ", "NM_PAIS_EXTERIOR_CNPJ", "CD_NATUREZA_JURIDICA",
    "DT_ABERTURA_CNPJ", "CD_CNAE_PRINCIPAL", "VL_CAPITAL_SOCIAL", "CD_PORTE",
    "FL_OPCAO_SIMPLES", "DT_OPCAO_SIMPLES", "DT_EXCLUSAO_SIMPLES", "CD_SITUACAO_CADASTRO_CPF",
    "DT_ATUALIZACAO_CPF", "FL_RESIDENTE_EXTERIOR_CPF", "CD_PAIS_EXTERIOR_CPF",
    "NM_PAIS_EXTERIOR_CPF", "NM_MAE", "DT_NASCIMENTO", "CD_SEXO_PESSOA_FISICA",
    "CD_NATUREZA_OCUPACAO", "CD_OCUPACAO_PRINCIPAL", "NU_ANO_EXERCICIO_OCUPACAO",
    "CD_UNIDADE_ADMINISTRATIVA", "NU_ANO_OBITO", "FL_ESTRANGEIRO", "NU_TITULO_ELEITOR",
    "DT_ATUALIZACAO_RF", "CD_TIPO_CONSOLIDACAO", "NU_DDD_TELEFONE_CEL", "NU_DDD_TELEFONE_COM",
    "NU_DDD_TELEFONE_CONT", "NU_DDD_TELEFONE_RES", "NU_DDD_FAX", "FL_ATUALIZACAO_RF",
    "DE_ERRO_ATUALIZACAO_RF", "CD_ESTABELECIMENTO", "NU_CNPJ_SUCEDIDA", "NM_CREDOR_SOCIAL",
    "DT_CARGA", "DT_UPDATE"
]

def gerar_dados_exemplo(qtd=3):
    dados = []
    for i in range(qtd):
        cpf = fake.cpf()
        cnpj = fake.cnpj()
        dados.append([
            i + 1, 1000 + i, fake.name(), cpf, cnpj, random.choice([cpf, cnpj]), fake.address(),
            "SP", "3550308", "São Paulo", "Rua", fake.street_name(), str(random.randint(1, 9999)),
            random.choice(["Fundos", "Apto 101", "Bloco B", "Sala 05", "Casa 2"]), "001", str(random.randint(1000000, 9999999)),
            fake.bairro(), fake.postcode(), fake.phone_number(), str(random.randint(100000000, 999999999)),
            fake.phone_number(), str(random.randint(100000000, 999999999)), fake.phone_number(), fake.email(),
            fake.phone_number(), fake.sentence(), fake.phone_number(), "A", fake.date_this_decade().strftime("%Y-%m-%d"),
            fake.street_suffix(), str(random.randint(10000000000, 99999999999)), "N", "001",
            fake.cpf(), fake.name(), "1", str(1000 + i), fake.company_suffix(), "02", fake.date_this_decade().strftime("%Y-%m-%d"),
            "", "", "", "213-5", fake.date_this_decade().strftime("%Y-%m-%d"), "6201-5",
            random.randint(10000, 1000000), "1", "S", fake.date_this_decade().strftime("%Y-%m-%d"),
            fake.date_this_decade().strftime("%Y-%m-%d"), "A", fake.date_this_decade().strftime("%Y-%m-%d"),
            "N", "", "", fake.name(), fake.date_of_birth().strftime("%Y-%m-%d"), "M", "001", "001",
            "2024", "01", "", "N", str(random.randint(10000000000, 99999999999)), fake.date_this_decade().strftime("%Y-%m-%d"),
            "001", "11", "11", "11", "11", "11", "S", "", "12345", fake.cnpj(), fake.company(),
            fake.date_this_decade().strftime("%Y-%m-%d"), fake.date_this_decade().strftime("%Y-%m-%d")
        ])
    return dados

def importar_dados():
    # Criar engine
    engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_NAME}')

    # Gerar dados
    dados = gerar_dados_exemplo(5)  # Quantidade de registros aqui
    df = pd.DataFrame(dados, columns=colunas)

    # Importar para o banco
    df.to_sql(TABELA_NOME, engine, index=False, if_exists='replace', chunksize=1000)
    print(f"Tabela '{TABELA_NOME}' criada e dados inseridos com sucesso!")

# ===================== EXECUÇÃO =============================

if __name__ == "__main__":
    print("Criando database...")
    criar_database()
    print("Importando dados...")
    importar_dados()
    print("✅ Processo concluído!")
