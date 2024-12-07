# LIBS
import pandas as pd
import numpy as np
import csv

# LECTURA DE ARCHIVOS
with open("embedding.txt", "r") as archivo:
    lineas = archivo.readlines()

# Lectura de cant y dimensiones    
N, dim = lineas[0].split()

N = int(N)
dim = int(dim)
 
# Generamos datos
lineas = lineas[1:]
lineas.sort(key=lambda str: int(str.split()[0])) # Ordenamos los nodos

datos = [list(map(float, linea.split())) for linea in lineas]

# ESCRIBIMOS EL CSV
with open("vec_emb.csv", "w", newline="") as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerows(datos)

print(f"\n'vec_emb.csv' creado. Primer columna el indice de \nla fila que representa el resto las {dim} coordenadas\n")
 



    