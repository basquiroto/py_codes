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
                zorder=3,
                legend_kwds={"label": "Taxa de Mulheres (Eleições 2024)", 
                             "orientation": "horizontal",
                             "pad": 0.05})

top_five = municipios[['NM_MUN', 'txGenFeminino']].nlargest(5, 'txGenFeminino').reset_index(drop=True)

top_text = "\n".join([f'{i+1}. {row['NM_MUN']} ({row['txGenFeminino']})' for i, row in top_five.iterrows()])
plt.text(-54, -28.75, top_text, fontsize=11, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.8))

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
                      zorder=2)

oceano.plot(ax=ax, color="#d4f1f4", zorder=1)

municipios.plot(column='txCorRacaPreta',
                ax=ax,
                legend=True,
                cmap='YlGn',
                edgecolor='black',
                zorder=3,
                legend_kwds={"label": "Taxa de Pessoas Pretas (Eleições 2024)", 
                             "orientation": "horizontal",
                             "pad": 0.05})

top_five = municipios[['NM_MUN', 'txCorRacaPreta']].nlargest(5, 'txCorRacaPreta').reset_index(drop=True)

top_text = "\n".join([f'{i+1}. {row['NM_MUN']} ({row['txCorRacaPreta']})' for i, row in top_five.iterrows()])
plt.text(-54, -28.75, top_text, fontsize=11, verticalalignment='top', horizontalalignment='left', bbox=dict(facecolor='white', alpha=0.8))