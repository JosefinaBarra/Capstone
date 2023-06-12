
import numpy as np
import pandas as pd
import pprint
import time
from simulacion_diario import Bodega
from abrir_archivo import demanda_historica, data_productos
from guardar_data import (
    guardar_pares_kpi, guardar_matriz_heatmap_kpi, guardar_3d,
    guardar_kpi_repeticion
)
from local_search import local_search
from calculos import calcular_kpi, calcular_mean_kpi, calcular_min_kpi, calcular_max_kpi, matriz_kpi

start = time.time()
np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter(
    'sample_data.xlsx',
    engine="xlsxwriter",
    engine_kwargs={"options": {"strings_to_numbers": True}}
)

replicas = 1000
periodos = 365
politica = "(s,S)"

resultado_base = {}

demanda_real = demanda_historica()

productos = [885]
precios_productos = data_productos(productos)

demanda_simulacion = {}
prom_demanda = []
# Hago n replicas de la demanda por periodo
for replica in range(0, replicas):
    demanda = {}
    # Se genera la demanda por periodos
    for i in range(0, periodos):
        demanda_generada = np.random.poisson(3.825)
        demanda[i] = demanda_generada
    prom_demanda.append(np.mean(list(demanda.values())))
    demanda_simulacion[replica] = demanda 
prom_demanda = int(np.ceil(np.mean(prom_demanda)))

rango_s_S = 10*prom_demanda

# BUSCAMOS ÓPTIMO PARA PARÁMETROS
valores_politica = [
    (s, S) for s in range(rango_s_S) for S in range(rango_s_S) if s <= S
]
valores_politica = np.array(valores_politica,'i,i')

#valores_politica = [(35, 50)]
for producto in productos:
    resultado = {}
    resultado_bodega = {}
    nombre = precios_productos[producto]['nombre']
    item_id = precios_productos[producto]['id']

    # Se crea la matriz de valores política
    for valores in valores_politica:
        muestra_grafico = True
        resultado[str(valores)] = {}
        resultado_bodega[str(valores)] = []
        # print(f"\nPOLÍTICA {valores}")
        for i in range(0, replicas):
            s = Bodega(
                s=valores[0],
                S=valores[1],
                politica=politica,
                periodos=periodos,
                demanda=demanda_simulacion[i],
                info_producto=precios_productos[producto],
                tiempo_revision=1,  # Tieme que ser >= 1
                lead_time=7,
                caso_base=False
            )
            s.run()
            resultado_bodega[str(valores)].append(s)
            #resultado[str(valores)][i] = s.guardar_kpi()

    #pprint.pprint(resultado)
    valores_kpi = calcular_kpi(resultado_bodega, valores_politica)
    print("A")
    mean_kpi = calcular_mean_kpi(valores_kpi)
    print("B")
    min_kpi = calcular_min_kpi(valores_kpi)
    print("C")
    max_kpi = calcular_max_kpi(valores_kpi)
    print("D")
    matriz_kpi(mean_kpi)
    end = time.time()
    print("TOTAL ", end-start)   
    # Se guardan kpi por repetición en excel
    '''
    nombre_columna, data_excel = guardar_pares_kpi(
        valores_politica, resultado, replicas, excel
    )
    
    # Se genera matriz por cada kpi en nueva hoja
    valores_matriz = guardar_matriz_heatmap_kpi(
        nombre_columna, rango_s_S, data_excel, excel, nombre, item_id
    )
    local_search(valores_matriz, nombre_columna)

    guardar_3d(valores_matriz, nombre_columna, nombre, item_id)

    # Se guardan los kpi de la mejor política
    politica_elegida = input("Política: ")
    guardar_kpi_repeticion(resultado, replicas, politica_elegida, excel)

    excel.close()
    '''
