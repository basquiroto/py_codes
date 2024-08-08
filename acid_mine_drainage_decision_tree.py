# %%
# Applying a decision tree to some spoil rocks from coal mining areas.
# Reference: Teo Me Why (YouTube). https://www.youtube.com/watch?v=oj0ACpEHpS0&list=PLvlkVRRKOYFTXcpttQSZmv1wDg7F3uH7o&index=1
# Data reference: Artigo CBCM 2017. https://www.researchgate.net/publication/319169453_Avaliacao_do_potencial_de_geracao_de_drenagem_acida_atraves_da_aplicacao_de_metodos_estaticos

import pandas as pd
import numpy as np
from sklearn import tree
import matplotlib.pyplot as plt
# %%
df = pd.read_csv(r'D:/github/acid_mine_drainage_decision_tree_data.csv', sep=';', decimal=',')
df

# %%
a_samples = df['Nome'].str.startswith('A', na=False)
t_samples = df['Nome'].str.startswith('T', na=False)
u_samples = df['Nome'].str.startswith('U', na=False)

print('Quantidade de Amostras por Área: ')
print('A: ', len(df[a_samples])) # 106
print('T: ', len(df[t_samples])) # 23
print('U: ', len(df[u_samples])) # 23

# %%
# Applying some filters to reduce quantity of distinct areas.
filter = df['Nome'].isin(['U001', 'U002', 'U003', 'U004'])
df_uru = df[filter]

# %%
features = ['pH_h2o', 'S_total_perc', 'PN', 'PA', 'NN']
target = 'Nome'

X = df_uru[features]
y = df_uru[target]
# %%
arvore = tree.DecisionTreeClassifier()
arvore.fit(X, y)

# %%
plt.figure(dpi=600)

tree.plot_tree(arvore,
               class_names=arvore.classes_,
               feature_names=features,
               filled=True)
# %%
predict_target = [[4.4, 0.12, -3.0, 5.5, 10]]
# %%
arvore.predict(predict_target)
# %%
probas = arvore.predict_proba(predict_target)[0]
pd.Series(probas, index=arvore.classes_)
# %%
# Testing with A samples. Training data.
df_ara = df.iloc[np.r_[0:7, 10:14, 16, 18, 19, 67:93, 103:113, 118, 119, 121:126, 129:141, 146:150]]
# %%
features = ['pH_h2o', 'S_total_perc', 'PN', 'PA', 'NN']
target = 'Nome'

X2 = df_ara[features]
y2 = df_ara[target]

arvore2 = tree.DecisionTreeClassifier()
arvore2.fit(X2, y2)

# %%
plt.figure(dpi=600)

tree.plot_tree(arvore2,
               class_names=arvore2.classes_,
               feature_names=features,
               filled=True)
# %%
indice = 144
predict_target = [list(df.iloc[indice, 1:6])]
predicted_area = arvore2.predict(predict_target)[0]

print('A amostra é da área: ', df.iloc[indice, 0])
print('A árvore de decisão diz que é da área: ', predicted_area)

# %%
probas = arvore2.predict_proba(predict_target)[0]
pd.Series(probas, index=arvore2.classes_)