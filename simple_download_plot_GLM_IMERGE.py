# -*- coding: utf-8 -*-
"""
@author: Fernando Basquiroto de Souza

Para baixar do OpenDAP 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/', é necessário estar logado no site
https://urs.earthdata.nasa.gov e habilitar, no perfil, em Applications > Authorized Apps > Approve More Applicatons > 
Busque por NASA GESDISC DATA ARCHIVE e clique em Authorize. Em seguida, aceite os termos de uso (Agree).

Depois disso, crie no seu computador um arquivo chamado '.netrc' na pasta 'C:/Usuários/<SeuUsuário>/' com a seguinte linha: 
machine urs.earthdata.nasa.gov login <Usuário> password <Senha>
"""

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Download do Arquivo
urlname = 'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGDE.06/2000/06/'
file = '3B-DAY-E.MS.MRG.3IMERG.20000603-S000000-E235959.V06.nc4.nc4'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"}

import requests
result = requests.get(urlname+file, headers=header)
try:
    result.raise_for_status()
    f = open(file,'wb')
    f.write(result.content)
    f.close()
    print('Arquivos baixados: '+file)
except:
    print('requests.get() retornou o erro '+str(result.status_code))

# Abrindo arquivo netCDF4
fn = 'C:/Users/ferna/Desktop/'+file
ds = nc.Dataset(fn)

# Ajustando dados
prec = ds.variables['precipitationCal'][0,:,:]
prec = prec.transpose()
lats = ds.variables['lat'][:]
lons = ds.variables['lon'][:]
lons2d, lats2d = np.meshgrid(lons, lats)

# Plotando os dados
ax = plt.axes(projection=ccrs.PlateCarree())

plt.contourf(lons2d, lats2d, prec, 60,
             transform=ccrs.PlateCarree())

ax.coastlines()

plt.savefig('C:/Users/ferna/Desktop/figura_chuva.png', dpi = 320, bbox_inches = 'tight')
plt.show()