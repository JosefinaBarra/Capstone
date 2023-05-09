import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

from simulacion_diario import Bodega
#from simulacion_semanal import Bodega

np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter('sample_data.xlsx')

valores_politica = [(0,5000), (500,3000),(500,2500)]
replicas = 100
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
    df = pd.read_excel('sample_data.xlsx', str(valores), engine='openpyxl')
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
    df.to_excel(excel, sheet_name='kpi'+str(valores), index=True)
    
    # Muestra el promedio de los kpi por política
    print(df.describe().transpose())
    print("-"*20)
    print("\n")
    
excel.save()
excel.close()


for valores in valores_politica:
    df = pd.read_excel('sample_data.xlsx', "kpi"+str(valores), engine='openpyxl')
    pdf = matplotlib.backends.backend_pdf.PdfPages("output" + str(valores) + ".pdf")

    for i in range(2, 13):
        fig, axes = plt.subplots(nrows=1, ncols=2)
        df.hist(column = df.columns[i], bins = 12, ax=axes[0])
        df.boxplot(column = df.columns[i], ax=axes[1])

        pdf.savefig(fig)
        
    pdf.close()