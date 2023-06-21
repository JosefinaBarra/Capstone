import numpy as np

replicas = 30
periodos = 365
politica = "(s,S)"

resultado_base = {}
productos = [885]

rango_s_S = 51
delta = 5
valores_politica = [
    (s, S) for s in range(0, rango_s_S, delta) for S in range(0, rango_s_S, delta) if s <= S
]
#print(valores_politica)
valores_politica = np.array(valores_politica, 'i,i')
