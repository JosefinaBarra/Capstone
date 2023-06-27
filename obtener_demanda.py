from pronostico_demanda.metodos_demanda import promedio_movil_simple, suavizacion_exp_simp, suavizacion_exp_doble,suavizacion_exp_triple, sarima
from pronostico_demanda.mejores_metodos import metodos_branch0
from pronostico_demanda.cargar_datos import *
import warnings
warnings.filterwarnings('ignore')

def obtener_pronostico(branch, item):
    set_metodo = metodos_branch0.loc[metodos_branch0['item'] == item]
    metodo = set_metodo['metodo'].iloc[0]

    if metodo == "pms":
        resultado = promedio_movil_simple(dicc_branch0, item)
        print([resultado[0].iloc[0], resultado[0].iloc[1], resultado[1]])
        return [resultado[0].iloc[0], resultado[0].iloc[1], resultado[1]]
    elif metodo == "ses":
        return print(suavizacion_exp_simp(dicc_branch0, item))
    elif metodo == "sed":
        return print(suavizacion_exp_doble(dicc_branch0, item))
    elif metodo == "set":
        return print(suavizacion_exp_triple(dicc_branch0, item))
    elif metodo == "sar":
        return print(sarima(dicc_branch0, item))


obtener_pronostico(0, 2)


