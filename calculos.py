import numpy as np
import pprint
import pandas as pd


def calcular_kpi(resultado, valores_politica):
    valores_kpi = {}
    for valores in valores_politica:
        valores_kpi[str(valores)] = {}
        resultado_politica = resultado[str(valores)]
        for i in range(0, len(resultado_politica)):
            valores_kpi[str(valores)][i] = {}
            demanda = sum(list(resultado_politica[i].demanda.values()))
            pedidos = sum(list(resultado_politica[i].cant_ordenada.values()))
            ventas = sum(list(resultado_politica[i].ventas.values()))
            demanda_insatisfecha = sum(list(resultado_politica[i].demanda_insatisfecha.values()))
            almacenamiento = sum(list(resultado_politica[i].almacenamiento.values()))

            valores_kpi[str(valores)][i]['Nivel de servicio'] = (ventas/demanda)*100
            valores_kpi[str(valores)][i]['Rotura stock'] = (demanda_insatisfecha/demanda)*100
            valores_kpi[str(valores)][i]['Total pedidos'] = pedidos
            valores_kpi[str(valores)][i]['Total ventas'] = ventas
            valores_kpi[str(valores)][i]['Total sin vender'] = demanda_insatisfecha
            valores_kpi[str(valores)][i]['Costo pedidos'] = pedidos * resultado_politica[i].costo_pedido
            valores_kpi[str(valores)][i]['Costo almacenamiento'] = almacenamiento
            valores_kpi[str(valores)][i]['Costo demanda insatisfecha'] = demanda_insatisfecha * resultado_politica[i].costo_demanda_perdida
            valores_kpi[str(valores)][i]['Costo total'] = pedidos * resultado_politica[i].costo_pedido + almacenamiento + demanda_insatisfecha * resultado_politica[i].costo_demanda_perdida
            valores_kpi[str(valores)][i]['Ingresos'] = ventas * resultado_politica[i].precio_venta
            valores_kpi[str(valores)][i]['Balance'] = ventas * resultado_politica[i].precio_venta - (almacenamiento + pedidos * resultado_politica[i].costo_pedido)
    return valores_kpi


def calcular_mean_kpi(valores_kpi):
    mean_kpi = {}
    for politica, kpi in valores_kpi.items():
        df = pd.DataFrame.from_dict(kpi, orient='columns', dtype=None)
        df = df.transpose()
        df2 = df.mean(axis=0)
        mean_kpi[str(politica)] = dict(df2)
    return mean_kpi


def calcular_min_kpi(valores_kpi):
    min_kpi = {}
    for politica, kpi in valores_kpi.items():
        df = pd.DataFrame.from_dict(kpi, orient='columns', dtype=None)
        df = df.transpose()
        df2 = df.min(axis=0)
        min_kpi[str(politica)] = dict(df2)
    return min_kpi


def calcular_max_kpi(valores_kpi):
    min_kpi = {}
    for politica, kpi in valores_kpi.items():
        df = pd.DataFrame.from_dict(kpi, orient='columns', dtype=None)
        df = df.transpose()
        df2 = df.max(axis=0)
        min_kpi[str(politica)] = dict(df2)
    return min_kpi


# https://www.pythonforbeginners.com/basics/tuple-string-to-tuple-in-python
def str_tuple(myStr):
    myStr = myStr.replace("(", "")
    myStr = myStr.replace(")", "")
    myStr = myStr.replace(",", " ")
    myList = myStr.split()
    myList = list(map(int, myList))
    return tuple(myList)


def matriz_kpi(kpi):
    pprint.pprint(kpi)
    matriz_kpi = {}
    lista_kpi = list(kpi[next(iter(kpi))].keys())
    for i in range(len(lista_kpi)):
        matriz = np.zeros((len(kpi.keys()), len(kpi.keys())))
        for politica, resultado in kpi.items():
            politica_tupla = str_tuple(politica)
            row = politica_tupla[0]
            col = politica_tupla[1]
            matriz[row][col] = resultado[lista_kpi[i]]
        matriz_kpi[lista_kpi[i]] = matriz
    return matriz_kpi