import numpy as np
def local_search(matriz, columnas):
    coordenadas = np.lexsort((matriz[0], matriz[11], -matriz[8]))
    mejor_coordenada = np.unravel_index(coordenadas[0], matriz[0].shape)
    print("Mejor coordenada:")
    print("Fila:", mejor_coordenada[0])
    print("Columna:", mejor_coordenada[1])
