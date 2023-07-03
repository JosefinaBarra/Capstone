import json
import os
import pprint
from itertools import groupby

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from scipy.stats import poisson


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
            #kpi = resultado_kpi[str(j)]
            col.append(list(kpi.keys()))
            rows.append(list(kpi.values()))
        data = rows[:12] + rows[15:]

        df = pd.DataFrame(data, columns=list(kpi.keys()))
        #print(valores, df.describe())
        nombre_columna = list(df.columns.values)
        nombre_columna.pop(-1)

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
    df_mean = pd.DataFrame(data_excel).transpose()
    df_mean.columns = nombre_columna

    df_mean.to_excel(excel, sheet_name='Mean', index=True)

    df2 = pd.DataFrame(data_excel_min).transpose()
    df2.columns = nombre_columna
    df2.to_excel(excel, sheet_name='Min', index=True)

    df2 = pd.DataFrame(data_excel_max).transpose()
    df2.to_excel(excel, sheet_name='Max', index=True)

    df2 = pd.DataFrame(data_excel_std).transpose()
    df2.to_excel(excel, sheet_name='Std', index=True)

    return nombre_columna, data_excel


def guardar_matriz_heatmap_kpi(
        nombre_columna, rango_s_S, delta, data_excel, excel, nombre, item_id, sucursal, dif_s_S, leadtime, t_revision
):
    actual_path = os.getcwd()
    valores_matriz = []
    print("len(nombre_columna)", len(nombre_columna))
    for kpi in range(0, len(nombre_columna)):
        matriz = []
        for i in range(0, rango_s_S, delta):
            fila = []
            for j in range(0, rango_s_S, delta):
                if i <= j and j-i <= dif_s_S:
                    tupla = "("+str(i)+", "+str(j)+")"
                    dato = data_excel[tupla][kpi]
                    fila.append(dato)
                else:
                    fila.append('0')
                fila_int = [float(x) for x in fila]
        
        #for i in range(0, rango_s_S, 1): #5
        #    fila = []
        #    j = int(S)
        #    if i <= j:
        #        tupla = "("+str(i)+", "+str(j)+")"
        #        print("tupla - kpi", tupla, kpi)
        #        dato = data_excel[tupla][kpi]
        #        fila.append(dato)
        #    else:
        #        fila.append('0')
        #    fila_int = [float(x) for x in fila]
        
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
        x = [i for i in range(0, rango_s_S, delta)]
        default_x_ticks = range(len(matriz[0]))
        plt.xticks(default_x_ticks, x)
        plt.yticks(default_x_ticks, x)

        ax.set_xlabel("S")
        ax.set_ylabel("s")

        titulo = f'S:{sucursal} P:{item_id}: {nombre}\n {str(nombre_columna[kpi])}'
        ax.set_title(titulo)
        fig.tight_layout()

        folder = f'resultados/lead_time_{leadtime}_t_revision_{t_revision}/{item_id}/graficos/sucursal_{sucursal}'
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/kpi'+str(kpi)+".png")

        matriz = np.array(matriz,'f')
        valores_matriz.append(matriz)
    plt.close('all')
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


def guardar_3d(valores_matriz, nombre_columna, nombre, item_id, sucursal, rango_s_S, delta, leadtime, t_revision):
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

        x_values = [i for i in range(0, rango_s_S, delta)]
        default_x_ticks = range(len(x[0]))
        plt.xticks(default_x_ticks, x_values)
        plt.yticks(default_x_ticks, x_values)

        titulo = f'S:{sucursal} P:{item_id}: {nombre}\n {nombre_columna[i]}'
        ax.set_title(titulo)

        actual_path = os.getcwd()
        folder = f'resultados/lead_time_{leadtime}_t_revision_{t_revision}/{item_id}/graficos/sucursal_{sucursal}'

        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+'/3d_kpi_'+str(i)+".png")
        i += 1
    plt.close('all')


