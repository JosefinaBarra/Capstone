import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st


#from simulacion_diario import Bodega
from simulacion_semanal import Bodega
np.random.seed(0)

def histogramas_png(valores_politica, replicas):
    actual_path = os.getcwd()

    for valores in valores_politica:
        folder = str(valores[0])+","+str(valores[1])
        dir = os.path.join(actual_path, folder)
        if not os.path.exists(dir):
            os.makedirs(dir)
        df = pd.read_excel('sample_data.xlsx', "kpi"+str(valores), engine='openpyxl')

        print(f"POLIICA {valores}")
        for i in range(1, len(df.columns)):
            intervalo = st.norm.interval(alpha=0.95, loc=np.mean(df.iloc[:,i]), scale=st.sem(df.iloc[:,i]))
            intervalo2 = st.t.interval(alpha = 0.95, df = len(df.iloc[:,i])-1, loc = np.mean(df.iloc[:,i]), scale = st.sem(df.iloc[:,i]))

            x_barra = np.mean(df.iloc[:,i])
            SE = np.std(df.iloc[:,i])/np.sqrt(replicas)

            izq = x_barra - 1.96*SE
            der = x_barra + 1.96*SE

            if not (np.isnan(intervalo[0]) and np.isnan(intervalo[1])):
                fig = plt.figure()
                plt.hist(df.iloc[:,i],bins=25, alpha=0.6, color='b')

                xmin, xmax = plt.xlim()
                mu, std = st.norm.fit(df.iloc[:,i]) 
                #print(f"{mu} - {std}")

                x = np.linspace(xmin, xmax, replicas)
                p = st.norm.pdf(x, mu, std)
                
                plt.plot(x, p, 'k', linewidth=2)
                
                #print(f"INTERVALOS: [{izq}, {der}]")
                #plt.axvline(izq, color='#395d90')
                #plt.axvline(der, color='#395d90')
                plt.title(f"{df.columns[i]} ~ N({np.round(mu,2)}, {np.round(std,2)})")
                fig.savefig(folder+'/'+str(valores)+str(df.columns[i])+".png")


                fig2 = plt.figure()
                plt.boxplot(df.iloc[:,i],vert=False)
                plt.title(f"{df.columns[i]}")
                fig2.savefig(folder+'/box'+str(valores)+str(df.columns[i])+".png")
        print("\n")

def generar_demanda(periodos):
        ''' Genera demanda semanal según distribución '''
        demanda = {}
        for i in range(0, periodos):
            #demanda_generada = np.random.normal(144.9151, 55.5326)
            #demanda_generada = np.random.uniform(61, 1725)
            #demanda_generada = np.random.gamma(3.002389619, 0.006414003)
            #demanda_generada = np.random.poisson(0.9)
            #demanda_generada = np.random.uniform(0, 5)
            #demanda_generada = np.random.poisson(1808.913)
            demanda_generada = np.random.poisson(3.825)
            demanda[i] = demanda_generada
        return demanda