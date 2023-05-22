import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import itertools as it, collections as _col

# [1] Función de: https://stackoverflow.com/questions/57809568/counting-sequential-occurrences-in-a-list-and
def scores(l):
  return _col.Counter([len(list(b)) for a, b in it.groupby(l, key=lambda x:x != 0) if a])


class Bodega:
    ''' Bodega con leadtime de 7 dias '''
    def __init__(
        self, s, S, politica, periodos, demanda
    ):
        # Número de dias de simulación
        self.dias = periodos
        self.politica = politica
        self.demanda = demanda

        # Ingresos por venta
        self.precio_venta = 6260

        # Costos
        self.costo_pedido = 4201
        self.costo_almacenamiento = 12
        self.costo_demanda_perdida = 6260

        # Lead time pedido
        self.lead_time = 2

        self.max = S
        
        if self.politica == "(s,S)":
            self.rop = s
        elif self.politica == "EOQ":
            self.rop = self.rop_eoq()
        
        # Resultados
        self.ventas = {}

        # Inventario inicial
        self.inventario = [0]*self.dias

        # Pedidos realizados
        self.cant_ordenada = [0]*self.dias

        # Demanda insatisfecha
        self.demanda_insatisfecha = [0]*self.dias

        # Productos almacenados al final del día i
        self.almacenamiento = [0]*self.dias

    # Demanda por dia
    def generar_demanda(self):
        ''' Genera demanda diaria según distribución '''
        for i in range(0, self.dias):
            #demanda_generada = np.random.normal(144.9151, 55.5326)
            #demanda_generada = np.random.uniform(61, 1725)
            #demanda_generada = np.random.uniform(0, 5)
            #demanda_generada = np.random.gamma(3.002389619, 0.006414003)
            #demanda_generada = np.random.poisson(0.9)
            demanda_generada = np.random.poisson(3.825)
            self.demanda[i] = demanda_generada
        return self.demanda
    
# -----  ----- POLÍTICA EOQ ----- ----- 
    def pedido_semana(self, dia, politica):
        ''' Retorna la cantidad a pedir según la política '''
        if politica == "(s,S)":
            if self.inventario[dia] <= self.rop:
                return self.max - self.inventario[dia]
            return 0
        elif politica == "EOQ":
            pedido = np.ceil(self.eoq())
            return pedido

    def eoq(self):
        demanda_total = np.sum(list(self.demanda.values()))
        costo_almacenamiento_total = self.costo_almacenamiento * self.dias
        self.Q_optimo = np.sqrt((2*demanda_total*self.costo_pedido)/(self.costo_almacenamiento*self.dias))
        #print(f"(2 * {demanda_total} * {self.costo_pedido}) / ({self.costo_almacenamiento} * {self.dias}")
        #print(f"EOQ = {self.Q_optimo}\n")
        return self.Q_optimo

    def rop_eoq(self):
        demanda_promedio = np.mean(list(self.demanda.values()))
        demanda_total = np.sum(list(self.demanda.values()))
        
        # Número esperado de ordenes
        N = demanda_total / self.eoq()
       
        # Punto de reorden
        L = self.dias / N
        self.tiempo_entre_pedidos = np.ceil(L)
        R = demanda_promedio*L
        #print(f"N = {np.ceil(N)}, L = {np.ceil(L)}, R = {np.ceil(R)}")
        return R

