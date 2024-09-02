# %%[markdown]
# # Classificação da Qualidade do Solo com Machine Learning
# Autor: Fernando Basquiro de Souza.

# ## Introdução
# A definição de uma classe para a qualidade do solo pode facilitar a comunicação e indicar rapidamente as características do material em análise. Há diferentes abordagens para a classificação da qualidade do solo conforme a destinação do seu uso, podendo ainda diferentes técnicas de classificação serem usadas (e.g. Somatório de Pontos, Lógica Difusa, Aprendizado de Máquina).<br><br>
# A avaliação da qualidade de um solo e suas camadas pode ser destinada para a seleção de jazidas de argila para construção de solos na recuperação ambiental de áreas mineradas (SOUZA et al, 2018); compreensão e monitoramento de solos florestais (AMACHER et al, 2007); e análise de viabilidade para agricultura (GRUIJTER et al, 2011).<br><br>
# Dessa forma, a partir de um conjunto de dados de amostras de solos disponibilizados pela EMBRAPA (2004), foram aplicadas técnicas de aprendizado de máquina (*machine learning*) da biblioteca scikit-learn em Python para avaliar as respostas obtidas.<br><br>

# ## Referências
# - SOUZA et al, 2018. A fuzzy logic-based expert system for substrate selection for soil construction in land reclamation. *REM - International Engineering Journal*, 71(4):553–559.<br>
# - AMACHER et al. 2007. Soil vital signs: A new soil quality index (SQI) for assessing forest soil health. U.S. Department of Agriculture, Forest Service, pages 1–12.<br>
# - GRUIJTER et al. 2011. Application of fuzzy logic to boolean models for digital soil assessment. *Geoderma*, 166(1):15–33.<br>
# - Empresa Brasileira de Pesquisa Agropecuária - EMBRAPA. 2004. *Solos do Estado de Santa Catarina*. EMBRAPA-CNPS, Rio de Janeiro.<br>
# - Téo Calvo. Machine learning para pôneis, 2024. Último acesso em 30 Setembro 2024. URL: https://www.youtube.com/playlist?list=PLvlkVRRKOYFTXcpttQSZmv1wDg7F3uH7o.<br>

# ## Desenvolvimento
# Nas linhas seguintes são apresentados os códigos aplicados para executar uma análise inicial dos dados importados, sendo que em seguida aplicou-se as técnicas de *machine learning* para prever a qualidade das amostras de solo.<br><br>
# As bibliotecas utilizadas foram: pandas para importar e gerenciar os dados; matplotlib para geração de gráficos; e sklearn para executar os modelos de aprendizado de máquina.
# %% 
# Importando as bibliotecas.
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn import naive_bayes
import matplotlib.pyplot as plt

# %%
# Realizando a leitura do arquivo com os dados de solo
caminho = r'D:/github/py_codes/'
dados = pd.read_csv(caminho+'soil_quality_data.csv', 
                    sep=',', decimal='.')

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
dados.query('pH < 4.0 and tA_perc > 70')

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

# Se usar todas os atributos, algoritmo da regressão não converge... 
# list(dados.columns[2:16])
# https://scikit-learn.org/stable/modules/preprocessing.html

# Acerto se previsão for aleatória
dados.qualidade.mean()

# %%
atributos = ['tA_perc', 'pH', 'c_org_perc', 'na_cmolc', 'k_cmolc', 'p_ppm', 'sat_al_perc']
resultado = ['qualidade']

regressao = linear_model.LogisticRegression(penalty=None, fit_intercept=True, max_iter=200)
regressao.fit(dados[atributos], dados[resultado].values.ravel())

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
print('Acurácia Árvore Decisão: ', acuracia)

precisao = metrics.precision_score(dados[resultado], arvore_previsao)
print('Precisão Árvore Decisão: ', precisao)

recall = metrics.recall_score(dados[resultado], arvore_previsao)
print('Recall Árvore Decisão: ', recall)

arvore_matriz_confusao = metrics.confusion_matrix(dados[resultado], arvore_previsao)
df_mat_conf_arv = pd.DataFrame(arvore_matriz_confusao, 
                               index=['False', 'True'],
                               columns=['False', 'True'])
print(df_mat_conf_arv)
# %%
nb = naive_bayes.GaussianNB()
nb.fit(dados[atributos], dados[resultado].values.ravel())
nb_previsao = nb.predict(dados[atributos])

acuracia = metrics.accuracy_score(dados[resultado], nb_previsao)
print('Acurácia Naive Bayes: ', acuracia)

precisao = metrics.precision_score(dados[resultado], nb_previsao)
print('Precisão Naive Bayes: ', precisao)

recall = metrics.recall_score(dados[resultado], nb_previsao)
print('Recall Naive Bayes: ', recall)

nb_matriz_confusao = metrics.confusion_matrix(dados[resultado], nb_previsao)
df_mat_conf_nb = pd.DataFrame(nb_matriz_confusao, 
                               index=['False', 'True'],
                               columns=['False', 'True'])
print(df_mat_conf_nb)
# %%
# Probabilidade de cada registro pertencer à qualidade True (boa).
nb_probabilidade = nb.predict_proba(dados[atributos])[:,1]
dt_probabilidade = arvore.predict_proba(dados[atributos])[:,1]
lr_probabilidade = regressao.predict_proba(dados[atributos])[:,1]

#%%
# Gerando a Curva ROC
curva_roc_nb = metrics.roc_curve(dados[resultado], nb_probabilidade)
curva_roc_dt = metrics.roc_curve(dados[resultado], dt_probabilidade)
curva_roc_lr = metrics.roc_curve(dados[resultado], lr_probabilidade)
plt.plot(curva_roc_nb[0], curva_roc_nb[1])
plt.plot(curva_roc_dt[0], curva_roc_dt[1])
plt.plot(curva_roc_lr[0], curva_roc_lr[1])
plt.grid(True)
plt.plot([0,1], [0,1], '--')
plt.legend(["Naive Bayes", "Árvore de Decisão", 'Regressão Logística', 'Média'])
plt.show()

# %%
roc_auc_nb = metrics.roc_auc_score(dados[resultado], nb_probabilidade)
print('Área Curva ROC NB: ', roc_auc_nb)

roc_auc_dt = metrics.roc_auc_score(dados[resultado], dt_probabilidade)
print('Área Curva ROC DT: ', roc_auc_dt)

roc_auc_lr = metrics.roc_auc_score(dados[resultado], lr_probabilidade)
print('Área Curva ROC LR: ', roc_auc_lr)