def guardar_kpi_repeticion(resultado, repeticiones, politica_elegida, producto, sucursal, leadtime, t_revision):
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
        kpi = resultado[repeticion]
        nivel_servicio.append(kpi["Nivel servicio [%]"])
        rotura_stock.append(kpi["Rotura de stock [%]"])
        total_pedidos.append(kpi["Total pedidos [unidades]"])
        total_ventas.append(kpi["Total ventas [unidades]"])
        total_sin_vender.append(kpi["Total sin vender [unidades]"])
        costo_pedidos.append(kpi["Costo pedidos [$]"])
        costo_almacenamiento.append(kpi["Costo almacenamiento [$]"])
        costo_demanda_insat.append(kpi["Costo demanda insatisfecha [$]"])
        costo_total.append(kpi["Costo total [$]"])
        dias_sin_stock.append(kpi["Cantidad dias sin stock [dias]"])
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

    path = f'resultados/lead_time_{leadtime}_t_revision_{t_revision}/{producto}/{producto}sucursal_{sucursal}_{politica_elegida}.xlsx'
    writer = pd.ExcelWriter(path, engine='openpyxl')
    df.to_excel(writer, sheet_name=politica_elegida, index=True)
    writer.close()


def guardar_periodo_tran(data, nombre, item_id, sucursal, leadtime, t_revision):
    inventario = []
    kpi_sim = {}

    for bodega in data:
        inventario.append(list(bodega.inventario.values()))

    inventario_prom = []
    # https://stackoverflow.com/questions/43436044/mean-value-of-each-element-in-multiple-lists-python
    inventario_prom = np.mean(np.vstack(inventario), axis=0).tolist()
    plt.plot(range(0, len(inventario_prom)), inventario_prom)
    #plt.show()

    max_inv = max(inventario_prom)
    print(max_inv)

    #periodo = int(input('Periodo transiente: '))
    periodo = 50
    fig = plt.figure()
    plt.plot(range(0, len(inventario_prom)), inventario_prom)
    plt.vlines(periodo, 0, max_inv, linestyles="dotted", colors="r")
    plt.text(periodo, max_inv-1,f'  t: {periodo}', color='r')
    titulo = f'S:{sucursal} P:{item_id}: {nombre}\nInventario promedio'
    plt.title(titulo)
    plt.xlabel('Días')
    plt.ylabel('Inventario promedio')

    actual_path = os.getcwd()
    folder = f'resultados/lead_time_{leadtime}_t_revision_{t_revision}/{item_id}/graficos/sucursal_{sucursal}'

    dir = os.path.join(actual_path, folder)
    if not os.path.exists(dir):
        os.makedirs(dir)
    fig.savefig(folder+'/inv_prom.png')

    for bodega in data:
        for i in range(periodo):
            bodega.inventario.pop(i)

    for i in range(0, len(data)):
        kpi_sim[i] = data[i].guardar_kpi()
    return kpi_sim

def parametros_lambda():
    df = pd.read_excel("data_productos/cuad13fil.xlsx")
    df = df.sort_values('lambda')
    
    df['lambda'] = df['lambda'] # demanda, pedidos por semana
    lambd = df['lambda']
    x = []  

    for i, row in df.iterrows():
        lambd = row['lambda']
        current_x = 0

        while poisson.sf(current_x, lambd) >  0.05:
            current_x += 1
        x.append(current_x)

    df['x'] = x
    df = df[df['x']>0]
    df = df.sort_values('lambda')
    
    df_885 = pd.read_csv('data_productos/lambdas885.txt', delimiter='\t')

    df1 = df_885[:11].reset_index()
    df1 = df1['Sucursal']
    df1 = df1.to_frame()

    df2 = df_885[12:].reset_index()
    df2 = df2['Sucursal']
    df2 = df2.to_frame()
    df2.rename(columns={'Sucursal': 'lambda'}, inplace=True)
    df2

    df_885 = pd.merge(df1, df2, left_index=True, right_index=True, how='inner')
    df_885['lambda'] = df_885['lambda'].astype(float)
    
    lambd = df_885['lambda']
    x = []  

    for i, row in df_885.iterrows():
        lambd = row['lambda']
        current_x = 0

        while poisson.sf(current_x, lambd) >  0.05:
            current_x += 1
        x.append(current_x)

    df_885['x'] = x
    
    print(df_885)
