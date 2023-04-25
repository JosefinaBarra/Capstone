# Gestión de inventario clínica veterinaria - Grupo 9
## Profesor: Gonzalo Pérez | Ayudante: Jorge Fuenzalida
Se realiza la simulación de los datos y su gráfica usando las librerías ```simpy```, ```numpy``` y ```matplotlib```.

Primero se generan datos aleatorios para la demanda en el archivo `generacion_datos.py`, suponiendo que la demanda `d ~ Poisson(lambda)`. En ese mismo archivo se calcula la suavización de la demanda histórica según un valor $\alpha$ en la función `suavizacion_demanda(demanda, alpha)`.

Las políticas de inventario simuladas son:
* Política min-max: Archivo `min_max.py`. El código se basa en el siguiente [video](https://www.youtube.com/watch?v=Kmu9DNQamLw&ab_channel=PaulGrogan)

Los métodos de pronóstico de demanda se encuentran en el archivo `pronostico_demanda.py`:
* Promedio ponderado simple: Se calcula el promedio de la demanda histórica con la función `prom_pond_simple(demanda)`.
* Suavización exponencial simple: Se calcula según la función $F_t = F_{t-1} + \alpha(A_{t-1}-F_{t-1})$ en la fórmula `suavizacion_demanda(demanda, alpha)`
