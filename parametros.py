import numpy as np
import pandas as pd
from obtener_demanda import obtener_pronostico
from pprint import pprint

# PARAMETROS
replicas = 40
periodos = 365
politica = "(s, S)"
#politica = "pronostico"

resultado_base = {}

# Se guardan los parámetros de lambda por producto y sucursal
parametros_lambda = pd.read_excel('outputdpsde115.xlsx')
sucursales = {}
for index, row in parametros_lambda.iterrows():
    item_id = row[0]
    branch = row[1]
    parametro = row[2]
    
    if item_id not in sucursales:
        sucursales[item_id] = {}
    
    if branch not in sucursales[item_id]:
        sucursales[item_id][branch] = parametro

productos = list(sucursales.keys())

delta = 5
rango_s_S = 101
dif_s_S = 20
valores_politica = [
    (s, S) for s in range(0, rango_s_S, delta) for S in range(0, rango_s_S, delta) if s <= S if S-s <= dif_s_S
]
sucursal = 0
if politica == "pronostico":
    delta = 1
    pronostico = obtener_pronostico(sucursal, productos[0])
    print("pronostico", pronostico)
    S = (pronostico[1] + 50)
    S = np.ceil(S)
    print("S", S)
    valores_politica = [
        (s, S) for s in range(0, rango_s_S, delta) if s <= S
    ]
    print("valores politica", valores_politica)
    valores_politica = np.array(valores_politica, 'i,i')
