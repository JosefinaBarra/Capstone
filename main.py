
import numpy as np
import pandas as pd
import csv

from simulacion_diario import Bodega
from funciones import histogramas_png, generar_demanda
#from abrir_archivo import demanda


np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter(
    'sample_data.xlsx',
    engine="xlsxwriter", 
    engine_kwargs={"options": {"strings_to_numbers": True}}
)

replicas = 1000
periodos = 30
politica = "(s,S)"
#politica = "EOQ"   

resultado = {}
resultado_base = {}

caso_base = True
no_mostro_grafico_base = True

# Demanda real
#print(demanda)

valores_politica = [(s, S) for s in range(51) for S in range(51) if s<=S]

# Demanda simulada
demanda = generar_demanda(periodos)

print(f"\nESTADÍSTICAS SIMULACIÓN")
for valores in valores_politica:
    muestra_grafico = True
    resultado[str(valores)] = {}
    #print(f"\nPOLÍTICA {valores}")
    for i in range(0, replicas):
        s = Bodega(
            s=valores[0],
            S=valores[1],
            politica=politica,
            periodos=periodos,
            demanda=demanda,
            precio_venta=6260,
            costo_pedido=4201,
            costo_almacenamiento=12,
            costo_demanda_perdida=6260,
            tiempo_revision=1, # Tieme que ser >= 1
            lead_time=7
        )
        s.run()
        
        if muestra_grafico:
            #s.grafico()
            muestra_grafico = False

        resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

# Se guardan kpi por repetición en excel
data_excel = {}
for valores in valores_politica:
    #print(f"\nPOLÍTICA {valores}")
    resultado_kpi = resultado[str(valores)]
    rows = []
    for j in range(0, replicas):
        kpi = resultado_kpi["repeticion"+str(j)]
        rows.append(list(kpi.values()))
    
    df = pd.DataFrame(rows, columns = list(kpi.keys()))
    #df.to_excel(excel, sheet_name='kpi'+str(valores), index=True)

    nombre_columna = list(df.columns.values)
    columna = []
    for i in range(0, len(nombre_columna)):
        valores_kpi = df[nombre_columna[i]].describe().loc[['mean']].tolist()
        valores_kpi = map(str,valores_kpi)
        columna.append(str(''.join(valores_kpi)))
        data_excel[str(valores)] = columna

    #df.describe().loc[['mean','min','max']].to_excel(excel, sheet_name='kpi'+str(valores), index=True)


df2 = pd.DataFrame(data_excel).transpose()
df2.columns = nombre_columna
df2.to_excel(excel, sheet_name='Mean', index=True)

for kpi in range(0, len(nombre_columna)):
    matriz = []
    for i in range(51):
        fila = []
        for j in range(51):
            if i <= j:
                tupla = "("+str(i)+", "+str(j)+")"
                dato = data_excel[tupla][kpi]
                fila.append(dato)
            else:
                fila.append(0)
        matriz.append(fila)

    df3 = pd.DataFrame(matriz)
    df3.to_excel(excel, sheet_name="Mean-kpi"+str(kpi), index=True)
    
excel.close()

# Guardo histogramas de kpi en carpetas
#histogramas_png(valores_politica, replicas)