# ----- ----- ----- ----- ----- ----- ----- 

    def run(self):
        ''' Corre simulación de bodega por dia'''
        self.demanda = self.generar_demanda()
        self.inventario[0] = 0
        encamino = False
        #print(f'En camino? {encamino} ')

        if self.politica == "EOQ":
            self.rop = self.rop_eoq()

        for i in range(0, self.dias):
            #print(f"----- DIA {i} -----")

            if self.politica == "(s,S)":
                # ACTUALIZO PEDIDO
                if i >= self.lead_time and self.cant_ordenada[i-self.lead_time] != 0:
                    self.inventario[i] = (self.inventario[i-1] - self.ventas[i-1]) + self.cant_ordenada[i-self.lead_time]
                    encamino = False
                    #print(f'Recibo pedido del día {i-self.lead_time} por :{self.cant_ordenada[i-self.lead_time]}')
                    #print(f'Inventario actualizado = {self.inventario[i]}\nEn camino? {encamino}\n')
                elif i > 1:
                    self.inventario[i] = self.inventario[i-1] - self.ventas[i-1]
                    #print("No hay pedidos por recibir")
                    #print(f'Inventario actualizado = {self.inventario[i]}\nEn camino? {encamino}\n')
                
                # EVALÚO POLÍTICA PARA HACER UN PEDIDO
                if not encamino:
                    self.cant_ordenada[i] = self.pedido_semana(i, self.politica)
                    if self.cant_ordenada[i] > 0:
                        encamino = True
                #print(f"\nPEDIDO REALIZADO DIA {i}: {self.cant_ordenada[i]}\nEn camino {encamino}\n")
            
            elif self.politica == "EOQ":
                if i >= self.lead_time and self.cant_ordenada[i-self.lead_time] != 0:
                    self.inventario[i] = (self.inventario[i-1] - self.ventas[i-1]) + self.cant_ordenada[i-self.lead_time]
                    #print(f'Recibo pedido del día {i-self.lead_time} por :{self.cant_ordenada[i-self.lead_time]}')
                    #print(f'Inventario actualizado = {self.inventario[i]}\nEn camino? {encamino}\n')

                elif i > 1:
                    self.inventario[i] = self.inventario[i-1] - self.ventas[i-1]
                    #print("No hay pedidos por recibir")
                    #print(f'Inventario actualizado = {self.inventario[i]}\nEn camino? {encamino}\n')

                #print(f"\n --- i({i}) % 14({self.tiempo_entre_pedidos}) = {i%self.tiempo_entre_pedidos} --- \n")
                if i == 0:
                    self.cant_ordenada[i] = self.Q_optimo
                    #print(f"\nPEDIDO REALIZADO DIA {i}: {self.cant_ordenada[i]}\n")
                if i % self.tiempo_entre_pedidos == 0 and self.rop > self.inventario[i]:
                    self.cant_ordenada[i] = self.Q_optimo
                    #print(f"\nPEDIDO REALIZADO DIA {i}: {self.cant_ordenada[i]}\n")


            # REVISO CANTIDAD QUE VENDO
            demanda = self.demanda[i]
            # Cumplo con la demanda
            if demanda <= self.inventario[i]:
                self.ventas[i] = demanda
                #print(f"VENDO: {demanda}")
                #print(f'Debería quedar en Inventario = {self.inventario[i] - self.ventas[i]}\n')

            # Vendo todo el inventario
            else:
                if self.inventario[i] > 0:
                    self.ventas[i] = self.inventario[i]
                else:
                    self.ventas[i] = 0
                self.demanda_insatisfecha[i] = demanda - self.inventario[i]
                #print(f"QUIEBRE DE STOCK: D={demanda} I={self.inventario[i]} - INSATISFECHO: {self.demanda_insatisfecha[i]}")
                #print(f'Debería quedan en Inventario = {self.inventario[i] - self.ventas[i]}\n')

            # Guardo productos que se mantuvieron en bodega durante el día i
            self.almacenamiento[i] = (self.inventario[i] - self.ventas[i])
        
        self.periodos_sin_stock()
            
    def guardar_datos(self, excel, politica):
        ''' Exporto datos de la bodega en archivo excel según la política ingresada '''

        col1 = "Días"
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
            col7:list(self.d_insatisfecha_diaria.values())
        })
        data.to_excel(excel, sheet_name=politica, index=False)
    

