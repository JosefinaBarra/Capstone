import numpy as np
import pandas as pd
from pprint import pprint


def data_branch(branch, item):
    path = f'pronostico_demanda/excel_branches/branch{branch}(1).xlsx'
    info_branch = pd.read_excel(path, engine='openpyxl').drop(columns=['Unnamed: 0'])

    dicc_branch = dict()
    branch = info_branch.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
    val_unicos = branch['item_id'].unique().tolist()
    for v in range(len(val_unicos)):
        item = val_unicos[v]
        b_it = branch.loc[branch['item_id']==item]
        dicc_branch[item] = b_it
    return dicc_branch

#branch0 = pd.read_excel("pronostico_demanda/excel_branches/branch0(1).xlsx").drop(columns=['Unnamed: 0'])
#branch1 = pd.read_excel("pronostico_demanda/excel_branches/branch1.xlsx").drop(columns=['Unnamed: 0'])
#branch2 = pd.read_excel("pronostico_demanda/excel_branches/branch2.xlsx").drop(columns=['Unnamed: 0'])
#branch3 = pd.read_excel("pronostico_demanda/excel_branches/branch3.xlsx").drop(columns=['Unnamed: 0']) 
#branch4 = pd.read_excel("pronostico_demanda/excel_branches/branch4.xlsx").drop(columns=['Unnamed: 0'])
#branch5 = pd.read_excel("pronostico_demanda/excel_branches/branch5.xlsx").drop(columns=['Unnamed: 0'])
#branch6 = pd.read_excel("pronostico_demanda/excel_branches/branch6.xlsx").drop(columns=['Unnamed: 0'])
#branch7 = pd.read_excel("pronostico_demanda/excel_branches/branch7.xlsx").drop(columns=['Unnamed: 0'])
#branch8 = pd.read_excel("pronostico_demanda/excel_branches/branch8.xlsx").drop(columns=['Unnamed: 0'])
#branch9 = pd.read_excel("pronostico_demanda/excel_branches/branch9.xlsx").drop(columns=['Unnamed: 0'])
#branch10 = pd.read_excel("pronostico_demanda/excel_branches/branch10.xlsx").drop(columns=['Unnamed: 0'])
'''
dicc_branch0 = dict()
branch = branch0.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch0[item] = b_it

dicc_branch1 = dict()
branch = branch1.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch1[item] = b_it

dicc_branch2 = dict()
branch = branch2.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch2[item] = b_it

dicc_branch3 = dict()
branch = branch3.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch3[item] = b_it

dicc_branch4 = dict()
branch = branch4.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch4[item] = b_it

dicc_branch5 = dict()
branch = branch5.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch5[item] = b_it

dicc_branch6 = dict()
branch = branch6.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch6[item] = b_it

dicc_branch7 = dict()
branch = branch7.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch7[item] = b_it

dicc_branch8 = dict()
branch = branch8.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch8[item] = b_it

dicc_branch9 = dict()
branch = branch9.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch9[item] = b_it

dicc_branch10 = dict()
branch = branch10.groupby(['item_id', 'semana'], as_index=False).agg({'quantity': 'sum'})
val_unicos = branch['item_id'].unique().tolist()
for v in range(len(val_unicos)):
    item = val_unicos[v]
    b_it = branch.loc[branch['item_id']==item]
    dicc_branch10[item] = b_it
'''