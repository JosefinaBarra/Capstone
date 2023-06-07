import os
import numpy as np
import pandas as pd
import time

from simulacion_diario import Bodega
from abrir_archivo import demanda_real, valores_producto
from period_transicion import periodo_transicion
from guardar_data import guardar_pares_kpi, guardar_matriz_heatmap_kpi, guardar_3d, histogramas_kpi

start = time.perf_counter()
np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

tiempos_revision = [1]
productos = [885]
precios_producto = valores_producto(productos)

replicas = 1000
periodos = 365

rango_s_S = 51
valores_politica = [(s, S) for s in range(rango_s_S) for S in range(rango_s_S) if s<=S]


actual_path = os.getcwd()

for producto in productos:
    sale_price = precios_producto[str(producto)]['sale_price']
    final_price = precios_producto[str(producto)]['final_price']
    cost = precios_producto[str(producto)]['cost']
    storage = precios_producto[str(producto)]['storage']
    nombre = precios_producto[str(producto)]['nombre']

    folder = 'item_' + str(producto)
    dir = os.path.join(actual_path, folder)
    if not os.path.exists(dir):
        os.makedirs(dir)

    for tiempos in tiempos_revision:
        folder = 'item_' + str(producto)+'/T'+str(tiempos)

        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)

        excel = pd.ExcelWriter(
            os.path.join(actual_path, folder, 'data_'+str(tiempos)+'.xlsx'),
            engine="xlsxwriter", 
            engine_kwargs={"options": {"strings_to_numbers": True}}
        )

        resultado = {}
        resultado_base = {}

        caso_base = True
        no_mostro_grafico_base = True

        
        # BUSCAMOS ÓPTIMO PARA PARÁMETROS
        print(f"\nESTADÍSTICAS SIMULACIÓN")
        for valores in valores_politica:
            muestra_grafico = True
            resultado[str(valores)] = {}
            # print(f"\nPOLÍTICA {valores}")
            for i in range(0, replicas):
                s = Bodega(
                    s=valores[0],
                    S=valores[1],
                    periodos=periodos,
                    demanda=None,
                    precio_venta=sale_price,
                    costo_pedido=cost,
                    costo_almacenamiento=storage,
                    costo_demanda_perdida=1200,
                    tiempo_revision=tiempos,  # Tiene que ser >= 1
                    lead_time=7,
                    caso_base=False,
                    id_producto=producto,
                    nombre_producto=nombre
                )
                s.run()
                if no_mostro_grafico_base:
                    s.grafico()
                    no_mostro_grafico_base = False

                if muestra_grafico:
                    # s.grafico()
                    muestra_grafico = False

                resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

        # Se guardan kpi por repetición en excel
        nombre_columna, data_excel = guardar_pares_kpi(valores_politica, resultado, replicas, excel)


        # Se genera matriz por cada kpi en nueva hoja
        valores_matriz = guardar_matriz_heatmap_kpi(nombre_columna, rango_s_S, data_excel, excel, tiempos, producto, nombre)
        guardar_3d(valores_matriz, nombre_columna, tiempos, producto, nombre)
  
        excel.close()

        finish = time.perf_counter()

        print(f'Finished in {round(finish-start, 2)} second(s)')

        # Guardo histogramas de kpi en carpetas
        # histogramas_kpi(valores_politica, resultado, replicas, excel)
