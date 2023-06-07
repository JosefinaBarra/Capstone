
import numpy as np
import pandas as pd

from simulacion_diario import Bodega
from abrir_archivo import demanda_historica, data_productos
from guardar_data import guardar_pares_kpi, guardar_matriz_heatmap_kpi, guardar_3d


np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter(
    'sample_data.xlsx',
    engine="xlsxwriter", 
    engine_kwargs={"options": {"strings_to_numbers": True}}
)

replicas = 10
periodos = 80
politica = "(s,S)"
#politica = "EOQ"   

resultado = {}
resultado_base = {}

caso_base = True
no_mostro_grafico_base = True

rango_s_S = 5
demanda_real = demanda_historica()

productos = [885]
precios_productos = data_productos(productos)

# SE OBTIENEN PARÁMETROS DEL CASO BASE USANDO DEMANDA HISTÓRICA
# Demanda real
'''
s = Bodega(
        s=np.ceil(np.mean(list(demanda_real.values()))/2),
        S=np.ceil(np.mean(list(demanda_real.values()))*2),
        politica=politica,
        periodos=periodos,
        demanda=demanda_real,
        precio_venta=6260,
        costo_pedido=4201,
        costo_almacenamiento=12,
        costo_demanda_perdida=1200,
        tiempo_revision=1, # Tiene que ser >= 1
        lead_time=7,
        caso_base=True
    )
s.run()
s.grafico()
print(s.guardar_kpi())
'''

# BUSCAMOS ÓPTIMO PARA PARÁMETROS
valores_politica = [(s, S) for s in range(rango_s_S) for S in range(rango_s_S) if s<=S]

for producto in productos:
    nombre = precios_productos[producto]['nombre']
    sale_price = precios_productos[producto]['sale_price']
    final_price = precios_productos[producto]['final_price']
    cost = precios_productos[producto]['cost']
    storage_cost = precios_productos[producto]['storage_cost']
    for valores in valores_politica:
        muestra_grafico = True
        resultado[str(valores)] = {}
        # print(f"\nPOLÍTICA {valores}")
        for i in range(0, replicas):
            s = Bodega(
                s=valores[0],
                S=valores[1],
                politica=politica,
                periodos=periodos,
                demanda=None,
                precio_venta=final_price,
                costo_pedido=cost,
                costo_almacenamiento=storage_cost,
                costo_demanda_perdida=1200,
                tiempo_revision=1,  # Tieme que ser >= 1
                lead_time=7,
                caso_base=False
            )
            s.run()
 
            if muestra_grafico:
                #s.grafico()
                muestra_grafico = False

            resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

    # Se guardan kpi por repetición en excel
    nombre_columna, data_excel = guardar_pares_kpi(valores_politica, resultado, replicas, excel)


    # Se genera matriz por cada kpi en nueva hoja
    valores_matriz = guardar_matriz_heatmap_kpi(nombre_columna, rango_s_S, data_excel, excel)
    guardar_3d(valores_matriz, nombre_columna)

    excel.close()

# Guardo histogramas de kpi en carpetas
#histogramas_png(valores_politica, replicas)
