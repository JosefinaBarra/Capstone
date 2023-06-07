import time
from concurrent.futures import ThreadPoolExecutor
from simulacion_diario_copy import Bodega
from guardar_data_copy import guardar_pares_kpi
import threading
import os
import pandas as pd
import numpy as np

start = time.perf_counter()

np.random.seed(0)
def process_bodega(params):
    politica, dias_simulados, producto, tiempo_revision, lead_time, repeticion, lock = params

    # Crea una instancia de la clase Bodega
    bodega = Bodega(politica, dias_simulados, 1, producto, tiempo_revision, lead_time)
    print(f"Ejecutando repeticion {repeticion} Bodega con política {politica} en producto {producto['id']}, tiempo de revisión {tiempo_revision} y lead time {lead_time}")

    # Llama a la función que deseas ejecutar en paralelo dentro de la instancia de Bodega
    bodega.run()

    kpi = bodega.guardar_kpi()
    # Adquirir el bloqueo antes de actualizar el diccionario resultado
    lock.acquire()
    try:
        if str(producto['id']) not in resultado:
            resultado[str(producto['id'])] = {}
        if str(politica) not in resultado[str(producto['id'])]:
            resultado[str(producto['id'])][str(politica)] = {}
 
        resultado[str(producto['id'])][str(politica)]["repeticion"+str(repeticion)] = kpi
    finally:
        # Liberar el bloqueo después de actualizar el diccionario resultado
        lock.release()


tiempos_revision = [1]  # Puedes proporcionar aquí tu lista de tiempos de revisión
info_productos = [
    {'id': 885, 'nombre': 'VACUNA OCTUPLE', 'precio_venta': 5261, 'costo_pedido': 4201, 'costo_almacenamiento': 12, 'costo_demanda_perdida': 1200},
]
replicas = 10
dias_simulados = 365
rango_s_S = 5

politicas = [(s, S) for s in range(rango_s_S) for S in range(rango_s_S) if s <= S]

actual_path = os.getcwd()

resultado = {}
lock = threading.Lock()

lead_times = [7]  # Puedes proporcionar aquí tu lista de lead times


if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        for repeticion in range(replicas):
            params = [
                (
                    politica, dias_simulados, producto, tiempo_revision, lead_time, repeticion, lock
                ) for politica in politicas for producto in info_productos for tiempo_revision in tiempos_revision for lead_time in lead_times
            ]
            executor.map(process_bodega, params)

    import pprint

    # Prints the nicely formatted dictionary
    pprint.pprint(resultado)

    with ThreadPoolExecutor() as executor:
        for producto in info_productos:
            for tiempos in tiempos_revision:
                folder = 'PRODCUCTO_' + str(producto['id'])+'/T'+str(tiempos)

                dir = os.path.join(actual_path, folder)
                if not os.path.exists(dir):
                    os.makedirs(dir)

                excel = pd.ExcelWriter(
                    os.path.join(actual_path, folder, 'data_'+str(tiempos)+'.xlsx'),
                    engine="xlsxwriter", 
                    engine_kwargs={"options": {"strings_to_numbers": True}}
                )

                nombre_columna, data_excel = guardar_pares_kpi(politicas, resultado[str(producto['id'])], replicas, excel)
        excel.close()

    finish = time.perf_counter()

    print(f'Finished in {round(finish-start, 2)} second(s)')