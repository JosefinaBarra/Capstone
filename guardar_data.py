import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def guardar_pares_kpi(valores_politica, resultado, replicas, excel):
    data_excel = {}
    data_excel_min = {}
    data_excel_max = {}
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
        columna_mean = []
        columna_min = []
        columna_max = []

        for i in range(0, len(nombre_columna)):
            valores_kpi_mean = df[nombre_columna[i]].describe().loc[['mean']].tolist()
            valores_kpi_min = df[nombre_columna[i]].describe().loc[['min']].tolist()
            valores_kpi_max = df[nombre_columna[i]].describe().loc[['max']].tolist()

            valores_kpi_mean = map(str,valores_kpi_mean)
            valores_kpi_min = map(str,valores_kpi_min)
            valores_kpi_max = map(str,valores_kpi_max)

            columna_mean.append(str(''.join(valores_kpi_mean)))
            columna_min.append(str(''.join(valores_kpi_min)))
            columna_max.append(str(''.join(valores_kpi_max)))

            data_excel[str(valores)] = columna_mean
            data_excel_min[str(valores)] = columna_min
            data_excel_max[str(valores)] = columna_max

        #df.describe().loc[['mean','min','max']].to_excel(excel, sheet_name='kpi'+str(valores), index=True)

    # KPI por columna y cada fila tiene pares (s,S)
    df2 = pd.DataFrame(data_excel).transpose()
    df2.columns = nombre_columna
    df2.to_excel(excel, sheet_name='Mean', index=True)

    df2 = pd.DataFrame(data_excel_min).transpose()
    df2.columns = nombre_columna
    df2.to_excel(excel, sheet_name='Min', index=True)

    df2 = pd.DataFrame(data_excel_max).transpose()
    df2.columns = nombre_columna
    df2.to_excel(excel, sheet_name='Max', index=True)

    return nombre_columna, data_excel

def guardar_matriz_heatmap_kpi(nombre_columna, rango_s_S, data_excel, excel, nombre, item_id):
    actual_path = os.getcwd()
    valores_matriz = []
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
        im = ax.imshow(matriz, cmap='GnBu', aspect='auto')
        ax.set_aspect('auto')
        ax.axis('scaled')

        fig.colorbar(im, ax=ax)

        # Show all ticks and label them with the respective list entries
        ax.xaxis.tick_top()
        ax.set_xticks(np.arange(0, rango_s_S, 10))
        ax.set_yticks(np.arange(0, rango_s_S, 10))

        ax.set_xlabel("S")
        ax.set_ylabel("s")

        titulo = f'{item_id}: {nombre}\n {str(nombre_columna[kpi])}'
        ax.set_title(titulo)
        fig.tight_layout()

        folder = 'graficos'
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/kpi'+str(kpi)+".png")

        valores_matriz.append(matriz)

    return valores_matriz

# https://gist.github.com/CMCDragonkai/dd420c0800cba33142505eff5a7d2589
def surface_plot(matrix, **kwargs):
    # acquire the cartesian coordinate matrices from the matrix
    # x is rows, y is cols
    (y, x) = np.meshgrid(np.arange(matrix.shape[1]), np.arange(matrix.shape[0]))

    fig = plt.figure()
    ax = fig.axes(projection='3d')

    surf = ax.plot_surface(x, y, matrix, **kwargs)
    return (fig, ax, surf)


def guardar_3d(valores_matriz, nombre_columna, nombre, item_id):
    i = 0
    mycmap = plt.get_cmap('gist_earth')

    for matriz_kpi in valores_matriz:
        z = np.array(matriz_kpi)

        (y, x) = np.meshgrid(np.arange(z.shape[1]), np.arange(z.shape[0]))

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter(x,y,z, s = 5)

        ax.set_xlabel('s')
        ax.set_ylabel('S')
        ax.set_zlabel('z')

        titulo = f'{item_id}: {nombre}\n {nombre_columna[i]}'
        ax.set_title(titulo)

        actual_path = os.getcwd()
        folder = 'graficos'

        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/3d_kpi_'+str(i)+".png")
        i += 1
