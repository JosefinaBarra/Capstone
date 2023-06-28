from gurobipy import *
from gurobipy import GRB, Model, quicksum
import gurobipy as gp
import numpy
import pandas as pd


# Lee el archivo Excel
def par_optimo(producto, sucursal):
    df = pd.read_excel(str(producto)+'/'+str(producto)+'sucursal_'+str(sucursal)+'.xlsx', sheet_name='Mean')

    max_balance = df['Balance [$]'].max()
    print(f'max balance = {max_balance}')
    if max_balance <= 0:
        print(f' ERROR: Max_balance = {max_balance}')
        return 'error'
    else:

        df['Balance [%]'] = (df['Balance [$]']/max_balance)*100
        print(df.head())

        filas = df.shape[0]

        # Obtiene los datos de la columna "Columna1"
        nivel_s = df['Nivel servicio [%]'][:filas]
        balance = df["Balance [%]"][:filas]

        model = gp.Model()
        variables = {}
        for i in range(len(nivel_s)):
            for j in range(len(balance)):
                if i == j:
                    variables[i, j] = model.addVar(vtype=GRB.BINARY, name=f'x[{i},{j}]')

        model.addConstr(gp.quicksum(variables[i, j] for i in range(len(nivel_s)) for j in range(len(balance)) if i ==j) == 1, "restriccion_unica")

        term1 = gp.quicksum((nivel_s[i] * variables[i, j]) for i in range(len(nivel_s)) for j in range(len(balance)) if i ==j)
        term2 = gp.quicksum((balance[j] * variables[i, j]) for i in range(len(nivel_s)) for j in range(len(balance)) if i ==j)
        model.setObjective(term1 + term2, GRB.MAXIMIZE)

        model.optimize()
        count = 0
        if model.status == GRB.OPTIMAL:
            print("Solución óptima encontrada")
            print("Valor objetivo: ", model.objVal)
            for i in range(len(nivel_s)):
                for j in range(len(balance)):
                    if i == j:
                        if variables[i, j].x > 0:
                            #print("Valor de x[{},{}]: {}".format(i, j, variables[i, j].x))
                            politica_elegida = df.iloc[i][0]
                            print(politica_elegida)
                        count += 1
        return politica_elegida
