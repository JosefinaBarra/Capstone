import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def guardar_pares_kpi(valores_politica, resultado, replicas, excel):
    data_excel = {}
    data_excel_min = {}
    data_excel_max = {}
    data_excel_std = {}
    for valores in valores_politica:
        # print(f"\nPOLÍTICA {valores}")
        resultado_kpi = resultado[str(valores)]
        rows = []
        for j in range(0, replicas):
            kpi = resultado_kpi["repeticion"+str(j)]
            rows.append(list(kpi.values()))

        df = pd.DataFrame(rows, columns=list(kpi.keys()))
        # df.to_excel(excel, sheet_name='kpi'+str(valores), index=True)

        nombre_columna = list(df.columns.values)
        columna_mean = []
        columna_min = []
        columna_max = []
        columna_std = []

        demanda_total = sum(list(df[nombre_columna[0]]))
        total_vendido = sum(list(df[nombre_columna[1]]))
        nivel_servicio = np.round((total_vendido/demanda_total)*100, 3)
        quiebre_stock = np.round(
            ((demanda_total-total_vendido)/demanda_total)*100, 3
        )

        for i in range(3, len(nombre_columna)):
            # print(nombre_columna[i], df[nombre_columna[i]].describe().loc[['mean']].tolist())
            columna = df[nombre_columna[i]]
            valores_kpi_mean = columna.describe().loc[['mean']].tolist()
            valores_kpi_min = columna.describe().loc[['min']].tolist()
            valores_kpi_max = columna.describe().loc[['max']].tolist()
            valores_kpi_std = columna.describe().loc[['std']].tolist()

            valores_kpi_mean = map(str, valores_kpi_mean)
            valores_kpi_min = map(str, valores_kpi_min)
            valores_kpi_max = map(str, valores_kpi_max)
            valores_kpi_std = map(str, valores_kpi_std)

            columna_mean.append(str(''.join(valores_kpi_mean)))
            columna_min.append(str(''.join(valores_kpi_min)))
            columna_max.append(str(''.join(valores_kpi_max)))
            columna_std.append(str(''.join(valores_kpi_std)))

            data_excel[str(valores)] = columna_mean
            data_excel_min[str(valores)] = columna_min
            data_excel_max[str(valores)] = columna_max
            data_excel_std[str(valores)] = columna_std

        # Se agrega dato de nivel de servicio al par (s,S)
        data_excel[str(valores)].append(nivel_servicio)
        data_excel[str(valores)].append(quiebre_stock)

    # KPI por columna y cada fila tiene pares (s,S)
    df2 = pd.DataFrame(data_excel).transpose()
    columnas = nombre_columna[3:]
    columnas.append("Nivel de servicio [%]")
    columnas.append("Quiebre de stock [%]")
    df2.columns = columnas
    df2.to_excel(excel, sheet_name='Mean', index=True)

    df2 = pd.DataFrame(data_excel_min).transpose()
    df2.columns = nombre_columna[3:]
    df2.to_excel(excel, sheet_name='Min', index=True)

    df2 = pd.DataFrame(data_excel_max).transpose()
    df2.to_excel(excel, sheet_name='Max', index=True)

    df2 = pd.DataFrame(data_excel_std).transpose()
    df2.to_excel(excel, sheet_name='Std', index=True)

    nombre_columna = nombre_columna[3:]
    nombre_columna.append("Nivel de servicio [%]")
    nombre_columna.append("Quiebre de stock [%]")

    return nombre_columna, data_excel


def guardar_matriz_heatmap_kpi(
        nombre_columna, rango_s_S, data_excel, excel, tiempos, producto, nombre
):
    actual_path = os.getcwd()
    valores_matriz = []
    for kpi in range(0, len(data_excel['(0, 0)'])):
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
        ax.set_xticks(np.arange(0, rango_s_S))
        ax.set_yticks(np.arange(0, rango_s_S))

        ax.set_xlabel("S")
        ax.set_ylabel("s")

        titulo = f'Producto {producto}: {nombre} \n {nombre_columna[kpi]}\n'
        ax.set_title(titulo)
        fig.tight_layout()

        folder = 'item_' + str(producto)+'/T'+str(tiempos)+'/graficos'
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/kpi'+str(kpi)+".png")

        valores_matriz.append(matriz)
    plt.close('all')
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


def guardar_3d(valores_matriz, nombre_columna, tiempos, producto, nombre):
    i = 0

    for matriz_kpi in valores_matriz:
        z = np.array(matriz_kpi)

        (y, x) = np.meshgrid(np.arange(z.shape[1]), np.arange(z.shape[0]))

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter(x, y, z, s=5)

        ax.set_xlabel('s')
        ax.set_ylabel('S')
        ax.set_zlabel('z')

        titulo = f'Producto {producto}: {nombre} \n {nombre_columna[i]}\n'
        ax.set_title(titulo)

        actual_path = os.getcwd()
        folder = 'item_' + str(producto)+'/T'+str(tiempos)+'/graficos'

        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/3d_kpi_'+str(i)+".png")
        i += 1
    plt.close('all')


def histogramas_kpi(valores_politica, resultado, replicas, excel):
    pass
