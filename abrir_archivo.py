import pandas as pd

demanda_real = {}
dia = 0

with open("dda_885.txt") as f:
    contenido = f.read().split('\n')
    for linea in contenido:
        separado = linea.split()
        for i in range(0, len(separado)):
            demanda_real[dia] = int(separado[i])
            dia += 1

def valores_producto(lista_productos):
    precios = {}
    for producto in lista_productos:
        precios[str(producto)] = {}
        data_items = pd.read_csv('items.csv')
        index_id = data_items.set_index(['item_id'])

        sale_price = index_id.loc[producto][3]
        final_price = index_id.loc[producto][4]
        cost = index_id.loc[producto][5]
        storage = index_id.loc[producto][6]

        precios[str(producto)]['nombre'] = index_id.loc[producto][0]
        precios[str(producto)]['sale_price'] = sale_price
        precios[str(producto)]['final_price'] = final_price
        precios[str(producto)]['cost'] = cost
        precios[str(producto)]['storage'] = storage
    
    return precios
