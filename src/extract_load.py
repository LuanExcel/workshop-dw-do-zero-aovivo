# import

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# import das variáveis de ambiente

load_dotenv()

commodities = ['CL=F','GC=F','SI=F']

DB_HOST=os.getenv('DB_HOST_PROD')
DB_PORT=os.getenv('DB_PORT_PROD')
DB_NAME=os.getenv('DB_NAME_PROD')
DB_USER=os.getenv('DB_USER_PROD')
DB_PASS=os.getenv('DB_PASS_PROD')
DB_SCHEMA=os.getenv('DB_SCHEMA_PROD')


#URL DE CONEXAO POSTGRES
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#CONECTAR NO BANCO
engine = create_engine(DATABASE_URL)


#/Buscando Dados
def buscar_dados_commodities(simbolo,periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo,interval=intervalo)[['Close']]
    dados['Simbolo'] = simbolo
    return dados

def buscar_todos_dados_commodities(commodities):
    dados_concatenados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        dados_concatenados.append(dados)
    return pd.concat(dados_concatenados)

def salvar_no_postgres(df,schema='public'):
    df.to_sql('commodities',engine,if_exists='replace',index=True,index_label='Date',schema=schema )

if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados,schema='public')  