# ----- ----- Se calculan los kpi ----- ----- 
    def nivel_servicio(self):
        ''' Calcula kpi del nivel de servicio '''
        total_demanda = sum(self.demanda.values())
        total_ventas = sum(self.ventas.values())
        return total_ventas/total_demanda
    
    def calcular_costos(self):
        ''' Calcula costos de la bodega '''
        total_pedidos = sum(self.cant_ordenada)
        costo_pedidos = total_pedidos * self.costo_pedido

        total_almacenamiento = sum(self.almacenamiento)
        costo_almacenamiento = total_almacenamiento * self.costo_almacenamiento

        total_demanda_perdida = sum(self.demanda_insatisfecha)
        costo_demanda_insatisfecha = total_demanda_perdida * self.precio_venta

        costo_total = costo_pedidos + costo_almacenamiento + costo_demanda_insatisfecha

        return costo_pedidos, costo_almacenamiento, costo_demanda_insatisfecha, costo_total
    
    def rotura_stock(self):
        ''' Se calcula la proporción de pedidos perdidos'''
        total_demanda_perdida = sum(self.demanda_insatisfecha)
        total_demanda = sum(self.demanda.values())

        return (total_demanda_perdida/total_demanda)*100
        
    def perdida_monetaria_quiebre_stock(self):
        ''' Retorna el valor monetario por las unidades no vendidas'''
        return sum(self.demanda_insatisfecha)*self.precio_venta
    
    def periodos_sin_stock(self):
        ''' [1] Función de stackoverflow: Cuenta ocurrencias seguidas de demanda insatisfecha != 0'''
        d = {'D':scores(self.demanda_insatisfecha)}

        datos = {}
        for i in range(0, 6):
            datos[str(i)+" dias seguidos [ocurrencias]"] = d["D"][i]
        datos.pop("0 dias seguidos [ocurrencias]")
        return datos


    def guardar_kpi(self):
        ''' Retorna valores de kpi en diccionario '''
        nivel_servicio = self.nivel_servicio()
        costo_pedidos, costo_almacenamiento, costo_demanda_insatisfecha, costo_total = self.calcular_costos()
        
        rotura_stock = self.rotura_stock()
        
        periodos_sin_stock = self.periodos_sin_stock()
        cant_dias_sin_stock = np.count_nonzero(self.demanda_insatisfecha)
        
        total_ventas = np.sum(list(self.ventas.values()))
        total_sin_vender = sum(self.demanda_insatisfecha)
               
        data =  {
            "Nivel servicio": nivel_servicio,
            "Rotura de stock [%]": rotura_stock,

            "Total pedidos [unidades]": sum(self.cant_ordenada),         
            "Costo pedidos [$]": costo_pedidos,

            "Costo almacenamiento [$]": costo_almacenamiento,
            
            "Cantidad dias sin stock": cant_dias_sin_stock,
            "Cantidad total sin vender [unidades]": total_sin_vender,
            "Pérdida monetaria quiebre stock [$]": total_sin_vender * self.precio_venta,
            "Costo demanda insatisfecha [$]": costo_demanda_insatisfecha,
            
            "Costo total [$]": costo_total,

            "Total ventas [unidades]": total_ventas,
            "Ingresos por ventas [$]": total_ventas*self.precio_venta,
            "Balance": total_ventas*self.precio_venta - costo_total
        }

        # Dias seguidas sin stock
        periodos = periodos_sin_stock
        for p in periodos:
            data[p] = periodos[p]
        return data
        
    
    def grafico(self):
        ''' Crea gráfico dias vs nivel de inventario '''
        plt.figure()
        plt.step(list(range(0, self.dias)), self.inventario, where='post')
        plt.xlabel("Días")
        plt.ylabel("Inventario")
        if self.politica == "(s,S)":
            titulo = self.politica + " : (" + str(np.ceil(self.rop)) + ", " + str(self.max) + ")"
        elif self.politica == "EOQ":
            titulo = self.politica + "Q_optimo = " + str(self.Q_optimo) + " - rop = " + str(self.rop) 
        plt.title(titulo)
        plt.show()
