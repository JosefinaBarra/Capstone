import pandas as pd


def demanda_historica():
    demanda_real = {}
    dia = 0

    with open("dda_885.txt") as f:
        contenido = f.read().split('\n')
        for linea in contenido:
            separado = linea.split()
            for i in range(0, len(separado)):
                demanda_real[dia] = int(separado[i])
                dia += 1
    return demanda_real


def data_productos(productos):
    data = {}
    archivo = pd.read_csv('items.csv')
    for producto in productos:
        data[producto] = {}
        info = archivo.loc[archivo['item_id'] == producto]
        data[producto]['nombre'] = info['prod_descr'].tolist()[0]
        data[producto]['sale_price'] = info['sale_price'].tolist()[0]
        data[producto]['final_price'] = info['final_price'].tolist()[0]
        data[producto]['cost'] = info['cost'].tolist()[0]
        data[producto]['storage_cost'] = info['storage_cost'].tolist()[0]
    return data
