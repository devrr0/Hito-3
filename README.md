# Experimento 3 - Minería de Datos 

## Índice
- [Descripción](#descripción)
- [Configuración Inicial](#configuración-inicial)
- [Contribuir al Proyecto](#contribuir-al-proyecto)
- [Datos del Experimento](#datos-del-experimento)
- [Metodología](#metodología)
- [Estructura del Proyecto](#estructura-del-proyecto)

## Descripción
Usando el dataset OkCupid, un conjunto de datos que recoge información de los usuarios de la plataforma de citas OkCupid, se busca encontrar conjuntos de personas en base a compatibilidad. Para la realización de este experimento se busca generar un grafo en donde las arista dependerá de la compatibilidad entre individuos. La compatibilidad está dada por las features de tipo "lf" en la base de datos, los cuales indican las preferencias de una persona en una relación. 

Una vez armado el grafo se transformaran los nodos a vectores utilizando la técnica NodeToVector. Ya obtenidos los vectores, se ocuparán diversas técnicas de cluster (K-means, cluster estratificado, DBSCAN, etc) para clusterizar los datos. Una vez etiquetados los datos se analizarán los distintos grupos encontrados en relación con el resto de columnas de la base de datos (por ejemplo: ideología política, tipo de religión, uso de drogas, etnia, etc).

## Configuración Inicial

1. Clonar el Repositorio

```bash
git clone https://github.com/devrr0/Hito-3.git
cd Hito-3
```

2. Crear y activar un entorno virtual para aislar las dependencias del proyecto

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar las dependencias necesarias con el entorno virtual activado.

```bash
pip install -r requirements.txt
```

Ya estás dentro del proyecto de git
```bash
git status  # estado de la rama
git fetch   # ver si hay novedades
git pull    # actualizar el proyecto
```

## Contribuir al Proyecto

1. Crear una nueva rama: 

Antes de trabajar en una nueva funcionalidad crea una nueva rama a partir de master.

```bash
git checkout master
git pull origin master
git checkout -b feature-nueva-funcionalidad
```

2. Hacer cambios y confirmar:

Realiza los cambios en tu rama y asegúrate de hacer commits con mensajes claros

```bash
git add .
git commit -m "Add: Implementar nueva funcionalidad X"
```

3. Subir la Rama de Funcionalidad al Repositorio Remoto

Sube tus cambios al repositorio remoto para que otros puedan revisarla.

```bash
git push origin feature-nueva-funcionalidad
```

4. Abrir un Pull Request 

Ve a GitHub y abre un Pull Request desde la rama feature-nueva-funcionalidad hacia master. El PR permite que otros miembros revisen los cambios antes de que se fusionen en la rama master.

5. Revisar y Fusionar el Pull Request
Después de que haya sido revisado y aprobado.

 Fusiona la rama feature-nueva-funcionalidad en master. Esto se hace en la interfaz de GitHub haciendo clic en "Merge pull request".


## Datos del experimento

Para la construcción del grafo se utilizaron distintas columnas para indicar una compatibilidad en cuanto a edad, país, estado de relación y orientación sexual.

```bash
# match: d_age
df['lf_min_age']
df['lf_max_age']

# match: d_country
df['lf_location']   # se seleccionaron los 25 paises mas representativos

# match: d_relationship
df['lf_single']

# match: lf_for
df['lf_for']

# match: gender_orientation
df['lf_want']       # se consideraron solo las 3 clases mas relevantes
```


## Metodología

1. Obtener grafo en formato TXT 

```bash
cd experiment
python CREAR_GRAFO.py 
```

2. Obtener embedding del grafo en espacio vertical con Node2Vec

```bash
python Node2Vec/main.py --input grafo_real.txt --output embedding.txt
```

3. Obtener embedding en formato CSV

```bash
python CREAR_CSV.py 
```
4. Clusterizar los datos y obtener clusters

5. Analizar clusters con los datos
 

## Estructura del Proyecto

```bash
Hito-3/
├── experiment/                         # Código y configuración del experimento
│   ├── Data/                           # Datos
│   │   ├──parsed_data_public.parquet   # Base de datos respuestas
│   │   ├──question_data.csv            # Base de datos preguntas
│   │   └──test_items.csv               # Base de datos items
│   ├── Node2Vec/                       # Implementación técnica NodeToVector
│   │   ├── __pycache__/                 
│   │   ├── main.py                      
│   │   └── node2vec.py                  
│   ├── ANALIZAR.ipynb                  # Anáñisis de los clusters
│   ├── CLUSTER.ipynb                   # Implementación de los clusters
│   ├── cluster.txt                     # Obtener los clusters
│   ├── CREAR_CSV.py                    # Construcción embedding a CSV
│   ├── CREAR_GRAFO.py                  # Construcción del grafo
│   ├── embedding.txt                   # Embedding del grafo
│   ├── grafo_real.txt                  # Grafo original
│   └── vec_emb.csv                     # Embedding 
├── requirements.txt                    # Requerimientos del proyecto
└── README.md                           # Documentación del proyecto
```


