import numpy as np

replicas = 30
periodos = 365
politica = "pdi"

resultado_base = {}
#productos = [885, 1437]
productos = [162, 1163]
sucursal = 0


rango_s_S = 51
valores_politica = [
    (s, S) for s in range(0, rango_s_S, 5) for S in range(0, rango_s_S, 5) if s <= S
]
print(valores_politica)
valores_politica = np.array(valores_politica, 'i,i')
