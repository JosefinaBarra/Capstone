# IMPORTS
import os
import pprint
import time

import numpy as np
import pandas as pd

from abrir_archivo import data_productos, demanda_historica
from guardar_data import (guardar_3d, guardar_kpi_repeticion,
                          guardar_matriz_heatmap_kpi, guardar_pares_kpi,
                          guardar_periodo_tran)
from parametros import *
from simulacion_diario import Bodega
from Ss_optimo import par_optimo

from abrir_archivo import demanda_historica, data_productos
from obtener_demanda import obtener_pronostico
from guardar_data import (
    guardar_pares_kpi, guardar_matriz_heatmap_kpi, guardar_3d,
    guardar_kpi_repeticion, guardar_periodo_tran
)

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

demanda_por_producto = {}
# Hago n replicas de la demanda por periodo
for producto in productos:
    demanda_por_sucursal = {}
    sucursales_producto = sucursales[producto]
    for sucursal in sucursales_producto.keys():
        # Se genera la demanda por repetición
        demanda_por_replica = {}
        for replica in range(0, replicas):
            demanda = {}
            for i in range(0, periodos):
                demanda_generada = np.random.poisson(sucursales_producto[sucursal])
                # Demanda en el día i
                demanda[i] = demanda_generada
            prom_demanda.append(np.mean(list(demanda.values())))

            # Demandas que se tienen por replica
            demanda_por_replica[replica] = demanda

        # Demanda en la sucursal
        demanda_por_sucursal[sucursal] = demanda_por_replica
    demanda_por_producto[producto] = demanda_por_sucursal

for producto in productos:
    print(f'\n--- PRODUCTO: {producto} ---\n')
    demanda_producto = demanda_por_producto[producto]
    sucursales_producto = sucursales[producto]
    for sucursal in sucursales_producto.keys():
        print(f'\n-- PRODUCTO: {producto} SUCURSAL: {sucursal} ---\n')
        demanda_sucursal = demanda_producto[sucursal]

        folder = str(producto)
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)

        excel = pd.ExcelWriter(
            folder + '/' + str(producto)+'sucursal_'+str(sucursal)+'.xlsx',
            engine="xlsxwriter",
            engine_kwargs={"options": {"strings_to_numbers": True}}
        )

        #DEFINIR PRONOSTICO DE LA DEMANDA AQUI

            # realizar pronóstico de dos períodos estando en día (t)
        # error: mse
        #print(self.item_id)
        #pronostico = obtener_demanda(self.sucursal, self.item_id)
        #print(pronostico)
        #if self.inventario[dia]  < (pronóstico_t+1 + error_t+1) + (pronóstico_t+2 + error_t+2):
        #if self.inventario[dia]  < (pronostico[0] + pronostico[2]) + (pronostico[1] + pronostico[2]):
            #pido pronostico_t+2 + error t+2
        #    return (pronostico[1] + pronostico[2])

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
                    tiempo_revision=1,  # Tiene que ser >= 1. =7 Se revisa una vez a la semana
                    lead_time=7,
                    caso_base=False,
                    sucursal=sucursal
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
            nombre_columna, rango_s_S, delta, data_excel, excel, nombre, item_id, sucursal, dif_s_S
        )
        print(f' Guardando gráfico 3D')
        guardar_3d(valores_matriz, nombre_columna, nombre, item_id, sucursal, rango_s_S, delta)

        excel.close()

        politica_elegida = par_optimo(producto, sucursal)
        print(f'\nPOLITICA ELEGIDA: {politica_elegida}')

        resultado = guardar_periodo_tran(resultado_bodega[politica_elegida], nombre, item_id, sucursal)

        guardar_kpi_repeticion(resultado, replicas, politica_elegida, producto, sucursal)

        excel.close()
end = time.time()
print("TOTAL ", end-start)
