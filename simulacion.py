# Código: https://www.youtube.com/watch?v=Kmu9DNQamLw&ab_channel=PaulGrogan

import simpy
import matplotlib.pyplot as plt
import numpy as np

from generacion_datos import demanda_simulada
from pronostico_demanda import suavizacion_demanda, prom_pond_simple


# Order policy (s,S)
def bodega(env, min, max, periodo):
    global inventario, balance, cant_ordenada

    demanda_historica = demanda_simulada()

    # Inventario inicial
    inventario = max
    balance = 0.0
    cant_ordenada = 0

    costo_almac = 2
    precio_venta = 200

    while True:
        llegada_cliente = generar_llegada_cliente()

        # Esperar llegada cliente
        yield env.timeout(llegada_cliente)

        # Actualizar balance por costo de almacenamiento
        balance -= inventario * costo_almac*llegada_cliente

        # Genera demanda por cliente
        demanda = generar_demanda()

        # Añado demanda al histórico
        demanda_historica.append(demanda)

        # Suficiente inventario para suplir demanda
        if demanda < inventario:
            balance += precio_venta * demanda
            inventario -= demanda
            print(
                "{:.2f} Vendido: {} - Inventario actual: {}".format(
                    env.now, demanda, inventario
                )
            )

        else:
            # No hay suficiente inventario -> Se vende todo
            balance += precio_venta * inventario
            inventario = 0
            print("{:.2f} Sold out: {}".format(env.now, inventario))

        # Reviso condición de reabastecimiento
        if (
            (inventario < min and cant_ordenada == 0)
        ):
            env.process(realizar_orden(env, max, demanda_historica))


def realizar_orden(env, max, demanda_historica):
    global inventario, balance, cant_ordenada
    costo_orden = 50
    lead_time = 2

    # Usando solo política min-max
    cant_ordenada = max - inventario

    # Usando promedio movil simple
    F_t = prom_pond_simple(demanda_historica)
    print("F_t: {} vs cant_ordenada: {}".format(F_t, cant_ordenada))

    # Usando pronóstico de uniformidad exponencial
    alpha = 0.1
    suav_demanda = suavizacion_demanda(demanda_historica, alpha)
    F_t = suav_demanda[-1]

    cant_ordenada = F_t

    balance -= costo_orden * cant_ordenada
    print("{:.2f} Nueva orden por: {}".format(env.now, cant_ordenada))

    # Tiempo que demora en llegar pedido
    yield env.timeout(lead_time)

    # Actualizar inventario
    inventario += cant_ordenada
    cant_ordenada = 0
    print(
        "{:.2f} orden recibida, {} en inventario".format(
            env.now, inventario
        )
    )


# Llegada de cliente d ~ Exp(lambda=5)
def generar_llegada_cliente():
    return np.random.exponential(1./5)


# Demanda por cliente D ~ Unif(1,4)
def generar_demanda():
    return np.random.randint(1, 5)


obs_time = []
nivel_inventario = []


def observe(env):
    global inventario

    while True:
        obs_time.append(env.now)
        nivel_inventario.append(inventario)
        yield env.timeout(0.1)


np.random.seed(0)
min = 10
max = 30
periodo = 1

env = simpy.Environment()
env.process(bodega(env, min, max, periodo))
env.process(observe(env))
env.run(until=30)

plt.figure()
plt.step(obs_time, nivel_inventario, where='post')
plt.xlabel("Días")
plt.ylabel("Inventario")
plt.show()
