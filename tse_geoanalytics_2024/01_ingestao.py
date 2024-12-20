# %%
import json
import pandas as pd
import sqlalchemy

# %%
# Code base: https://github.com/TeoMeWhy/tse-analytics-2024/
# Data source: https://dadosabertos.tse.jus.br/dataset/candidatos-2024

engine = sqlalchemy.create_engine("sqlite:///database.db")

with open('ingestoes.json', 'r') as open_file:
    ingestoes = json.load(open_file)

for i in ingestoes:
    df = pd.read_csv(i['path'], encoding='latin-1', sep=';')
    df.to_sql(i['table'], engine, if_exists='replace', index=False) 