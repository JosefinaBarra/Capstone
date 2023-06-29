import numpy as np
import pandas as pd
from obtener_demanda import obtener_pronostico
from pprint import pprint

# PARAMETROS
replicas = 5
periodos = 365
#politica = "(s, S)"
politica = "pronostico"
#politica = "poisson"

resultado_base = {}

# Se guardan los parámetros de lambda por producto y sucursal
parametros_lambda = pd.read_excel('data_productos/cuad13fil.xlsx')
sucursales = {}
for index, row in parametros_lambda.iterrows():
    item_id = int(row[0])
    branch = int(row[1])
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
if politica == "pronostico":
    delta = 5
    sucursal = 0
    pronostico = obtener_pronostico(sucursal, productos[0])
    print("pronostico", pronostico)
    S = (pronostico[1] + 50)
    S = np.ceil(S)
    print("S", S)
    valores_politica = [
        (s, S) for s in range(0, rango_s_S, delta) if s <= S
    ]
    #print("valores politica", valores_politica)
    valores_politica = np.array(valores_politica, 'i,i')

elif politica == "poisson":
    sucursales = {
        885: {
                0: {'l': 0.4000, 'x': 2},
                1:	{'l':0.9890, 'x':3},
                2:	{'l':2.1287, 'x':5},
                3:	{'l':1.4438, 'x':4},
                4:	{'l':6.0055, 'x':10},
                5:	{'l':3.9945, 'x':8},
                6:	{'l':1.1863, 'x':3},
                7:	{'l':3.3397, 'x':7},
                8:	{'l':0.9260, 'x': 3},
                9:	{'l':2.5890, 'x': 5},
                10:	{'l':4.4904, 'x': 8}
        }
    }
    valores_politica = [
        (s, S) for s in range(0, rango_s_S, delta) if s<=S 
    ]
        

