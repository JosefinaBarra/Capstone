import numpy as np


def prom_pond_simple(demanda):
    return np.mean(demanda)


def suavizacion_demanda(demanda, alpha):
    pronostico = [demanda[0]]
    for i in range(1, len(demanda)):
        calculo = pronostico[-1] + alpha*(demanda[i]-pronostico[-1])
        pronostico.append(calculo)
    return pronostico
