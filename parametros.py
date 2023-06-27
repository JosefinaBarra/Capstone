import numpy as np
from obtener_demanda import obtener_pronostico

replicas = 30
periodos = 365
politica = "(s, S)"

resultado_base = {}
productos = [1024]
sucursal = 0

rango_s_S = 50
pronostico = obtener_pronostico(sucursal, productos[0])
print("pronostico", pronostico)
S = (pronostico[1] + 50)
print("S", S)
#rango_s_S = 20
valores_politica = [
    (s, S) for s in range(0, rango_s_S, 1) if s <= S
]
print("valores politica", valores_politica)
valores_politica = np.array(valores_politica, 'i,i')


#rango_s_S = 51

# valores_politica = [
#     (s, S) for s in range(0, rango_s_S, 5) for S in range(0, rango_s_S, 5) if s <= S
# ]

# print(valores_politica)
#valores_politica = np.array(valores_politica, 'i,i')
