import numpy as np
import json

from simulacion import Bodega

np.random.seed(0)

valores_politica = [(100,1000), (150,1000)]
repeticiones = 30

resultado = {}
for valores in valores_politica:
    resultado["POLITICA " + str(valores)] = {}
    for i in range(1, repeticiones+1):
        s = Bodega(valores[0], valores[1])
        s.run()
        s.guardar_datos()
        resultado["POLÍTICA "+str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

print(json.dumps(resultado, indent=4))
