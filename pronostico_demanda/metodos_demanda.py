from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from pmdarima import auto_arima
import math
import numpy as np
import pandas as pd




# MAE
# https://datagy.io/mae-python/

def mae(y_true, predictions):
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))



def promedio_movil_simple(dicc_branch, item):

    data = dicc_branch[item]
    data2 = data.copy()
    data = data2.drop(columns=['item_id'])
    
    #datos: [semana, quantity]
    
    data_training = data[:math.floor(int((len(data)*2/3)))+1]
    data_test = data[-math.ceil((int(len(data)*1/3))):]
    data_training['MA'] = data_training['quantity'].rolling(window=4).mean().shift(1)
    data_forecast = data_training.copy()

    #producir pronóstico 
    for i in range(len(data_test)):
        data_forecast.loc[len(data_forecast)]=[data_forecast.iloc[len(data_forecast)-1][0] + 1, 0, 0]
        data_forecast['MA'] = data_forecast['quantity'].rolling(window=4).mean().shift(1)
        data_forecast['quantity'].loc[len(data_forecast)-1] = data_forecast['MA'].loc[len(data_forecast)-1]
        data_forecast.loc[len(data_forecast)]=[data_forecast.iloc[len(data_forecast)-1][0] + 1, 0, 0]
        data_forecast['MA'] = data_forecast['quantity'].rolling(window=4).mean().shift(1)
        data_forecast['quantity'].loc[len(data_forecast)-2] = data_test['quantity'].iloc[i]

    mae_ = mae(data_test['quantity'], data_forecast['MA'][-len(data_test):])

    return [data_forecast['MA'][-2:], mae_]


def suavizacion_exp_simp(dicc_branch, item):
    
    data = dicc_branch[item]
    print(data)
    
    data2 = data.copy()
    data = data2.drop(columns=['item_id'])
    
    #datos: [semana, quantity]

    data_training = data[:math.floor(int((len(data)*2/3)))+1]
    data_test = data[-math.ceil((int(len(data)*1/3))):]
    
    data_forecast = pd.DataFrame()
    data_forecast['test'] = None
    data_forecast['SES 1'] = None
    data_forecast['SES 2'] = None
    
    
    for i in range(0, len(data_test)):
        ses_model = SimpleExpSmoothing(np.asarray(data_training['quantity'])).fit(smoothing_level=0.3, optimized=False)
        forecast = ses_model.forecast(2)
        data_forecast.loc[len(data_forecast)] = [data_test.iloc[i][1], forecast[0], forecast[1]]
        data_training.loc[len(data_training)] = [data_test.iloc[i][0], data_test.iloc[i][1]]

    #print("\n", list(data_forecast['SES 1'])[-1], "\n")
    #print("\n", data_forecast['SES 2'], "\n")

    mae_ = mae(data_test['quantity'], data_forecast['SES 1'])
    valor1 = list(data_forecast['SES 1'])[-1]
    valor2 = list(data_forecast['SES 2'])[-1]

    return [valor1, valor2, mae_]


def suavizacion_exp_doble(dicc_branch, item):
    
    data = dicc_branch[item]
    
    data2 = data.copy()
    data = data2.drop(columns=['item_id'])
    
    #datos: [semana, quantity]

    data_training = data[:math.floor(int((len(data)*2/3)))+1]
    data_test = data[-math.ceil((int(len(data)*1/3))):]
    
    data_forecast = pd.DataFrame()
    data_forecast['test'] = None
    data_forecast['SED 1'] = None
    data_forecast['SED 2'] = None
    
    for i in range(0, len(data_test)):
        sed_model = Holt(np.asarray(data_training['quantity'])).fit(smoothing_level = 0.3, smoothing_slope = 0.2)
        forecast = sed_model.forecast(2)
        data_forecast.loc[len(data_forecast)] = [data_test.iloc[i][1], forecast[0], forecast[1]]
        data_training.loc[len(data_training)] = [data_test.iloc[i][0], data_test.iloc[i][1]]

    mae_ = mae(data_test['quantity'], data_forecast['SED 1'])
    return [data_forecast['SED 1'][-1], data_forecast['SED 2'][-1], mae_]
    


def suavizacion_exp_triple(dicc_branch, item):
    
    data = dicc_branch[item]
    
    data2 = data.copy()
    data = data2.drop(columns=['item_id'])
    
    #datos: [semana, quantity]

    data_training = data[:math.floor(int((len(data)*2/3)))+1]
    data_test = data[-math.ceil((int(len(data)*1/3))):]
    
    data_forecast = pd.DataFrame()
    data_forecast['test'] = None
    data_forecast['SET 1'] = None
    data_forecast['SET 2'] = None
    
    for i in range(0, len(data_test)):
        
        set_model = ExponentialSmoothing(np.asarray(data_training['quantity']) ,seasonal_periods=2 ,trend='add', seasonal='add',).fit()
        forecast = set_model.forecast(2)
        data_forecast.loc[len(data_forecast)] = [data_test.iloc[i][1], forecast[0], forecast[1]]
        data_training.loc[len(data_training)] = [data_test.iloc[i][0], data_test.iloc[i][1]]

    mae_ = mae(data_test['quantity'], data_forecast['SET 1'])
    return [data_forecast['SET 1'][-1], data_forecast['SET 2'][-1]], mae_


def sarima(dicc_branch, item):
    
    data = dicc_branch[item]
    
    data2 = data.copy()
    data = data2.drop(columns=['item_id'])
    
    #datos: [semana, quantity]

    data_training = data[:math.floor(int((len(data)*2/3)))+1]
    data_test = data[-math.ceil((int(len(data)*1/3))):]
    
    data_forecast = pd.DataFrame()
    data_forecast['test'] = None
    data_forecast['sarima 1'] = None
    data_forecast['sarima 2'] = None

    for i in range(0, len(data_test)):
        
        model = auto_arima(y=np.asarray(data_training['quantity']), m=6)
        forecast = pd.Series(model.predict(n_periods = 2))
        data_forecast.loc[len(data_forecast)] = [data_test.iloc[i][1], forecast[0], forecast[1]]
        data_training.loc[len(data_training)] = [data_test.iloc[i][0], data_test.iloc[i][1]]

    mae_ = mae(data_test['quantity'], data_forecast['sarima 1'])
    return [data_forecast['sarima 1'][-1], data_forecast['sarima 2'][-1]], mae_
