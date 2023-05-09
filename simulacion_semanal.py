import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import itertools as it, collections as _col

# [1] Función de: https://stackoverflow.com/questions/57809568/counting-sequential-occurrences-in-a-list-and
def scores(l):
  return _col.Counter([len(list(b)) for a, b in it.groupby(l, key=lambda x:x != 0) if a])


class Bodega:
    ''' Bodega con leadtime de 1 semana '''
    def __init__(
        self, rop, max, politica
    ):
        # Número de semanas simulación
        self.semanas = 50
        self.politica = politica

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
        ''' Genera demanda semanal según distribución '''
        for i in range(0, self.semanas):
            #demanda_generada = np.random.normal(144.9151, 55.5326)
            demanda_generada = np.random.uniform(61, 1725)
            #demanda_generada = np.random.gamma(3.002389619, 0.006414003)
            self.demanda[i] = demanda_generada
        return self.demanda

    def pedido_semana(self, semana, politica):
        ''' Retorna la cantidad a pedir según la política '''
        if politica == "(s,S)":
            if self.inventario[semana] < self.rop:
                return self.max - self.inventario[semana]
            return 0
        elif politica == "EOQ":
            return 0

    def run(self):
        ''' Corre simulación de bodega por semana'''
        self.demanda = self.generar_demanda()
        self.inventario[0] = 0

        for i in range(0, self.semanas):
            # Actualizo inventario si hay pedido de semana anterior
            #print(f"----- SEMANA {i} -----")
            if i >= 1:
                if self.inventario[i-1] < self.rop:
                    self.inventario[i] = self.max - self.inventario[i-1] 
                    print(f'Recibo pedido de semana {i-1} de :{self.max - self.inventario[i-1] }')
                    print(f'Inventario = {self.inventario[i]}\n')
                else:
                    self.inventario[i] = self.inventario[i-1] - self.ventas[i-1]
                    print("No hay pedidos por recibir")
                    print(f'Inventario = {self.inventario[i]}\n')
            
            # Se calcula la cantidad a ordenar según política
            self.cant_ordenada[i] = self.pedido_semana(i, self.politica)
            print(f"\nPedido para próx semana: {self.cant_ordenada[i]}")

            # Reviso inventario para venta
            demanda = self.demanda[i]
            if demanda <= self.inventario[i]:
                self.ventas[i] = demanda
                #print(f"VENDO: {demanda}")
                #print(f'Inventario = {self.inventario[i] - self.ventas[i]}\n')

            # Vendo todo el inventario
            else:
                if self.inventario[i] > 0:
                    self.ventas[i] = self.inventario[i]
                else: 
                    self.ventas[i] = 0
                self.demanda_insatisfecha[i] = demanda - self.inventario[i]
                print(f"QUIEBRE DE STOCK: D={demanda} I={self.inventario[i]} - INSATISFECHO: {self.demanda_insatisfecha[i]}")
                print(f'Inventario = {self.inventario[i] - self.ventas[i]}\n')

            # Costos al final de la semana
            self.almacenamiento[i] = (self.inventario[i] - self.ventas[i])*self.costo_almacenamiento
            self.pedido[i] = self.cant_ordenada[i]*self.costo_pedido
            self.d_insatisfecha_semanal[i] = self.demanda_insatisfecha[i]*self.costo_demanda_perdida + self.demanda_insatisfecha[i]*self.precio_venta
            self.ingresos[i] = self.ventas[i]*self.precio_venta
        self.periodos_sin_stock()
            
    def guardar_datos(self, excel, politica):
        ''' Exporto datos de la bodega en archivo excel según la política ingresada '''

        col1 = "Semanas"
        col2 = "Demanda [unidades]"
        col3 = "Inventario [unidades]"
        col4 = "Ventas [$]"
        col5 = "Pedidos [unidades]"
        col6 = "Demanda insatisfecha [unidades]"
        col7 = "Costo monetario stock out [$]"

        data = pd.DataFrame({
            col1:list(self.demanda.keys()),
            col2:list(self.demanda.values()),
            col3:self.inventario,
            col4:list(self.ventas.values()),
            col5:self.cant_ordenada,
            col6:self.demanda_insatisfecha,
            col7:list(self.d_insatisfecha_semanal.values())
        })
        data.to_excel(excel, sheet_name=politica, index=False)
    
    # Se calculan los kpi
    def nivel_servicio(self):
        ''' Calcula kpi del nivel de servicio '''
        total_demanda = sum(self.demanda.values())
        total_ventas = sum(self.ventas.values())
        return total_ventas/total_demanda
    
    def calcular_costos(self):
        ''' Calcula costos de la bodega '''
        total_pedidos = sum(self.pedido.values())

        total_almacenamiento = sum(self.almacenamiento.values())

        total_d_perdida = sum(self.d_insatisfecha_semanal.values())

        total = total_almacenamiento+total_d_perdida+total_pedidos

        return [total_pedidos, total_almacenamiento, total_d_perdida, total]
    
    def rotura_stock(self):
        ''' Se calcula la proporción de pedidos perdidos'''
        pedido_no_satisfecho = sum(self.demanda_insatisfecha)
        pedidos_totales = sum(self.demanda.values())

        return pedido_no_satisfecho/pedidos_totales
    
    def unidades_sin_vender(self):
        ''' Total de productos sin vender por quiebre de stock '''
        return sum(self.demanda_insatisfecha)
    
    def perdida_monetaria_stock_out(self):
        ''' Retorna el valor monetario por las unidades no vendidas'''
        return sum(self.demanda_insatisfecha)*self.precio_venta
    
    def periodos_sin_stock(self):
        ''' [1] Función de stackoverflow: Cuenta ocurrencias seguidas de demanda insatisfecha != 0'''
        d = {'D':scores(self.demanda_insatisfecha)}
        r = '\n'.join([f'Días | {" | ".join(d.keys())} ', '-'*15]+[f'{i}          {"   ".join(str(b.get(i, 0)) for b in d.values())}' for i in range(1, 6)])
        minimo = min(list(d["D"]))
        maximo = max(list(d["D"]))
        i = minimo
        datos = {}
        for i in range(0, maximo + 1):
            datos[str(i)+"semanas"] = d["D"][i]
        return datos
            
    def guardar_kpi(self):
        ''' Retorna valores de kpi en diccionario '''
        nivel_servicio = self.nivel_servicio()
        costos_totales = self.calcular_costos()
        rotura_stock = self.rotura_stock()
        total_sin_vender = self.unidades_sin_vender()
        perdida_monetaria_stock_out = self.perdida_monetaria_stock_out()
        periodos_sin_stock = self.periodos_sin_stock()

        data = {
            "Nivel servicio": nivel_servicio,
            "Costo pedidos": costos_totales[0],
            "Costo almacenamiento": costos_totales[1],
            "Costo demanda insatisfecha": costos_totales[2],
            "Costo total": costos_totales[3],
            "Rotura de stock": rotura_stock,
            "Cantidad total sin vender": total_sin_vender,
            "Pérdida monetaria quiebre stock": perdida_monetaria_stock_out
        }
        periodos = periodos_sin_stock
        for p in periodos:
            data[p] = periodos[p]
        return data
        
    
    def grafico(self):
        ''' Crea gráfico semanas vs nivel de inventario '''
        plt.figure()
        plt.step(list(range(0, self.semanas)), self.inventario, where='post')
        plt.xlabel("Semanas")
        plt.ylabel("Inventario")
        plt.show()
