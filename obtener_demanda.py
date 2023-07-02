from pronostico_demanda.metodos_demanda import promedio_movil_simple, suavizacion_exp_simp, suavizacion_exp_doble,suavizacion_exp_triple, sarima
from pronostico_demanda.mejores_metodos import metodos_branch0, metodos_branch4
from pronostico_demanda.cargar_datos import data_branch
import warnings
warnings.filterwarnings('ignore')


def obtener_pronostico(branch, item):
    if branch == branch:
        set_metodo = metodos_branch0.loc[metodos_branch0['item'] == item]
    else:
        set_metodo = metodos_branch4.loc[metodos_branch0['item'] == item]

    metodo = set_metodo['metodo'].iloc[0]
    #print(f'metodo: {metodo}')

    dicc_branch = data_branch(branch, item)

    if metodo == "pms":
        #print('Metodo pms')
        resultado = promedio_movil_simple(dicc_branch, item)
        #print([resultado[0].iloc[0], resultado[0].iloc[1], resultado[1]])
        return [resultado[0].iloc[0], resultado[0].iloc[1], resultado[1]]
    elif metodo == "ses":
        #print('Metodo ses')
        return suavizacion_exp_simp(dicc_branch, item)
    elif metodo == "sed":
        #print('Metodo sed')
        return suavizacion_exp_doble(dicc_branch, item)
    elif metodo == "set":
        #print('Metodo set')
        return suavizacion_exp_triple(dicc_branch, item)
    elif metodo == "sar":
        #print('Metodo sar')
        return sarima(dicc_branch, item)


#obtener_pronostico(0, 2)


