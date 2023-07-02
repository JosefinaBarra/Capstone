import numpy as np
import pandas as pd

metodos_branch0 = pd.read_excel("pronostico_demanda/metodos_branches/mejor_metodo_branch0.xlsx").drop(columns=['Unnamed: 0'])
metodos_branch4 = pd.read_excel("pronostico_demanda/metodos_branches/mejor_metodo_branch4.xlsx").drop(columns=['Unnamed: 0'])
