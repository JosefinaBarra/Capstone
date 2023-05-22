
import numpy as np
import pandas as pd

from simulacion_diario import Bodega
from funciones import histogramas_png, generar_demanda
#from abrir_archivo import demanda


np.random.seed(0)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

excel = pd.ExcelWriter('sample_data.xlsx')

replicas = 100
periodos = 30
#politica = "(s,S)"
politica = "EOQ"   

resultado = {}
resultado_base = {}

caso_base = True
no_mostro_grafico_base = True

# Demanda real
#print(demanda)

# Demanda simulada
demanda = generar_demanda(periodos)


prom_demanda = np.mean(list(demanda.values()))


valores_politica = []
for i in range(1, 4):
    valores_politica.append((np.ceil(prom_demanda/i), np.ceil((i+1)*prom_demanda)))


#valores_politica = [
#    (prom_demanda,5000), (prom_demanda/2,5000), (prom_demanda/3,5000),
#    (prom_demanda,4000), (prom_demanda/2,4000), (prom_demanda/3,4000),
#    (prom_demanda,3000), (prom_demanda/2,3000), (prom_demanda/3,3000),
#    (prom_demanda,2000), (prom_demanda/2,2000), (prom_demanda/3,2000),
#    (prom_demanda,1000), (prom_demanda/2,1000), (prom_demanda/3,1000)
#]


print(f"\nESTADÍSTICAS SIMULACIÓN")
for valores in valores_politica:
    muestra_grafico = True
    resultado[str(valores)] = {}
    print(f"\nPOLÍTICA {valores}")
    for i in range(0, replicas):
        s = Bodega(valores[0], valores[1], politica, periodos, demanda)
        s.run()
        
        if muestra_grafico:
            s.grafico()
            muestra_grafico = False

        resultado[str(valores)]["repeticion"+str(i)] = s.guardar_kpi()

# Se guardan kpi por repetición en excel
print(f"\nESTADÍSTICAS KPI")
for valores in valores_politica:
    print(f"\nPOLÍTICA {valores}")
    resultado_kpi = resultado[str(valores)]
    rows = []
    for j in range(0, replicas):
        kpi = resultado_kpi["repeticion"+str(j)]
        rows.append(list(kpi.values()))
    df = pd.DataFrame(rows, columns = list(kpi.keys()))
    df.to_excel(excel, sheet_name='kpi'+str(valores), index=True)
    
    # Muestra el promedio de los kpi por política
    print(df.describe().transpose())
    print("-"*20)
    print("\n")
    
excel.save()
excel.close()

# Guardo histogramas de kpi en carpetas
# histogramas_png(valores_politica, replicas)
