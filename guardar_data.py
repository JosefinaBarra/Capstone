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
        resultado_kpi = resultado[str(valores)]
        rows = []
        col = []
        for j in range(0, replicas):
            kpi = resultado_kpi[j]
            col.append(list(kpi.keys()))
            rows.append(list(kpi.values()))
        data = rows[:12] + rows[15:]

        df = pd.DataFrame(data, columns=list(kpi.keys()))
        # df.to_excel(excel, sheet_name='kpi'+str(valores), index=True)
        nombre_columna = list(df.columns.values)
        nombre_columna = nombre_columna[:12] + nombre_columna[15:]
        columna_mean = []
        columna_min = []
        columna_max = []
        columna_std = []

        for i in range(0, len(nombre_columna)):
            mean_kpi = df[nombre_columna[i]].describe().loc[['mean']].tolist()
            min_kpi = df[nombre_columna[i]].describe().loc[['min']].tolist()
            max_kpi = df[nombre_columna[i]].describe().loc[['max']].tolist()
            std_kpi = df[nombre_columna[i]].describe().loc[['std']].tolist()

            mean_kpi = map(str, mean_kpi)
            min_kpi = map(str, min_kpi)
            max_kpi = map(str, max_kpi)
            std_kpi = map(str, std_kpi)

            columna_mean.append(str(''.join(mean_kpi)))
            columna_min.append(str(''.join(min_kpi)))
            columna_max.append(str(''.join(max_kpi)))
            columna_std.append(str(''.join(std_kpi)))

            data_excel[str(valores)] = columna_mean
            data_excel_min[str(valores)] = columna_min
            data_excel_max[str(valores)] = columna_max
            data_excel_std[str(valores)] = columna_std

    # KPI por columna y cada fila tiene pares (s,S)
    df2 = pd.DataFrame(data_excel).transpose()
    df2.columns = nombre_columna

    df2.to_excel(excel, sheet_name='Mean', index=True)

    df2 = pd.DataFrame(data_excel_min).transpose()
    df2.to_excel(excel, sheet_name='Min', index=True)

    df2 = pd.DataFrame(data_excel_max).transpose()
    df2.to_excel(excel, sheet_name='Max', index=True)

    df2 = pd.DataFrame(data_excel_std).transpose()
    df2.to_excel(excel, sheet_name='Std', index=True)

    return nombre_columna, data_excel


def guardar_matriz_heatmap_kpi(
        nombre_columna, rango_s_S, data_excel, excel, nombre, item_id
):
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
    (y, x) = np.meshgrid(
        np.arange(matrix.shape[1]), np.arange(matrix.shape[0])
    )

    fig = plt.figure()
    ax = fig.axes(projection='3d')

    surf = ax.plot_surface(x, y, matrix, **kwargs)
    return (fig, ax, surf)


def guardar_3d(valores_matriz, nombre_columna, nombre, item_id):
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

        titulo = f'{item_id}: {nombre}\n {nombre_columna[i]}'
        ax.set_title(titulo)

        actual_path = os.getcwd()
        folder = 'graficos'

        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/3d_kpi_'+str(i)+".png")
        i += 1


def guardar_kpi_repeticion(resultado, repeticiones, politica_elegida, excel):
    nivel_servicio = []
    rotura_stock = []
    total_pedidos = []
    costo_pedidos = []
    costo_almacenamiento = []
    dias_sin_stock = []
    total_sin_vender = []
    costo_demanda_insat = []
    costo_total = []
    total_ventas = []
    ingresos = []
    balance = []
    demanda = []
    ventas = []

    data = {}

    for repeticion in range(0, repeticiones):
        kpi = resultado[politica_elegida][repeticion]
        nivel_servicio.append(kpi["Nivel servicio [%]"])
        rotura_stock.append(kpi["Rotura de stock [%]"])
        total_pedidos.append(kpi["Total pedidos [unidades]"])
        costo_pedidos.append(kpi["Costo pedidos [$]"])
        costo_almacenamiento.append(kpi["Costo almacenamiento [$]"])
        dias_sin_stock.append(kpi["Cantidad dias sin stock [dias]"])
        total_sin_vender.append(kpi["Cantidad total sin vender [unidades]"])
        costo_demanda_insat.append(kpi["Costo demanda insatisfecha [$]"])
        costo_total.append(kpi["Costo total [$]"])
        total_ventas.append(kpi["Total ventas [unidades]"])
        ingresos.append(kpi["Ingresos por ventas [$]"])
        balance.append(kpi["Balance [$]"])
        demanda.append(kpi["Demanda"])
        ventas.append(kpi["Ventas"])

    data["Nivel servicio [%]"] = nivel_servicio
    data["Rotura de stock [%]"] = rotura_stock
    data["Total pedidos [unidades]"] = total_pedidos
    data["Costo pedidos [$]"] = costo_pedidos
    data["Costo almacenamiento [$]"] = costo_almacenamiento
    data["Cantidad dias sin stock [dias]"] = dias_sin_stock
    data["Cantidad total sin vender [unidades]"] = total_sin_vender
    data["Costo demanda insatisfecha [$]"] = costo_demanda_insat
    data["Costo total [$]"] = costo_total
    data["Total ventas [unidades]"] = total_ventas
    data["Ingresos por ventas [$]"] = ingresos
    data["Balance [$]"] = balance

    total_demanda = sum(demanda)
    total_ventas = sum(ventas)
    total_no_vendido = total_demanda - total_ventas
    print(f'Nivel servicio: {round((total_ventas/total_demanda)*100, 3)} %')
    print(f'Rotura stock: {round((total_no_vendido/total_demanda)*100, 3)} %')

    df = pd.DataFrame(data)
    df.to_excel(excel, sheet_name=politica_elegida, index=True)
