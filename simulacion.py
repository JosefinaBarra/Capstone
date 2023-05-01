# Código: https://www.youtube.com/watch?v=Kmu9DNQamLw&ab_channel=PaulGrogan
# Código: https://asadali047.medium.com/inventory-simulation-for-beginners-7ea55eb6c4f8

import simpy
import matplotlib.pyplot as plt
import numpy as np


class Bodega:
    def __init__(
        self, env, rop, max, costo_almacenamiento, costo_orden, precio_venta, lead_time
    ):
        self.env = env
        self.rop = rop
        self.max = max
        #self.demanda = demanda
        self.costo_almacenamiento = costo_almacenamiento
        self.precio_venta = precio_venta
        self.costo_orden = costo_orden
        self.lead_time = lead_time

        # Inventario inicial
        self.inventario = max
        self.balance = 0
        self.cant_ordenada = 0
        self.obs = []
        self.nivel_inventario = []

    def generar_llegada_cliente(self):
        return np.random.exponential(1./5)

    # Demanda por cliente D ~ Unif(1,4)
    def generar_demanda(self):
        return np.random.randint(1,5)

    def realizar_orden(self):
        # Política (s,S) o min/max:
        self.cant_ordenada = self.max
        print("{:.2f} Nueva orden por: {}".format(self.env.now, self.max))

        # Política EOQ
        # BUSCAR

        self.balance -= self.cant_ordenada * self.costo_orden
        
        # Espero que llegue pedido
        yield self.env.timeout(self.lead_time)
        self.inventario += self.cant_ordenada
        self.cant_ordenada = 0

        print(f'[{round(self.env.now, 2)}] Orden recibida, {self.inventario} en inventario')

    def runner_setup(self):
        while True:
            llegada_cliente = self.generar_llegada_cliente()

            # Espero llegada cliente
            yield self.env.timeout(llegada_cliente)

            # Costo almacenar hasta llegada cliente
            self.balance -= self.inventario*self.costo_almacenamiento*llegada_cliente
            
            # Generar demanda cliente
            self.demanda = self.generar_demanda()

            # Hay stock
            if self.demanda < self.inventario:
                self.balance += self.precio_venta*self.demanda
                self.inventario -= self.demanda
                print(f'[ {round(self.env.now,2)}] Vendo {self.demanda}')
            
            # No hay stock -> Vendo todo
            else:
                self.balance += self.precio_venta*self.inventario
                self.inventario = 0
                print(f'[{round(self.env.now,2)}] Stock insuficiente!! Quedan: {self.inventario} ')

            # Revisión continua: Inventario < min Y no hay orden en camino
            if self.inventario < self.rop and self.cant_ordenada == 0:
                self.env.process(self.realizar_orden())
    
    def observe(self):
        while True:
            self.obs.append(self.env.now)
            self.nivel_inventario.append(self.inventario)
            yield self.env.timeout(0.1)
    
    def grafico(self):
        plt.figure()
        plt.step(self.obs, self.nivel_inventario, where='post')
        plt.xlabel("Días")
        plt.ylabel("Inventario")
        plt.show()


def run(simulation:Bodega,until:float):
    simulation.env.process(simulation.runner_setup())
    simulation.env.process(simulation.observe())
    simulation.env.run(until=until)


np.random.seed(0)

s = Bodega(simpy.Environment(), 10, 30, 2, 50, 100, 2)
run(s,8)
#print(s.inventory_level)
s.grafico()
