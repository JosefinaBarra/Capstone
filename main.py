
import numpy as np
import pandas as pd
import json
import pprint
import time
from parametros import *
from simulacion_diario import Bodega
from abrir_archivo import demanda_historica, data_productos
from local_search import local_search
from obtener_demanda import obtener_pronostico
from calculos import (
    calcular_kpi, calcular_mean_kpi, calcular_min_kpi,
    calcular_max_kpi, matriz_kpi
)
from guardar_data import (
    guardar_pares_kpi, guardar_matriz_heatmap_kpi, guardar_3d,
    guardar_kpi_repeticion, guardar_periodo_tran
)

start = time.time()
np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

demanda_real = demanda_historica()

precios_productos = data_productos(productos)

demanda_simulacion = {}
prom_demanda = []
# Hago n replicas de la demanda por periodo
for replica in range(0, replicas):  #30
    demanda = {}
    # Se genera la demanda por periodos
    for i in range(0, periodos):  #7
        demanda_generada = np.random.poisson(3.825)
        demanda[i] = demanda_generada
    prom_demanda.append(np.mean(list(demanda.values())))

    demanda_simulacion[replica] = demanda

prom_demanda = int(np.ceil(np.mean(prom_demanda)))

for producto in productos:
    excel = pd.ExcelWriter(
        str(producto)+'.xlsx',
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
    print(precios_productos, "\n")

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
                tiempo_revision=7,  # Tieme que ser >= 1. =7 Se revisa una vez a la semana
                lead_time=7,
                caso_base=False,
                sucursal = sucursal
            )
            s.run()
            resultado_bodega[str(valores)].append(s)
            resultado[str(valores)][i] = s.guardar_kpi()

    # Se guardan kpi por repetición en excel
    nombre_columna, data_excel = guardar_pares_kpi(
        valores_politica, resultado, replicas, excel
    )

    # Se genera matriz por cada kpi en nueva hoja
    valores_matriz = guardar_matriz_heatmap_kpi(
        nombre_columna, rango_s_S, data_excel, excel, nombre, item_id
    )
    guardar_3d(valores_matriz, nombre_columna, nombre, item_id)

    s = input("s: ")
    S = input("S: ")
    politica_elegida = '('+s+', '+S+')'

    resultado = guardar_periodo_tran(resultado_bodega[politica_elegida])

    guardar_kpi_repeticion(resultado, replicas, politica_elegida, excel)

    excel.close()
    end = time.time()
    print("TOTAL ", end-start)

    '''
    #pprint.pprint(resultado)
    valores_kpi = calcular_kpi(resultado_bodega, valores_politica)
    mean_kpi = calcular_mean_kpi(valores_kpi)
    min_kpi = calcular_min_kpi(valores_kpi)
    max_kpi = calcular_max_kpi(valores_kpi)

    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    with open("valores_kpi_"+str(producto)+".json", "w") as file:
        json.dump(valores_kpi, file, cls=NpEncoder, indent=4)
    # Se guardan kpi de simulaciones en archivo json
    '''