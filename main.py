import json

import numpy as np
import pandas as pd

from simulacion import Bodega

np.random.seed(0)
excel = pd.ExcelWriter('sample_data.xlsx')

valores_politica = [(60,2000), (70,2000), (60,1000), (70,1000)]
replicas = 30

resultado = {}
for valores in valores_politica:
    resultado[str(valores)] = {}
    for i in range(0, replicas):
        s = Bodega(valores[0], valores[1])
        s.run()
        s.guardar_datos(excel, str(valores))
        resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

#print(json.dumps(resultado, indent=4))
#print("\n")

# Se guardan kpi por repetición en excel

for i in range(0, len(valores_politica)):
    politica = resultado[str(valores_politica[i])]
    rows = []
    for j in range(0, replicas):
        kpi = politica["repeticion"+str(j)]
        rows.append(list(kpi.values()))

    df = pd.DataFrame(rows, columns = list(kpi.keys()))   
    df.to_excel(excel, sheet_name='kpi'+str(valores_politica[i]), index=True)
    print(valores_politica[i])
    print(df.mean())
    print("\n")
excel.save()
excel.close()

