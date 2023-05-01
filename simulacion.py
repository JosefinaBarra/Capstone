# Código: https://www.youtube.com/watch?v=Kmu9DNQamLw&ab_channel=PaulGrogan
# Código: https://asadali047.medium.com/inventory-simulation-for-beginners-7ea55eb6c4f8

import simpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Bodega:
    def __init__(
        self, env, rop, max, costo_almacenamiento, costo_orden, precio_venta, lead_time
    ):
        self.env = env
        self.rop = rop
        self.max = max
        self.costo_almacenamiento = costo_almacenamiento
        self.precio_venta = precio_venta
        self.costo_orden = costo_orden
        self.lead_time = lead_time
        #self.demanda = demanda

        # Inventario inicial
        self.inventario = max

        # Condiciones iniciales
        self.balance = 0
        self.cant_ordenada = 0
        
        self.obs = []
        self.nivel_inventario = []
        self.estado_balance = []

    def generar_llegada_cliente(self):
        return np.random.exponential(1./5)

    # Demanda por cliente D ~ Unif(1,4)
    def generar_demanda(self):
        return np.random.randint(1,5)

    def realizar_orden(self):
        # Política (s,S) o min/max:
        self.cant_ordenada = self.max
        self.balance -= self.cant_ordenada * self.costo_orden
        print(f"[{round(self.env.now, 2)}] Nueva orden por: {self.max}")
        print(f' - Costos por esta orden: {self.cant_ordenada * self.costo_orden} - Balance: {self.balance}\n')

        # Política EOQ
        # BUSCAR
        
        # Espero que llegue pedido
        yield self.env.timeout(self.lead_time)
        self.inventario += self.cant_ordenada
        self.cant_ordenada = 0

        print(f'[{round(self.env.now, 2)}] Orden recibida, {self.inventario} en inventario\n')

    def runner_setup(self):
        while True:
            llegada_cliente = self.generar_llegada_cliente()

            # Espero llegada cliente
            yield self.env.timeout(llegada_cliente)

            # Costo almacenar hasta llegada cliente
            self.balance -= self.inventario*self.costo_almacenamiento*llegada_cliente
            print(f'[{round(self.env.now,2)}] Llega cliente:')
            print(f' - Costos por almacenar: {self.inventario*self.costo_almacenamiento*llegada_cliente}')
            print(f' - Balance: {self.balance}')
            print(f' - Inventario: {self.inventario}\n\n')
            
            # Generar demanda cliente
            self.demanda = self.generar_demanda()

            # Hay stock
            if self.demanda < self.inventario:
                self.balance += self.precio_venta*self.demanda
                self.inventario -= self.demanda
                print(f'[{round(self.env.now,2)}] Realizo venta:')
                print(f' - Vendido: {self.demanda}')
                print(f' - Ganancias en esta venta: {self.precio_venta*self.demanda}')
                print(f' - Balance: {self.balance}')
                print(f' - Inventario: {self.inventario}\n\n')
            
            # Vendo todo -> Quedo sin stock
            elif self.demanda == self.inventario:
                self.balance += self.precio_venta*self.demanda
                self.inventario -= self.demanda
                print(f'[{round(self.env.now,2)}] Realizo venta:')
                print(f' - Vendido: {self.demanda}')
                print(f' - Ganancias en esta venta: {self.precio_venta*self.demanda}')
                print(f' - Balance: {self.balance}')
                print(f' - Inventario: {self.inventario}\n\n')
            
            elif self.demanda > self.inventario:
                print(f'[{round(self.env.now)}] NO TENEMOS STOCK!!\n\n')

            # Revisión continua: Inventario < min Y no hay orden en camino
            if self.inventario < self.rop and self.cant_ordenada == 0:
                print(f'REVISANDO STOCK: REALIZO ORDEN')
                self.env.process(self.realizar_orden())
    
    def observe(self):
        while True:
            self.obs.append(self.env.now)
            self.nivel_inventario.append(self.inventario)
            self.estado_balance.append(self.balance)
            yield self.env.timeout(0.1)
    
    def guardar_datos(self):
        col1 = "Tiempo"
        col2 = "Inventario actual"
        col3 = "Balance"

        data = pd.DataFrame({
            col1:self.obs,
            col2:self.nivel_inventario,
            col3:self.estado_balance
        })
        data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)
    
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

s = Bodega(
    simpy.Environment(),
    rop=10,
    max=30,
    costo_almacenamiento=2,
    costo_orden=50,
    precio_venta=100,
    lead_time=2
)
run(s,8)
s.grafico()
s.guardar_datos()
