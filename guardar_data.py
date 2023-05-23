import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def guardar_pares_kpi(valores_politica, resultado, replicas, excel):
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

    # KPI por columna y cada fila tiene pares (s,S)
    df2 = pd.DataFrame(data_excel).transpose()
    df2.columns = nombre_columna
    df2.to_excel(excel, sheet_name='Mean', index=True)

    return nombre_columna, data_excel

def guardar_matriz_heatmap_kpi(nombre_columna, rango_s_S, data_excel, excel):
    actual_path = os.getcwd()
    for kpi in range(0, len(nombre_columna)):
        matriz = []
        for i in range(rango_s_S):
            fila = []
            for j in range(rango_s_S):
                if i <= j:
                    tupla = "("+str(i)+", "+str(j)+")"
                    dato = data_excel[tupla][kpi]
                    fila.append(dato)
                else:
                    fila.append('0')
                fila_int = [float(x) for x in fila]
            matriz.append(fila_int)

        df3 = pd.DataFrame(matriz)
        df3.to_excel(excel, sheet_name="Mean-kpi"+str(kpi), index=True)

        fig, ax = plt.subplots()
        im = ax.imshow(matriz, cmap='GnBu')
        fig.colorbar(im, ax=ax)

        # Show all ticks and label them with the respective list entries
        ax.xaxis.tick_top()
        ax.set_xticks(np.arange(0, rango_s_S))
        ax.set_yticks(np.arange(0, rango_s_S))

        ax.set_title(str(nombre_columna[kpi]))
        fig.tight_layout()
        
        folder = 'graficos'
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/kpi'+str(kpi)+".png")
    