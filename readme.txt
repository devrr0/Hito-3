MATCHES DE NODOS:

lf_min_age        match: d_age
lf_max_age
-----------------------------------
lf_location       match: d_country
-se seleccionaron solo los 25 paises mas representativos
-----------------------------------
lf_single         match: d_relationship
-se filtro desde un principio, ya que todos buscan solterxs
----------------------------------- 
lf_for            match: lf_for
-----------------------------------
lf_want           match: gender_orientation
-se consideraron solo las clases mas relevantes: Men, Women, Everybody
----------------------------------- 


METODOLOGIA:

1. OBTENER GRAFO EN FORMATO PUNTO TXT: CREAR_GRAFO.py -> grafo_real.txt

copy:       python CREAR_GRAFO.py 

2. OBTENER EMBEDING DEL GRAFO EN ESPACIO VECTORIAL CON Node2Vec: Node2Vec/main.py -> embedding.txt

copy:       python Node2Vec/main.py --input grafo_real.txt --output embedding.txt

3. OBTENER ENBEDDING EN FORMATO CSV: CREAR_CSV.py -> vec_emb.csv

copy:       python CREAR_CSV.py 

4. CLUSTERIZAR LOS DATOS  Y OBTENER CLUSTERS: CLUSTER.ipynb -> cluster.txt
5. ANALIZAR CLUSTER CON LOS DATOS: ANALIZAR.ipynb
 



