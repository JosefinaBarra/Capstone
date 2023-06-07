import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools as it
import collections as _col

np.random.seed(0)


# [1] Función de: https://stackoverflow.com/questions/57809568/counting-sequential-occurrences-in-a-list-and
def scores(l):
    return _col.Counter(
        [len(list(b)) for a, b in it.groupby(l, key=lambda x:x != 0) if a]
    )


class Bodega:
    ''' Bodega con leadtime de 7 dias '''
    def __init__(
        self, s, S, politica, periodos, demanda, info_producto,
        tiempo_revision, lead_time, caso_base
    ):
        # Número de dias de simulación
        self.dias = periodos
        self.politica = politica
        self.caso_base = caso_base
        if self.caso_base:
            self.demanda = demanda
        else:
            self.demanda = {}

        self.nombre_producto = info_producto['nombre']
        self.item_id = info_producto['id']

        # Ingresos por venta
        self.precio_venta = info_producto['final_price']

        # Costos
        self.costo_pedido = info_producto['cost']
        self.costo_almacenamiento = info_producto['storage_cost']
        self.costo_demanda_perdida = 1200

        self.tiempo_revision = tiempo_revision

        # Lead time pedido
        self.lead_time = lead_time

        self.max = S
        self.rop = s

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
            demanda_generada = np.random.poisson(3.825)
            self.demanda[i] = demanda_generada
        return self.demanda

    def pedido_semana(self, dia, politica):
        ''' Retorna la cantidad a pedir según la política '''
        if self.inventario[dia] <= self.rop:
            return self.max - self.inventario[dia]
        return 0

    def run(self):
        ''' Corre simulación de bodega por dia'''
        if not self.caso_base:
            self.demanda = self.generar_demanda()
        self.inventario[0] = self.max
        encamino = False
        # print(f'En camino? {encamino} ')

        if self.politica == "EOQ":
            self.rop = self.rop_eoq()

        for i in range(0, self.dias):
            # print(f"----- DIA {i} -----")
            # ACTUALIZO PEDIDO
            if (i >= self.lead_time) and (
                self.cant_ordenada[i-self.lead_time] != 0
            ):
                self.inventario[i] = (
                    self.inventario[i-1] - self.ventas[i-1]
                ) + self.cant_ordenada[i-self.lead_time]
                encamino = False

            elif i > 0:
                self.inventario[i] = self.inventario[i-1] - self.ventas[i-1]

            # EVALÚO POLÍTICA PARA HACER UN PEDIDO
            if not encamino:
                # Si toca hacer revisión
                if self.tiempo_revision != 0 and i % self.tiempo_revision == 0:
                    self.cant_ordenada[i] = self.pedido_semana(
                        i, self.politica
                    )
                    if self.cant_ordenada[i] > 0:
                        encamino = True

            # REVISO CANTIDAD QUE VENDO
            demanda = self.demanda[i]
            # Cumplo con la demanda
            if demanda <= self.inventario[i]:
                self.ventas[i] = demanda

            # Vendo todo el inventario
            elif demanda > self.inventario[i]:
                if self.inventario[i] > 0:
                    self.ventas[i] = self.inventario[i]
                else:
                    self.ventas[i] = 0
                self.demanda_insatisfecha[i] = demanda - self.inventario[i]

            # Guardo productos que se mantuvieron en bodega durante el día i
            self.almacenamiento[i] = (
                self.inventario[i] - self.ventas[i]
            )*self.costo_almacenamiento

        self.periodos_sin_stock()

    def guardar_datos(self, excel, politica):
        ''' Exporto datos de la bodega en archivo excel según la política '''

        col1 = "Días"
        col2 = "Demanda [unidades]"
        col3 = "Inventario [unidades]"
        col4 = "Ventas [$]"
        col5 = "Pedidos [unidades]"
        col6 = "Demanda insatisfecha [unidades]"
        col7 = "Costo monetario stock out [$]"

        data = pd.DataFrame({
            col1: list(self.demanda.keys()),
            col2: list(self.demanda.values()),
            col3: self.inventario,
            col4: list(self.ventas.values()),
            col5: self.cant_ordenada,
            col6: self.demanda_insatisfecha,
            col7: list(self.d_insatisfecha_diaria.values())
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

        costo_almacenamiento = sum(self.almacenamiento)

        total_demanda_perdida = sum(self.demanda_insatisfecha)
        costo_demanda_insatisfecha = total_demanda_perdida * self.precio_venta

        costo_total = (
            costo_pedidos + costo_almacenamiento + costo_demanda_insatisfecha
        )

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
        ''' [1] Función de stackoverflow
        Cuenta ocurrencias seguidas de demanda insatisfecha != 0'''
        d = {'D': scores(self.demanda_insatisfecha)}

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

        data = {
            "Nivel servicio [%]": np.round(nivel_servicio*100, 3),
            "Rotura de stock [%]": np.round(rotura_stock, 3),

            "Total pedidos [unidades]": sum(self.cant_ordenada),
            "Costo pedidos [$]": np.round(costo_pedidos, 3),

            "Costo almacenamiento [$]": np.round(costo_almacenamiento, 3),

            "Cantidad dias sin stock [dias]": cant_dias_sin_stock,
            "Cantidad total sin vender [unidades]": total_sin_vender,
            "Costo demanda insatisfecha [$]": np.round(
                costo_demanda_insatisfecha, 3
            ),

            "Costo total [$]": np.round(costo_total, 3),

            "Total ventas [unidades]": total_ventas,
            "Ingresos por ventas [$]": np.round(total_ventas*self.precio_venta, 3),
            "Balance [$]": np.round(total_ventas*self.precio_venta - costo_pedidos - costo_almacenamiento, 3)
        }

        # Dias seguidas sin stock
        periodos = periodos_sin_stock
        for p in periodos:
            data[p] = periodos[p]
        return data

    def grafico(self):
        ''' Crea gráfico dias vs nivel de inventario '''
        actual_path = os.getcwd()

        fig, ax = plt.subplots()
        plt.step(list(range(0, self.dias)), self.inventario, where='post')
        plt.xlabel("Días")
        plt.ylabel("Inventario")
        titulo = f'Item {self.item_id}: {self.nombre_producto}\n({str(np.ceil(self.rop))}, {str(self.max)})'
        plt.title(titulo)
        folder = 'graficos'
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        fig.savefig(folder+"/caso_base.png")
