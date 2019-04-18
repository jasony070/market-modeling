from math import sqrt
from numpy import concatenate
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import load_model
from keras import backend
import numpy as np

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg

def setup():
    data = pd.read_csv(filepath_or_buffer="./static/data2.csv", index_col="date")
    data = data.apply(pd.to_numeric, errors = "coerce")
    data['spindx'].replace(0, np.nan, inplace=True)
    data['spindx'].fillna(method='ffill', inplace=True)

    number_of_variables = 8
    values = data[['spindx'] + ['TCMNOM_Y2'] + ['TCMNOM_Y10'] + ['DCOILBRENTEU'] + ['GOLDPMGBD228NLBM'] + ['exalus'] + ['exjpus'] + ['exukus']].values
    values = values.astype('float32')

    historic_data = np.array([])
    for day in values[-10:]:
        historic_data = np.concatenate((historic_data, day), axis=None)

    historic_data = np.append (historic_data, historic_data[:8])
    look_back = 10
    time_steps = 1
    reframed = series_to_supervised(values, look_back, time_steps)

    return values, reframed, historic_data
    # return values, historic_data.reshape(1,1,historic_data.shape[0])

def predict(num=1):
    num = int(num)
    # values, pred_para = setup()
    values, reframed, historic_data = setup()

    reframed = reframed.append(dict(zip(reframed.columns, historic_data)), ignore_index=True)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_pred = scaler.fit_transform(reframed)

    pred_para = scaled_pred[-1][:-8]
    pred_para = pred_para.reshape(1,10,8)

    backend.clear_session()
    multi_model = load_model("./static/lstm2.hdf5")

    graph = []
    for row in values[-30:]:
        graph.append(row)

    while num != 0:
      yhat = multi_model.predict(pred_para)

      pred_para = pred_para.reshape((1,80))
      pred = concatenate((pred_para[:, :], yhat), axis=1)
      inv_pred = scaler.inverse_transform(pred)
      graph.append(inv_pred[:,-8:].flatten())
      pred_para = np.concatenate((pred_para.flatten()[8:], yhat[0]))
      pred_para = pred_para.reshape(1,10,8)

      # graph.append(yhat[0][0])
      # pred_para = np.concatenate((pred_para.flatten()[8:], yhat[0][0]))
      # pred_para = pred_para.reshape(1,1, pred_para.shape[0])

      num -= 1

    chartist = [[],[],[],[],[],[],[],[]]
    for row in graph:
      chartist[0].append(row[0])
      chartist[4].append(row[1])
      chartist[5].append(row[2])
      chartist[7].append(row[3])
      chartist[6].append(row[4])
      chartist[3].append(row[5])
      chartist[1].append(row[6])
      chartist[2].append(row[7])
    return chartist
