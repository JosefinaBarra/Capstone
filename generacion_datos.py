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
