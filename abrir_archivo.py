import os

demanda_real = {}
dia = 0

with open("dda_885.txt") as f:
    contenido = f.read().split('\n')
    for linea in contenido:
        separado = linea.split()
        for i in range(0, len(separado)):
            demanda_real[dia] = int(separado[i])
            dia += 1