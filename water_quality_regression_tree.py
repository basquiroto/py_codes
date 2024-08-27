# %%
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import tree

# %%
# Code source. https://github.com/TeoMeWhy/ml-4-poneis/blob/main/dia03/cerveja_notas.py
# Data Source. INDE. Indicadores de Qualidade da Água (2001 a 2021).
# https://metadados.inde.gov.br/geonetwork/srv/por/catalog.search;jsessionid=64250ED2AE0E64647D3EFDF420D97DBA#/metadata/647706bb-bbad-4b99-8413-6b4f48697521

file_path = r'D:/github/'
iqa = gpd.read_file(file_path+'iqa.geojson')
od = gpd.read_file(file_path+'oxigeniodissolvido.geojson')
# %%
iqa_nan_values = iqa.isna()
iqa_nan_count = iqa_nan_values.sum(axis=1)
iqa_min_value = iqa_nan_count.min() # 3
#iqa_lots_values = iqa[iqa_nan_count == iqa_min_value]
iqa_lots_values = iqa[iqa_nan_count <= 3]

od_nan_values = od.isna()
od_nan_count = od_nan_values.sum(axis=1)
od_min_value = od_nan_count.min() # 3
#od_lots_values = iqa[od_nan_count == od_min_value]
od_lots_values = od[od_nan_count <= 3]
# %%
iqa_index = set(iqa_lots_values['CDESTACAO'])
od_index = set(od_lots_values['CDESTACAO'])

match_index = iqa_index.intersection(od_index)
print(match_index)
# %%
estacao = 'EMMI02900'
iqa_estacao = iqa_lots_values['CDESTACAO']==estacao
od_estacao = od_lots_values['CDESTACAO']==estacao

iqa_row = pd.DataFrame(iqa_lots_values[iqa_estacao])
od_row = pd.DataFrame(od_lots_values[od_estacao])

df = pd.concat([iqa_row, od_row])
print(df)
# %%
mean_df = df.filter(like='MED_', axis=1)
transp_df = mean_df.T
transp_df.columns = ['iqa', 'od']
# %%
plt.plot(transp_df['od'], transp_df['iqa'], 'o')
plt.grid(True)
plt.title('Relação Oxigênio Dissolvido x IQA (' + estacao + ')')
plt.xlabel('OD (mg/L)')
plt.ylabel('IQA')
plt.show()
# %%
X = transp_df[['od']].dropna()
Y = transp_df[['iqa']].dropna()

reg = linear_model.LinearRegression()
reg.fit(X, Y)

a, b = reg.intercept_, reg.coef_[0]
print(f"y = {round(b[0],4)} + {round(a[0],4)}*x")
# %%
y_estimado = reg.predict(X)
# %%
plt.plot(transp_df["od"], transp_df["iqa"], 'o')
plt.plot(X, y_estimado, '-')
plt.grid(True)
plt.title('Relação Oxigênio Dissolvido x IQA (' + estacao + ')')
plt.xlabel('OD (mg/L)')
plt.ylabel('IQA')
plt.show()

# %%
arvore = tree.DecisionTreeRegressor(max_depth=2)
arvore.fit(X, Y)

y_estimado_arvore = arvore.predict(X)
#y_estimado_arvore.sort()
#reverse_y = list(y_estimado_arvore)[::-1]
# %%
plt.figure(dpi=500)
plt.plot(X, Y, 'o')
plt.plot(X, y_estimado, '-')
plt.plot(X, y_estimado_arvore, 'X')
plt.grid(True)
plt.title('Relação Oxigênio Dissolvido x IQA (' + estacao + ')')
plt.xlabel('OD (mg/L)')
plt.ylabel('IQA')
plt.legend(["Observações", "Regressão Linear", "Árvore de Decisão"])
plt.show()
# %%
## Teste com dados da bacia carbonífera de santa catarina.
agua = pd.read_csv(file_path + 'dados_agua_bcsc.csv', sep=';', decimal=',')
# %%
# Regression model
reg2 = linear_model.LinearRegression()
reg2.fit(agua[['ferro']], agua['sulfato'])

a2, b2 = reg2.intercept_, reg2.coef_[0]
print(f"y = {round(a2, 4)} + {round(b2,4)}*x")

s_estimado = reg2.predict(agua[['ferro']])
# %%
# Decision tree model
arvore2 = tree.DecisionTreeRegressor(max_depth=2)
arvore2.fit(agua[['ferro']], agua['sulfato'])

s_estimado_arvore = arvore2.predict(agua[['ferro']])
# %%
plt.figure(dpi=500)
plt.plot(agua[['ferro']], agua['sulfato'], 'o')
plt.plot(agua[['ferro']], s_estimado, '-')
plt.plot(agua[['ferro']], s_estimado_arvore, 'X')
plt.grid(True)
plt.title('Relação Ferro Total x Sulfatos')
plt.xlabel('Fe Total (mg/L)')
plt.ylabel('Sulfatos (mg/L)')
plt.legend(["Observações", "Regressão Linear", "Árvore de Decisão"])
plt.show()

# %%
# Aplicando com mais dados (Fe + Mn + pH --> Sulfatos)
reg3 = linear_model.LinearRegression()
reg3.fit(agua[['ferro', 'ph', 'manganes']], agua['sulfato'])

a3, b3, b4, b5 = reg3.intercept_, reg3.coef_[0], reg3.coef_[1], reg3.coef_[2]
print(f"y = {round(a3, 4)} + {round(b3,4)}*x + {round(b4,4)}*x + {round(b5,4)}*x")
# %%
