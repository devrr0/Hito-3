#LIBS
import pandas as pd
import re
import numpy as np
import os
import time
from tqdm import tqdm

#----------------------------------------------------------------------------
# CARGAR PARQUET
df_path = os.getcwd() + "\\DATA\\parsed_data_public.parquet"

df_raw = pd.read_parquet(df_path)

# FILTRADO DE COLS

# Expresión regular para encontrar columnas que comienzan con 'q' seguida de un número
pattern = r'^q\d+'

# Filtrar las columnas que NO cumplen con el patrón
columnas_filtradas = [col for col in df_raw.columns if not re.match(pattern, col)]

df = df_raw[columnas_filtradas]

# Filtramos para tener solo lascols necesarias
columnas_filtro = [col for col in df.columns if col[0:2]=="lf"] + ["d_age","d_country","gender2","d_relationship"]

# Col relevantes
df = df[columnas_filtro]

# Filtrado de filas
# Filas en blancos
df = df[df.isna().sum(axis=1) == 0]

# Generos sencillos
df = df[df["lf_want"].isin(["Women","Men","Everyone"])]
df["lf_want"] = df["lf_want"].replace("Men","Man")
df["lf_want"] = df["lf_want"].replace("Women","Woman")

# Paises comunes
top_paises=df["d_country"].value_counts().head(25).index
df = df[df["d_country"].isin(top_paises)]

# Solterx
df = df[df["d_relationship"]=="Single"]

#------------------------------------------------------------------------------------

# NUM NODOS Y LISTA DE INDICES
N= df.shape[0]
indices = df.index.to_list()

#  FUN DE RELACION
def w(i,j):
    X=df.iloc[i]
    Y=df.iloc[j]
    
    # AGE
    X_AGE= int((X["lf_min_age"] <= Y["d_age"]) and (X["lf_max_age"] >= Y["d_age"]))
    Y_AGE= int((Y["lf_min_age"] <= X["d_age"]) and (Y["lf_max_age"] >= X["d_age"]))
    AGE = X_AGE*Y_AGE

    # WANT
    if X["lf_want"] == "Everyone":
        X_WANT=1
    else:
        X_WANT = int(X["lf_want"] == Y["gender2"])

    if Y["lf_want"] == "Everyone":
        Y_WANT=1
    else:
        Y_WANT = int(Y["lf_want"] == X["gender2"])

    WANT= X_WANT * Y_WANT
    
    # LOCATION
    if (X["lf_location"] == "Near me") or (Y["lf_location"] == "Near me"):
        LOC=int(X["d_country"]==Y["d_country"])
    else:
        LOC=1    

    # FOR
    x_list = X["lf_for"].split(", ")
    y_list = Y["lf_for"].split(", ")
    e_for = len(set(x_list) & set(y_list))
    
    if e_for > 0:
        FOR = 1
    else:
        FOR = 0
    
    return bool(AGE*WANT*LOC*FOR)

# ESCRITURA DEL GRAFO

# Nombre del archivo a crear
nombre_archivo = "grafo_real.txt"

# Crear y escribir el archivo
with open(nombre_archivo, "w") as archivo:    
    for i in tqdm(range(N)):
        for j in range(i+1,N):
            if w(i,j):
                archivo.write(f"{indices[i]} {indices[j]}\n")
        
        # Borra la línea anterior sobrescribiéndola con espacios
        #print(f"\r{' ' * 50}", end="",flush=True)  # Limpia la línea actual
        #print(f"\r{round((100*(i+1))/(N//10),2)}% de grafo completado", end="",flush=True)
        
        # Pausa para simular tiempo de procesamiento
        #time.sleep(0.001)

print("\n'grafo_real.txt' creado, programa finalizado.\n")
