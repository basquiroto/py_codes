# %% 
# Importando as bibliotecas
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn import naive_bayes
import matplotlib.pyplot as plt

# %%
# Realizando a leitura do arquivo com os dados de solo
# Fonte dos dados. 
# EMBRAPA - Empresa Brasileira de Pesquisa Agropecuária. Solos do Estado de Santa Catarina. Rio de Janeiro: EMBRAPA-CNPS, 2004. 745 p.

caminho = r'D:/github/py_codes/'
dados = pd.read_csv(caminho+'soil_quality_data.csv', sep=',', decimal='.')

# %%
# Analisandos os dados importados (amostragem de 5 linhas)
dados.sample(5)

# %% 
# Verificando se há dados faltando.
dados.isna().sum()

# %%
# Contagem de dados existentes
nr_amostras = len(dados) # ou dados.shape[0]
print('Número de amostras de solo: ', nr_amostras)

nr_atributos = dados.shape[1]
print('Número de atributos: ', nr_atributos)

print('Estatísticas básicas: ')
dados.describe()

# %%
# Realizando buscas dentro do DataFrame
print('Amostras de solo com pH maior que 5.5: ')
condicao1 = dados.pH > 5.5
dados[condicao1]

# %%
print('Amostras com teor de argila entre 40 e 60%: ')
condicao2 = (dados.tA_perc > 40) & (dados.tA_perc < 60)
dados[condicao2]

# %%
print('Amostras de solo com pH menor que 4.5 e teor de argila maior que 70%: ')
condicao3A = (dados.pH < 4.0)
condicao3B = (dados.tA_perc > 70)
dados[condicao3A][condicao3B]

# %% 
# Acessando registro específico (linha) a partir do index.
# .loc[] busca pelo Label da linha/coluna.
# .iloc[] busca pelo índice da linha/coluna.

dados.iloc[70, :]

# %%
# Acessando coluna específica a partir do rótulo.
dados.loc[:, 'horizonte']

# %%
# Criando nova coluna a partir de SQI_perc
dados['qualidade'] = dados.SQI_perc > 30 # Se maior que 30, bom (true)

# %%
# Aplicando métricas (Curso Machine Learning para Póneis)
# https://github.com/TeoMeWhy/ml-4-poneis/blob/main/dia04/classificacao.py

# Se usar todas os atributos, algoritmo da regressão não converge... list(dados.columns[2:16])
# https://scikit-learn.org/stable/modules/preprocessing.html
atributos = ['tA_perc', 'pH', 'c_org_perc', 'na_cmolc', 'k_cmolc', 'p_ppm', 'sat_al_perc']
resultado = ['qualidade']

regressao = linear_model.LogisticRegression(penalty=None, fit_intercept=True, max_iter=200)
regressao.fit(dados[atributos], dados[resultado])

previsao = regressao.predict(dados[atributos])
# %%
acuracia = metrics.accuracy_score(dados[resultado], previsao)
print('Acurácia Regressão Logística: ', acuracia)

precisao = metrics.precision_score(dados[resultado], previsao)
print('Precisão Regressão Logística: ', precisao)

recall = metrics.recall_score(dados[resultado], previsao)
print('Recall Regressão Logística: ', recall)

matriz_confusao = metrics.confusion_matrix(dados[resultado], previsao)
df_mat_conf = pd.DataFrame(matriz_confusao, 
                           index=['False', 'True'],
                           columns=['False', 'True'])
print(df_mat_conf)

# %%
arvore = tree.DecisionTreeClassifier(max_depth=3)
arvore.fit(dados[atributos], dados[resultado])
arvore_previsao = arvore.predict(dados[atributos])

acuracia = metrics.accuracy_score(dados[resultado], arvore_previsao)
print('Acurácia Regressão Logística: ', acuracia)

precisao = metrics.precision_score(dados[resultado], arvore_previsao)
print('Precisão Regressão Logística: ', precisao)

recall = metrics.recall_score(dados[resultado], arvore_previsao)
print('Recall Regressão Logística: ', recall)

arvore_matriz_confusao = metrics.confusion_matrix(dados[resultado], arvore_previsao)
df_mat_conf_arv = pd.DataFrame(arvore_matriz_confusao, 
                               index=['False', 'True'],
                               columns=['False', 'True'])
print(df_mat_conf_arv)
# %%
nb = naive_bayes.GaussianNB()
nb.fit(dados[atributos], dados[resultado])
nb_previsao = nb.predict(dados[atributos])

acuracia = metrics.accuracy_score(dados[resultado], nb_previsao)
print('Acurácia Regressão Logística: ', acuracia)

precisao = metrics.precision_score(dados[resultado], nb_previsao)
print('Precisão Regressão Logística: ', precisao)

recall = metrics.recall_score(dados[resultado], nb_previsao)
print('Recall Regressão Logística: ', recall)

nb_matriz_confusao = metrics.confusion_matrix(dados[resultado], nb_previsao)
df_mat_conf_nb = pd.DataFrame(nb_matriz_confusao, 
                               index=['False', 'True'],
                               columns=['False', 'True'])
print(df_mat_conf_nb)
# %%
nb_probabilidade = nb.predict_proba(dados[atributos])[:,1]
nb_probabilidade # Probabilidade de cada registro pertencer à qualidade True (boa).

#%%
curva_roc = metrics.roc_curve(dados[resultado], nb_probabilidade)
plt.plot(curva_roc[0], curva_roc[1] )
plt.grid(True)
plt.plot([0,1], [0,1], '--')
plt.show()

# %%
roc_auc = metrics.roc_auc_score(dados[resultado], nb_probabilidade)
roc_auc