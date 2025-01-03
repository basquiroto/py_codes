# %% 
import pandas as pd
import geopandas as gpd
import sqlalchemy
import matplotlib.pyplot as plt
from shapely import box

# %%
with open('consulta.sql', 'r') as open_file:
    query = open_file.read()

engine = sqlalchemy.create_engine('sqlite:///database.db')

df = pd.read_sql_query(query, engine)
df.head()

# %%
shp_file = r'C:\VM2GEO\SIG\LIM_MUN\SC_Municipios_2021.shp'

mun_shp = gpd.read_file(shp_file)
mun_shp['NM_MUN'] = mun_shp['NM_MUN'].str.upper()

mun_shp.head()

# %%
shp_brasil = r'C:\VM2GEO\SIG\LIM_MUN\BR_UF_2021.shp'
br_shp = gpd.read_file(shp_brasil)

# %%
municipios = mun_shp.merge(df, left_on='NM_MUN', right_on='NM_UE')
municipios.sample(5)

# %%
bounds = municipios.geometry.total_bounds
xmin, ymin, xmax, ymax = bounds

oceano = gpd.GeoDataFrame(geometry=[box(-51, -29.5, -48, -25)], crs=municipios.crs)

# %% 
# Mapa 1. Taxa de Mulheres nos municipios catarinensese.
# https://matplotlib.org/stable/users/explain/colors/colormaps.html
tx_extent = 0.005

fig, ax = plt.subplots(figsize = (9,9))
xlim = ([xmin*(1+tx_extent), xmax*(1-tx_extent)])
ylim = ([ymin*(1+tx_extent), ymax*(1-tx_extent)])

ax.set_xlim(xlim)
ax.set_ylim(ylim)

basemap = br_shp.plot(color='white',
                      ax=ax, 
                      edgecolor='black', 
                      zorder=2)

oceano.plot(ax=ax, color="#d4f1f4", zorder=1)

municipios.plot(column='txGenFeminino',
                ax=ax,
                legend=True,
                cmap='YlGn',
                edgecolor='black',
                linewidth=0.5,
                zorder=3,
                legend_kwds={"label": "Taxa de Mulheres (Eleições 2024)", 
                             "orientation": "horizontal",
                             "pad": 0.05})

top_five = municipios[['NM_MUN', 'txGenFeminino']].nlargest(5, 'txGenFeminino').reset_index(drop=True)

top_text = "\n".join([f'{i+1}. {row['NM_MUN']} ({row['txGenFeminino']})' for i, row in top_five.iterrows()])
plt.text(-54, -28.75, top_text, fontsize=11, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.8))

plt.title('Taxa de Mulheres nas Eleições de 2024', fontsize=14, color='black', style='italic', loc='left')

plt.savefig("./sc_eleicoes_2024_mulheres.png")

# %%
# Mapa 2. Taxa de pessoas pretas nas cidades catarinenses.
tx_extent = 0.005

fig, ax = plt.subplots(figsize = (9,9))
xlim = ([xmin*(1+tx_extent), xmax*(1-tx_extent)])
ylim = ([ymin*(1+tx_extent), ymax*(1-tx_extent)])

ax.set_xlim(xlim)
ax.set_ylim(ylim)

basemap = br_shp.plot(color='white',
                      ax=ax, 
                      edgecolor='black', 
                      zorder=2)

oceano.plot(ax=ax, color="#d4f1f4", zorder=1)

municipios.plot(column='txCorRacaPreta',
                ax=ax,
                legend=True,
                cmap='YlGn',
                edgecolor='black',
                linewidth=0.5,
                zorder=3,
                legend_kwds={"label": "Taxa de Pessoas Pretas (Eleições 2024)", 
                             "orientation": "horizontal",
                             "pad": 0.05})

top_five = municipios[['NM_MUN', 'txCorRacaPreta']].nlargest(5, 'txCorRacaPreta').reset_index(drop=True)

top_text = "\n".join([f'{i+1}. {row['NM_MUN']} ({row['txCorRacaPreta']})' for i, row in top_five.iterrows()])
plt.text(-54, -28.75, top_text, fontsize=11, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.8))

plt.title('Taxa de Pessoas Pretas nas Eleições de 2024', fontsize=14, color='black', style='italic', loc='left')

plt.savefig("./sc_eleicoes_2024_pessoas_pretas.png")

# %%
from sklearn import cluster

# %%
X = municipios[['txGenFeminino', 'txCorRacaPreta']]
model = cluster.KMeans(n_clusters=6)
model.fit(X)

municipios['clusters'] = model.labels_

# %%
tx_extent = 0.005

fig, ax = plt.subplots(figsize = (9,9))
xlim = ([xmin*(1+tx_extent), xmax*(1-tx_extent)])
ylim = ([ymin*(1+tx_extent), ymax*(1-tx_extent)])

ax.set_xlim(xlim)
ax.set_ylim(ylim)

basemap = br_shp.plot(color='white',
                      ax=ax, 
                      edgecolor='black', 
                      linewidth=0.5,
                      zorder=2)

oceano.plot(ax=ax, color="#d4f1f4", zorder=1)

# https://github.com/geopandas/geopandas/issues/1269
# https://sashamaps.net/docs/resources/20-colors/
colors = {
    0: "#fabed4",
    1: "#ffd8b1",
    2: "#fffac8",
    3: "#aaffc3",
    4: "#dcbeff",
    5: "#42d4f4"
}

