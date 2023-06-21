# IMPORTS
import json
import os
import pprint
import time

import numpy as np
import pandas as pd
from tqdm import tqdm

from abrir_archivo import data_productos, demanda_historica
from calculos import (calcular_kpi, calcular_max_kpi, calcular_mean_kpi,
                      calcular_min_kpi, matriz_kpi)
from guardar_data import (guardar_3d, guardar_kpi_repeticion,
                          guardar_matriz_heatmap_kpi, guardar_pares_kpi,
                          guardar_periodo_tran)
from parametros import *
from simulacion_diario import Bodega
from Ss_optimo import par_optimo


start = time.time()
np.random.seed(0)

actual_path = os.getcwd()

pd.set_option('display.float_format', lambda x: '%.3f' % x)

demanda_real = demanda_historica()

precios_productos = data_productos(productos)
print('VALORES PRODUCTOS')
pprint.pprint(precios_productos)

prom_demanda = []
#prom_demanda = int(np.ceil(np.mean(prom_demanda)))

sucursales = {
    0: 1.1222,
    1: 0.5722,
    2: 1.4722,
    3: 1.4388,
    4: 3.825,
    5: 3.4666,
    6: 1.0611,
    7: 3.8555,
    8: 0.8833,
    9: 2.6833,
    10: 5.288
}

demanda_por_sucursal = {}
# Hago n replicas de la demanda por periodo
for sucursal in range(0, len(sucursales.keys())):
    # Se genera la demanda por repetición
    demanda_por_replica = {}
    for replica in range(0, replicas):
        demanda = {}
        for i in range(0, periodos):
            demanda_generada = np.random.poisson(sucursales[sucursal])
            # Demanda en el día i
            demanda[i] = demanda_generada
        prom_demanda.append(np.mean(list(demanda.values())))

        # Demandas que se tienen por replica
        demanda_por_replica[replica] = demanda

    # Demanda en la sucursal
    demanda_por_sucursal[sucursal] = demanda_por_replica

for producto in productos:
    print(f'--- PRODUCTO: {producto} ---')
    for sucursal in range(0, len(sucursales.keys())):
        print(f'-- SUCURSAL: {sucursal} ---')
        demanda_sucursal = demanda_por_sucursal[sucursal]

        folder = str(producto)
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)

        excel = pd.ExcelWriter(
            folder + '/' + str(producto)+'sucursal_'+str(sucursal)+'.xlsx',
            engine="xlsxwriter",
            engine_kwargs={"options": {"strings_to_numbers": True}}
        )

        resultado = {}
        resultado_bodega = {}
        nombre = precios_productos[producto]['nombre']
        item_id = precios_productos[producto]['id']
        #print(precios_productos, "\n")

        # Se crea la matriz de valores política
        for j in range(0, len(valores_politica)):
            muestra_grafico = True
            resultado[str(valores_politica[j])] = {}
            resultado_bodega[str(valores_politica[j])] = []
            # print(f"\nPOLÍTICA {valores}")
            for i in range(0, replicas):
                s = Bodega(
                    s=valores_politica[j][0],
                    S=valores_politica[j][1],
                    politica=politica,
                    periodos=periodos,
                    demanda=demanda_sucursal[i],
                    info_producto=precios_productos[producto],
                    tiempo_revision=1,  # Tieme que ser >= 1
                    lead_time=7,
                    caso_base=False
                )
                s.run()
                resultado_bodega[str(valores_politica[j])].append(s)
                resultado[str(valores_politica[j])][i] = s.guardar_kpi()
        print(f' Termina for valores politica')
        # Se guardan kpi por repetición en excel
        print(f' Guardando excel por pares')
        nombre_columna, data_excel = guardar_pares_kpi(
            valores_politica, resultado, replicas, excel
        )
        print(f' Guardando gráfico heatmap')
        # Se genera matriz por cada kpi en nueva hoja
        valores_matriz = guardar_matriz_heatmap_kpi(
            nombre_columna, rango_s_S, delta, data_excel, excel, nombre, item_id, sucursal
        )
        print(f' Guardando gráfico 3D')
        guardar_3d(valores_matriz, nombre_columna, nombre, item_id, sucursal, rango_s_S, delta)

        excel.close()

        politica_elegida = par_optimo(producto, sucursal)
        print(f'\nPOLITICA ELEGIDA: {politica_elegida}')

        resultado = guardar_periodo_tran(resultado_bodega[politica_elegida], nombre, item_id, sucursal)

        guardar_kpi_repeticion(resultado, replicas, politica_elegida, producto, sucursal)

    end = time.time()
    print("TOTAL ", end-start)
