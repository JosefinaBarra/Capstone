import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from simulacion_diario import Bodega
#from simulacion_semanal import Bodega

np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter('sample_data.xlsx')

valores_politica = [(500,3000)]
replicas = 20
politica = "(s,S)"
#politica = "EOQ"

resultado = {}
for valores in valores_politica:
    resultado[str(valores)] = {}
    for i in range(0, replicas):
        s = Bodega(valores[0], valores[1], politica)
        s.run()
        s.guardar_datos(excel, str(valores))
        resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

    print(f"{valores} - Estadísticas simulación")
    df = pd.read_excel('sample_data.xlsx', engine='openpyxl')
    print(df.describe().transpose())
    print("\n")

# Se guardan kpi por repetición en excel
for i in range(0, len(valores_politica)):
    politica = resultado[str(valores_politica[i])]
    rows = []
    for j in range(0, replicas):
        kpi = politica["repeticion"+str(j)]
        rows.append(list(kpi.values()))
    df = pd.DataFrame(rows, columns = list(kpi.keys()))   
    df.to_excel(excel, sheet_name='kpi'+str(valores_politica[i]), index=False)
    
    # Muestra el promedio de los kpi por política
    print(f"{valores_politica[i]} - Estadísticas KPI")
    print(df.describe().transpose())
excel.save()
excel.close()
