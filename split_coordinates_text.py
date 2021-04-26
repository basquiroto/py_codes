# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:24:23 2021

@author: Fernando Basquiroto de Souza

Conversão de coordenadas de textos (e.g. presentes em leis) para
data frames (possibilitando o uso em SIG)
"""
import re
import pandas as pd
import sys

# Texto exemplo da PL 292/2020 - Altera os limites do Parque Nacional da 
# Serra do Itajaí, localizado no Município de Botuverá, Estado de Santa Catarina.
# https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2237089

# Importando texto de arquivo
#with open(r'C:\Users\ferna\Desktop\texto.txt') as f:
#    texto = f.read()

# Texto exemplo
texto = '''ponto 1, de coordenadas planas aproximadas - c.p.a. E= 680.032 e 
N= 6.990.540, localizado no limite do Parque Nacional da Serra do Itajaí,
conforme disposto no Decreto de 4 de junho de 2004; deste, segue por linhas retas passando
pelo ponto 2, de c.p.a. E= 680.320 e N= 6.990.112, até atingir o ponto 3, de c.p.a. E= 680.049 e
N= 6.989.973, localizado na cota altimétrica de 122,3 metros (cento e vinte e dois metros e
trinta centímetros); deste, segue por linhas retas acompanhando a cota de 122,3 metros (cento
e vinte e dois metros e trinta centímetros), passando pelos seguintes pontos: ponto 4, de c.p.a.
E= 680.039 e N= 6.989.988, ponto 5, de c.p.a. E= 680.028 e N= 6.990.007, ponto 6, de c.p.a. E=
680.007 e N= 6.990.042, ponto 7, de c.p.a. E= 679.991 e N= 6.990.071, ponto 8, de c.p.a. E=
679.982 e N= 6.990.086, ponto 9, de c.p.a. E= 679.974 e N= 6.990.103, ponto 10, de c.p.a. E=
679.965 e N= 6.990.114,'''

# Extraindo longitude (E) e latitude (N)
# \d = Qualquer dígito; \s = Whitespace (https://docs.python.org/3/library/re.html)
# Exemplo para formato E= 698.034 e N= 6.980.760
e_raw = re.findall(r'E=\s[\d\.-]+[\d]', texto)
n_raw = re.findall(r'N=\s[\d\.-]+[\d\.-]+[\d]', texto)

# Exemplo para formato E= 698034 e N= 6980760
#e_raw = re.findall(r'E=\s\d\d\d\d\d\d', texto)
#n_raw = re.findall(r'N=\s\d\d\d\d\d\d\d', texto)

if len(e_raw) != len(n_raw):
    sys.exit('Erro na quantidade de coordenadas obtidas.')

# Removendo caracteres como letras e pontos
e_string = []; n_string = []

for i in range(len(e_raw)):
    e_string.append(e_raw[i].replace('E= ', '').replace('E=\n', '')\
                    .replace('.', ''))
        
    n_string.append(n_raw[i].replace('N= ', '').replace('N=\n', '')\
                    .replace('.', ''))

# Convertendo para número inteiro
e_int = list(map(int, e_string))
n_int = list(map(int, n_string))
coordenadas = [e_int, n_int]

# Salvando como dataframe do Pandas e em CSV para abrir no SIG
dt_coord = pd.DataFrame(coordenadas).transpose()
dt_coord.columns = ['E_UTM', 'N_UTM']
print(dt_coord.head(5))

dt_coord.to_csv(r'C:\Users\ferna\Desktop\Coordenadas.csv')
