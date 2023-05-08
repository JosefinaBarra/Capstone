# Código: https://www.youtube.com/watch?v=Kmu9DNQamLw&ab_channel=PaulGrogan
# Código: https://asadali047.medium.com/inventory-simulation-for-beginners-7ea55eb6c4f8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Bodega:
    ''' Bodega con lead time de 1 semana '''
    def __init__(
        self, rop, max
    ):
        # Número de semanas simulación
        self.semanas = 50

        # Condiciones iniciales de bodega
        self.rop = rop
        self.max = max
        
        # Resultados
        self.demanda = {}
        self.ventas = {}
        self.almacenamiento = {}
        self.pedido = {}
        self.d_insatisfecha_semanal = {}
        self.ingresos = {}

        # Inventario inicial
        self.inventario = [0]*self.semanas

        # Pedidos realizados
        self.cant_ordenada = [0]*self.semanas

        # Demanda insatisfecha
        self.demanda_insatisfecha = [0]*self.semanas

        # Ingresos por venta
        self.precio_venta = 2

        # Costos
        self.costo_pedido = 2
        self.costo_almacenamiento = 2
        self.costo_demanda_perdida = 5

    # Demanda por semana
    def generar_demanda(self):
        for i in range(0, self.semanas):
            #demanda_generada = np.random.normal(144.9151, 55.5326)
            demanda_generada = np.random.uniform(61, 1725)
            #demanda_generada = np.random.gamma(3.002389619, 0.006414003)
            self.demanda[i] = demanda_generada
        return self.demanda

    def pedido_semana(self, semana):
        if self.inventario[semana] < self.rop:
            return self.max - self.inventario[semana]
        return 0

    def run(self):
        self.demanda = self.generar_demanda()
        self.inventario[0] = 0
        for i in range(0, self.semanas):
            # Actualizo inventario si hay pedido de semana anterior
            if self.inventario[i-1] < self.rop:
                self.inventario[i] = self.max - self.inventario[i-1] 
            else:
                self.inventario[i] = self.inventario[i-1] - self.ventas[i-1]
            
            # Reviso política (s,S)
            self.cant_ordenada[i] = self.pedido_semana(i)
            #print(f"\nPedido para próx semana: {self.cant_ordenada[i]}")

            # Reviso inventario para venta
            demanda = self.demanda[i]
            if demanda <= self.inventario[i]:
                self.ventas[i] = demanda

            # Vendo todo el inventario
            else:
                self.ventas[i] = self.inventario[i]
                self.demanda_insatisfecha[i] = demanda - self.inventario[i]

            # Costos al final de la semana
            self.almacenamiento[i] = (self.inventario[i] - self.ventas[i])*self.costo_almacenamiento
            self.pedido[i] = self.cant_ordenada[i]*self.costo_pedido
            self.d_insatisfecha_semanal[i] = self.demanda_insatisfecha[i]*self.costo_demanda_perdida
            self.ingresos[i] = self.ventas[i]*self.precio_venta
            
    def guardar_datos(self):
        ''' Exporto datos de la bodega en archivo excel '''
        col1 = "Semana"
        col2 = "Demanda"
        col3 = "Inventario"
        col4 = "Ventas"
        col5 = "Pedidos"
        col6 = "Demanda insatisfecha"

        data = pd.DataFrame({
            col1:list(self.demanda.keys()),
            col2:list(self.demanda.values()),
            col3:self.inventario,
            col4:list(self.ventas.values()),
            col5:self.cant_ordenada,
            col6:self.demanda_insatisfecha
        })
        data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)
    
    # Se calculan los kpi
    def nivel_servicio(self):
        total_demanda = sum(self.demanda.values())
        total_ventas = sum(self.ventas.values())
        return total_ventas/total_demanda
    
    def calcular_costos(self):
        total_pedidos = sum(self.pedido.values())

        total_almacenamiento = sum(self.almacenamiento.values())

        total_d_perdida = sum(self.d_insatisfecha_semanal.values())

        total = total_almacenamiento+total_d_perdida+total_pedidos

        return [total_pedidos, total_almacenamiento, total_d_perdida, total]
    
    def rotacion_inventario(self):
        pass

    def perdida_obsolescencia(self):
        pass

    def precision_demanda_pronosticada(self):
        pass

    def rotura_stock(self):
        pedido_no_satisfecho = sum(self.demanda_insatisfecha)
        pedidos_totales = sum(self.demanda.values())

        return pedido_no_satisfecho/pedidos_totales

    def guardar_kpi(self):
        nivel_servicio = self.nivel_servicio()
        costos_totales = self.calcular_costos()
        rotura_stock = self.rotura_stock()
        return {
            "Nivel servicio": nivel_servicio,
            "Costo pedidos": costos_totales[0],
            "Costo almacenamiento": costos_totales[1],
            "Costo demanda insatisfecha": costos_totales[2],
            "Costo total": costos_totales[3],
            "Rotura de stock": rotura_stock
        }
        
    
    def grafico(self):
        ''' Crea gráfico día vs inventario '''
        plt.figure()
        plt.step(list(range(0, self.semanas)), self.inventario, where='post')
        plt.xlabel("Semanas")
        plt.ylabel("Inventario")
        plt.show()
