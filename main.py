
import numpy as np
import pandas as pd
import csv

from simulacion_diario import Bodega
from funciones import histogramas_png, generar_demanda
#from abrir_archivo import demanda
from guardar_data import guardar_pares_kpi, guardar_matriz_heatmap_kpi


np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter(
    'sample_data.xlsx',
    engine="xlsxwriter", 
    engine_kwargs={"options": {"strings_to_numbers": True}}
)

replicas = 1000
periodos = 30
politica = "(s,S)"
#politica = "EOQ"   

resultado = {}
resultado_base = {}

caso_base = True
no_mostro_grafico_base = True

rango_s_S = 51

# Demanda real
#print(demanda)

valores_politica = [(s, S) for s in range(rango_s_S) for S in range(rango_s_S) if s<=S]

# Demanda simulada
demanda = generar_demanda(periodos)

print(f"\nESTADÍSTICAS SIMULACIÓN")
for valores in valores_politica:
    muestra_grafico = True
    resultado[str(valores)] = {}
    #print(f"\nPOLÍTICA {valores}")
    for i in range(0, replicas):
        s = Bodega(
            s=valores[0],
            S=valores[1],
            politica=politica,
            periodos=periodos,
            demanda=demanda,
            precio_venta=6260,
            costo_pedido=4201,
            costo_almacenamiento=12,
            costo_demanda_perdida=1200,
            tiempo_revision=1, # Tieme que ser >= 1
            lead_time=7
        )
        s.run()
        
        if muestra_grafico:
            #s.grafico()
            muestra_grafico = False

        resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

# Se guardan kpi por repetición en excel
nombre_columna, data_excel = guardar_pares_kpi(valores_politica, resultado, replicas, excel)


# Se genera matriz por cada kpi en nueva hoja
guardar_matriz_heatmap_kpi(nombre_columna, rango_s_S, data_excel, excel)
    
excel.close()

# Guardo histogramas de kpi en carpetas
#histogramas_png(valores_politica, replicas)
