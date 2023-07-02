# IMPORTS
import os
import pprint
import time
import shutil

import numpy as np
import pandas as pd

from abrir_archivo import data_productos
from guardar_data import (guardar_3d, guardar_kpi_repeticion,
                          guardar_matriz_heatmap_kpi, guardar_pares_kpi,
                          guardar_periodo_tran)
from parametros import *
from simulacion_diario import Bodega
from Ss_optimo import par_optimo

from guardar_data import (
    guardar_pares_kpi, guardar_matriz_heatmap_kpi, guardar_3d,
    guardar_kpi_repeticion, guardar_periodo_tran
)

start = time.time()
np.random.seed(0)

actual_path = os.getcwd()

pd.set_option('display.float_format', lambda x: '%.3f' % x)

precios_productos = data_productos(productos)
print('VALORES PRODUCTOS')

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
                if politica == "poisson":
                    lambd = sucursales_producto[sucursal]['l']
                else:
                    lambd = sucursales_producto[sucursal]
                demanda_generada = np.random.poisson(lambd)
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
        if sucursal == 4:
            print(f'\n-- PRODUCTO: {producto} SUCURSAL: {sucursal} ---\n')
            demanda_sucursal = demanda_producto[sucursal]

            folder = f'resultados/B5_lead_time_{leadtime}_t_revision_{t_revision}/{producto}'
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
                #print(f"\nPOLÍTICA {valores_politica[j]}")
                for i in range(0, replicas):
                    if politica == 'pronostico':
                        shutil.copy(
                            f"pronostico_demanda/excel_branches/branch{sucursal}.xlsx", f"pronostico_demanda/excel_branches/branch{sucursal}(1).xlsx"
                        )

                    s = Bodega(
                        s=valores_politica[j][0],
                        S=valores_politica[j][1],
                        politica=politica,
                        periodos=periodos,
                        demanda=demanda_sucursal[i],
                        info_producto=precios_productos[producto],
                        tiempo_revision=t_revision,  # Tiene que ser >= 1. =7 Se revisa una vez a la semana
                        lead_time=leadtime,
                        t_revision=t_revision,
                        caso_base=False,
                        sucursal=sucursal,
                        parametro_l = sucursales[producto][sucursal]
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
            excel.close()
            print(f' Guardando gráfico heatmap')
            # Se genera matriz por cada kpi en nueva hoja
            valores_matriz = guardar_matriz_heatmap_kpi(
                nombre_columna, rango_s_S, delta, data_excel, excel, nombre, item_id, sucursal, dif_s_S, leadtime, t_revision
            )
            print(f' Guardando gráfico 3D')
            guardar_3d(valores_matriz, nombre_columna, nombre, item_id, sucursal, rango_s_S, delta, leadtime, t_revision)

            

            politica_elegida = par_optimo(producto, sucursal, leadtime, t_revision, valor_balance, valor_nivel_servicio)
            if politica_elegida != 'error':
                print(f'\nPOLITICA ELEGIDA: {politica_elegida}')

                resultado = guardar_periodo_tran(resultado_bodega[politica_elegida], nombre, item_id, sucursal, leadtime, t_revision)

                guardar_kpi_repeticion(resultado, replicas, politica_elegida, producto, sucursal, leadtime, t_revision)

                excel.close()
end = time.time()
print("TOTAL ", end-start)
