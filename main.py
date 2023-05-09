import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#from simulacion_diario import Bodega
from simulacion_semanal import Bodega

np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter('sample_data.xlsx')

valores_politica = [(500,3000),(500,2500)]
replicas = 20
politica = "(s,S)"
#politica = "EOQ"

resultado = {}

print(f"\nESTADÍSTICAS SIMULACIÓN")
for valores in valores_politica:
    print(f"\nPOLÍTICA {valores}")
    resultado[str(valores)] = {}
    for i in range(0, replicas):
        s = Bodega(valores[0], valores[1], politica)
        s.run()
        s.guardar_datos(excel, str(valores))
        resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()
    df = pd.read_excel('sample_data.xlsx', engine='openpyxl')
    print(df.describe().transpose())
    print("\n")
    print("-"*20)
    print("\n")

# Se guardan kpi por repetición en excel
print(f"\nESTADÍSTICAS KPI")
for valores in valores_politica:
    print(f"\nPOLÍTICA {valores}")
    politica = resultado[str(valores)]
    rows = []
    for j in range(0, replicas):
        kpi = politica["repeticion"+str(j)]
        rows.append(list(kpi.values()))
    df = pd.DataFrame(rows, columns = list(kpi.keys()))   
    df.to_excel(excel, sheet_name='kpi'+str(valores), index=False)
    
    # Muestra el promedio de los kpi por política
    print(df.describe().transpose())
    print("-"*20)
    print("\n")
    
excel.save()
excel.close()
