import numpy as np


def demanda_simulada():
    # Suponiendo que la demanda histórica es de hace 1 mes
    demanda = []
    dias = 0

    while dias < 30:
        demanda_random = np.random.randint(1, 50)
        demanda.append(demanda_random)
        dias += 1

    return demanda


def suavizacion_demanda(demanda, alpha):
    pronostico = [demanda[0]]
    for i in range(1, len(demanda)):
        calculo = pronostico[-1] + alpha*(demanda[i]-pronostico[-1])
        pronostico.append(calculo)
    return pronostico
