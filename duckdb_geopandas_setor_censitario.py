# %% Importing libraries
import duckdb
import geopandas as gpd
from shapely import wkt
import matplotlib.pyplot as plt

# %% Testing sample data from the docs
r1 = duckdb.sql('SELECT 42 AS i')
duckdb.sql('SELECT i, i * 2 AS double_i FROM r1').show()

# %% Install spatial extension for duckdb
#duckdb.sql('INSTALL spatial')
duckdb.sql('LOAD spatial')

# %% Importing real data
# Sources: 
# IBGE. Malha de Setores Censitários. https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/26565-malhas-de-setores-censitarios-divisoes-intramunicipais.html
# GeoOne. Tutorial Download Dados IBGE. https://geoone.com.br/dados-setores-censitarios-ibge/

sc_shp = duckdb.sql('SELECT * FROM ST_Read(\'D:\\Users\\Fernando\\Downloads\\SC_Malha_Preliminar_2022.gpkg\')')
sc_excel = duckdb.sql('SELECT * FROM ST_Read(\'D:\\Users\\Fernando\\Downloads\\Base_informações_setores2010_sinopse_SC\\Base_informações_setores2010_sinopse_SC.xlsx\', open_options = [\'HEADERS=FORCE\'])')

# %% Reviewing column names
print('SHP: ', sc_shp.columns)
print('Excel: ', sc_excel.columns)

# %% What kind of data has those columns
print(sc_shp.df().sample())
print(sc_excel.df().sample())

# %% Preview of joining tables process
duckdb.sql("""
           SELECT shp.NM_MUN, shp.NM_DIST, 
           ex.Cod_setor, ex.V014 as pessoas_residentes, ex.V072 as mais_100_anos, shp.geom
           FROM sc_shp shp
           JOIN sc_excel ex ON left(shp.CD_SETOR, 15) = ex.Cod_setor
           LIMIT 10
           """)

# %% Join tables
db = duckdb.sql("""
           SELECT shp.NM_MUN, shp.NM_DIST,  
           ex.Cod_setor, ex.V014 as pessoas_residentes, ex.V072 as mais_100_anos, shp.geom
           FROM sc_shp shp
           JOIN sc_excel ex ON left(shp.CD_SETOR, 15) = ex.Cod_setor
           WHERE ex.V072 NOT IN ('X', '0')
           """)
           

# %% -- converting to pandas with .df() messes with geom types, so it is necessary to convert them to text
pd_df = duckdb.sql("""SELECT * EXCLUDE (geom), ST_AsTEXT(geom) as geom_text FROM db""").df()
pd_df.head()
# %%
pd_df['geom_text'] = gpd.GeoSeries.from_wkt(pd_df['geom_text'])
gdf = gpd.GeoDataFrame(pd_df, geometry = pd_df['geom_text'])

print(gdf.sample(5))
# %%
# https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html
sc = gpd.read_file('D:\\Users\\Fernando\\Downloads\\SC_Municipios_2022\\SC_Municipios_2022.shp')
estados = gpd.read_file('D:\\Users\\Fernando\\Downloads\\SC_Municipios_2022\\BR_UF_2022.shp')

# %%
fig, ax = plt.subplots()

estados.plot(ax=ax, color = '#FFFFE6', edgecolor='#EEEEEE', zorder=1)
sc.plot(ax=ax, color = '#FFFFCC', edgecolor='#CCCCCC', zorder=2)
gdf.plot(ax=ax, color='#FF0000', legend=True, zorder=3)
ax.set_xlim(-54.2, -48.2)
ax.set_ylim(-29.8, -25.8)

# %% 
duckdb.sql("""SELECT NM_MUN, count(*) as dist_mais_100 FROM db GROUP BY NM_MUN ORDER BY 2 DESC""")

# %% bbox of Florianópolis
duckdb.sql("""SELECT ST_XMAX(ST_Union_Agg(geom)) AS xmax,
           ST_YMAX(ST_Union_Agg(geom)) AS ymax,
           ST_XMIN(ST_Union_Agg(geom)) AS xmin,
           ST_YMIN(ST_Union_Agg(geom)) AS ymin FROM db WHERE NM_MUN = 'Florianópolis'""")
# %%
ax = sc.plot(color = 'white', edgecolor='gray')
ax.set_xlim(-48.7, -48.3)
ax.set_ylim(-27.9, -27.3)
gdf.plot(ax=ax, color='red')

# %%
