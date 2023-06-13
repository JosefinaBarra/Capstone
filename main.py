
import numpy as np
import pandas as pd
import json
import time
from simulacion_diario import Bodega
from abrir_archivo import demanda_historica, data_productos
from local_search import local_search
from calculos import (
    calcular_kpi, calcular_mean_kpi, calcular_min_kpi,
    calcular_max_kpi, matriz_kpi
)

start = time.time()
np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

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

rango_s_S = 51

# BUSCAMOS ÓPTIMO PARA PARÁMETROS
valores_politica = [
    (s, S) for s in range(0, rango_s_S, 5) for S in range(0, rango_s_S, 5) if s <= S
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

    class NpEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)

    with open("valores_kpi.json", "w") as file:
        json.dump(valores_kpi, file, cls=NpEncoder, indent=4)

    end = time.time()
    print("TOTAL ", end-start)
    # Se guardan kpi de simulaciones en archivo json