municipios.plot(column='clusters',
                ax=ax,
                edgecolor='black',
                linewidth=0.5,
                color=municipios['clusters'].map(colors),
                zorder=3)

plt.suptitle('Distribuição de Clusters\n', fontsize=14, color='black', style='italic', y=0.8075, x=0.25)
plt.title('Clusters criados a partir da taxa de mulheres e pessoas pretas nas eleições de 2024.', fontsize=8, color='black', loc='left')

# %%
municipios.explore(column='clusters', color=municipios['clusters'].map(colors))

# %%
# Mapa 4 - Valor médios dos bens declarados por candidato nas eleições 2024.
tx_extent = 0.005

fig, ax = plt.subplots(figsize = (9,9))
xlim = ([xmin*(1+tx_extent), xmax*(1-tx_extent)])
ylim = ([ymin*(1+tx_extent), ymax*(1-tx_extent)])

ax.set_xlim(xlim)
ax.set_ylim(ylim)

basemap = br_shp.plot(color='white',
                      ax=ax, 
                      edgecolor='black', 
                      zorder=2)

oceano.plot(ax=ax, color="#d4f1f4", zorder=1)

municipios.plot(column='mediaBensPorCand',
                ax=ax,
                legend=True,
                cmap='magma_r',
                edgecolor='black',
                linewidth=0.5,
                zorder=3,
                legend_kwds={"label": "Valor médio dos bens dos candidatos (Eleições 2024)", 
                             "orientation": "horizontal",
                             "pad": 0.05})

top_five = municipios[['NM_MUN', 'mediaBensPorCand']].nlargest(5, 'mediaBensPorCand').reset_index(drop=True)

top_text = "\n".join([f'{i+1} - {row['NM_MUN']} (R$ {row['mediaBensPorCand']:,.2f})'.replace(",", "!").replace(".", ",").replace("!", ".") for i, row in top_five.iterrows()])
plt.text(-54, -28.75, top_text, fontsize=11, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.8))

plt.text(-49.85, -29.425, 'linkedin.com/in/fernandobsouza', fontsize=9, alpha=0.4)

plt.title('Valor médio dos bens dos candidatos nas Eleições de 2024', fontsize=14, color='black', style='italic', loc='left')

# %%
# Mapa 5. Valor total dos bens declarados por candidato nas eleições 2024.
tx_extent = 0.005

fig, ax = plt.subplots(figsize = (9,9))
xlim = ([xmin*(1+tx_extent), xmax*(1-tx_extent)])
ylim = ([ymin*(1+tx_extent), ymax*(1-tx_extent)])

ax.set_xlim(xlim)
ax.set_ylim(ylim)

basemap = br_shp.plot(color='white',
                      ax=ax, 
                      edgecolor='black', 
                      zorder=2)

oceano.plot(ax=ax, color="#d4f1f4", zorder=1)

municipios.plot(column='somaTotalBens',
                ax=ax,
                legend=True,
                cmap='magma_r',
                edgecolor='black',
                linewidth=0.5,
                zorder=3,
                legend_kwds={"label": "Valor total dos bens dos candidatos (Eleições 2024)", 
                             "orientation": "horizontal",
                             "pad": 0.05})

top_five = municipios[['NM_MUN', 'somaTotalBens']].nlargest(5, 'somaTotalBens').reset_index(drop=True)

top_text = "\n".join([f'{i+1} - {row['NM_MUN']} (R$ {row['somaTotalBens']:,.2f})'.replace(",", "!").replace(".", ",").replace("!", ".") for i, row in top_five.iterrows()])
plt.text(-54, -28.70, top_text, fontsize=11, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.8))

plt.text(-49.85, -29.425, 'linkedin.com/in/fernandobsouza', fontsize=9, alpha=0.4)

plt.title('Valor total dos bens dos candidatos nas Eleições de 2024', fontsize=14, color='black', style='italic', loc='left')

# %%
# Histogramas... Valor total dos bens.
fig, ax = plt.subplots(figsize = (4,7))

ax.boxplot(municipios["somaTotalBens"])
ax.set_title('Distribuição dos bens dos candidatos\n por município (Eleições 2024).',
             fontsize=10, color='black', style='italic')

ax.set_ylabel('Somatório dos valores dos bens dos candidatos (R$)',
              fontsize=8)
ax.yaxis.grid(True)

# %%
# Histogramas... Valor médio dos bens.
fig, ax = plt.subplots(figsize = (4,7))

ax.boxplot(municipios["mediaBensPorCand"])
ax.set_title('Distribuição dos valores médios dos bens\ndos candidatos por município (Eleições 2024).',
             fontsize=10, color='black', style='italic')

ax.set_ylabel('Média dos valores dos bens dos candidatos (R$)',
              fontsize=8)
ax.yaxis.grid(True)

# %%
query2 = """SELECT SQ_CANDIDATO, NM_UE, DS_CARGO, SG_PARTIDO, DS_GENERO, DS_GRAU_INSTRUCAO, DS_ESTADO_CIVIL, DS_COR_RACA, DS_OCUPACAO FROM tb_candidaturas"""

df2 = pd.read_sql_query(query2, engine)
df2.head()

# %%
df2['DS_GRAU_INSTRUCAO'].unique()