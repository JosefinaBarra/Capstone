# Gestión de inventario clínica veterinaria - Grupo 9
## Profesor: Gonzalo Pérez | Ayudante: Jorge Fuenzalida

Para iniciar la simulación se deben tener las librerías de Python: `Numpy`, `Pandas` y `Matplotlib` y se debe correr el archivo `main.py`.  
 
En el archivo `main.py` se definen los valores para la cantidad de repeticiones, periodos a simular, rango de valores para evaluar todos pares de parámetros posibles y qué política se evaluará. Por ahora se usa solamente la política $(s,S)$ y se intentó implementar la $EOQ$.  

Respecto al caso base, se usó los datos históricos de la demanda del **producto 885**. Para simularlo, primero se leen los datos del archivo `dda_885.txt` usando el archivo `arbrir_archivo.py` para tener las demandas diarias. Con esta demanda se calcula el promedio usando en el caso base. En este caso se hizo una única repetición de 30 días. El gráfico de la simulación se guarda en `graficos/caso_base.png`. 

El inicio de la simulación comienza al implementar la función `run()` del objeto `Bodega`. Este objeto representa la bodega de una sucursal y recibe los parámetros: 
- s: int 
- S: int 
- politica: string 
- periodos: int 
- precio_venta: int 
- costo_pedido: int 
- costo_almacenamiento: int 
- costo_demanda_perdida: int 
- tiempo_revision: int 
- lead_time: int 

Luego de la simulación se guardan los resultados en un diccionario de la forma: 

$$ \displaylines{\left\lbrace \\\ \hspace{3mm} '\left\(s,S\right\)' :\left\lbrace  \\\ \hspace{6mm} 'repeticion_i' :\left\lbrace KPI_0: x_0 , … , KPI_N: x_N\right\rbrace  \\\ \hspace{4mm}\right\rbrace  \\\ \right\rbrace } $$

Por lo que para cada par $(s,S)$ se almacenan los $KPI$ obtenidos en cada repetición. Con este resultado se usa la función `guardar_pares_kpi()` en el archivo `guardar_data.py` para guardar en el archivo Excel `sample_data.xlsx`, definiendo las filas como los pares de parámetros y las columnas los valores de la media de los $KPI$.  

Además, en el mismo Excel se crea por cada hoja una matriz con los $KPI$ de cada combinación evaluada. De esta matriz se guardan los gráficos de calor en una carpeta llamada graficos usando la función `guardar_matriz_heatmap_kpi()` ubicada en el archivo `guardar_data.py`. 
