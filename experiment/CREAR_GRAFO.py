#LIBS
import pandas as pd
import re
import numpy as np
import os
import time
from joblib import Parallel,delayed
from tqdm import tqdm

print("Cargando DataSet...")
t0= time()
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

print("DataSet cargado.")
#------------------------------------------------------------------------------------

# NUM NODOS Y LISTA DE INDICES
N= df.shape[0]
indices = df.index.to_list()

#  FUN DE RELACION
def w(i,j):
    X=df.iloc[i]
    Y=df.iloc[j]
    
    # LOCATION
    LOC = X["d_country"] == Y["d_country"] or (X["lf_location"] == Y["lf_location"] == "Located anywhere")
    if not LOC:
        return ""
    
    # WANT
    X_WANT = X["lf_want"] == Y["gender2"] or X["lf_want"] == "Everyone" 
    Y_WANT = Y["lf_want"] == X["gender2"] or Y["lf_want"] == "Everyone"
    WANT= X_WANT and Y_WANT
    if not WANT:
        return ""
    
    # AGE
    X_AGE= X["lf_min_age"] <= Y["d_age"] <= X["lf_max_age"]
    Y_AGE= Y["lf_min_age"] <= X["d_age"] <= Y["lf_max_age"]
    AGE = X_AGE and Y_AGE
    if not AGE:
        return ""
    
    # FOR
    x_list = X["lf_for"].split(", ")
    y_list = Y["lf_for"].split(", ")
    FOR = len(set(x_list) & set(y_list)) > 0
    if not FOR:
        return ""
    
    return f"{indices[i]} {indices[j]}\n"

# ESCRITURA DEL GRAFO

# Nombre del archivo a crear
nombre_archivo = "grafo_real.txt"
print(f"Creando '{nombre_archivo}'...")

# CREAR LINEAS CON PARALELIZACION
pares = [(i,j) for i in range(N//8) for j in range(i+1,N//8)]
lineas = Parallel(n_jobs=8)(delayed(w)(*par) for par in tqdm(pares))

# ESCRIBIR LINEAS
with open(nombre_archivo, "w") as archivo:    
    archivo.writelines(lineas)
        
print(f"\n'{nombre_archivo}' creado, programa finalizado. Tiempo total: {round((time()-t0)/3600,3)} horas")
