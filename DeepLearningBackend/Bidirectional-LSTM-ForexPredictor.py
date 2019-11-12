#!/usr/bin/env python
# coding: utf-8

# ## Forex Predictor LSTM

# In[1]:


import keras.backend as K
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from keras.callbacks import LearningRateScheduler
from keras.callbacks import ModelCheckpoint
from keras.layers import *
from keras.models import Sequential
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MinMaxScaler

from config import *

df = pd.read_csv("EURUSD_15m_BID_01.01.2010-31.12.2016.csv")
print(df.count())

# Rename bid OHLC columns
df.rename(columns={'Time': 'timestamp', 'Open': 'open', 'Close': 'close',
                   'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True)
df.set_index('timestamp', inplace=True)
df = df.astype(float)

# Add additional features
df['momentum'] = df['volume'] * (df['open'] - df['close'])
df['avg_price'] = (df['low'] + df['high']) / 2
# df['range'] = df['high'] - df['low']
df['ohlc_price'] = (df['low'] + df['high'] + df['open'] + df['close']) / 4
df['oc_diff'] = df['open'] - df['close']

print(df.head())


def create_dataset(dataset, look_back=20):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return np.array(dataX), np.array(dataY)


# Scale and create datasets
target_index = df.columns.tolist().index('close')
high_index = df.columns.tolist().index('high')
low_index = df.columns.tolist().index('low')
dataset = df.values.astype('float32')

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# Create y_scaler to inverse it later
y_scaler = MinMaxScaler(feature_range=(0, 1))
t_y = df['close'].values.astype('float32')
t_y = np.reshape(t_y, (-1, 1))
y_scaler = y_scaler.fit(t_y)

X, y = create_dataset(dataset, look_back=50)
y = y[:, target_index]

train_size = int(len(X) * 0.99)
trainX = X[:train_size]
trainY = y[:train_size]
testX = X[train_size:]
testY = y[train_size:]


# ## Model creation

# In[6]:


model = Sequential()
model.add(
    Bidirectional(LSTM(90, input_shape=(X.shape[1], X.shape[2]),
                       return_sequences=True),
                  merge_mode='sum',
                  weights=None,
                  input_shape=(X.shape[1], X.shape[2])))
model.add(LSTM(30, return_sequences=True))
model.add(LSTM(20, return_sequences=True))
model.add(LSTM(10, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(4, return_sequences=False))
model.add(Dense(4, kernel_initializer='uniform', activation='relu'))
model.add(Dense(1, kernel_initializer='uniform', activation='relu'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae', 'mse'])
print(model.summary())


# In[7]:


checkpoint = ModelCheckpoint(bi_rnn_weights,
                                 monitor='val_mean_squared_error',
                                 verbose=1,
                                 save_best_only=True,
                                 mode='min')
callbacks_list = [checkpoint]


# In[8]:


history = model.fit(trainX, trainY, epochs=10, batch_size=1024, verbose=1, callbacks=callbacks_list,
                        validation_split=0.1)


# In[ ]:


model.load_weights(bi_rnn_weights)


# ## Benchmark

# In[ ]:


pred = model.predict(testX)
pred = y_scaler.inverse_transform(pred)
close = y_scaler.inverse_transform(np.reshape(testY, (testY.shape[0], 1)))
predictions = pd.DataFrame()
predictions['predicted'] = pd.Series(np.reshape(pred, (pred.shape[0])))
predictions['close'] = pd.Series(np.reshape(close, (close.shape[0])))
predictions['diff'] = predictions['predicted'] - predictions['close']


# In[ ]:


p = df[-pred.shape[0]:].copy()
predictions.index = p.index
predictions = predictions.astype(float)
predictions = predictions.merge(p[['low', 'high']], right_index=True, left_index=True)


# In[ ]:


flattened = pd.DataFrame(predictions.to_records())
flattened['forex_pair']="EURUSD"
flattened['timestamp']=flattened.timestamp.apply(lambda x: x.strftime('%Y%m%d %H:%M:%S'))
flattened['decision']=""


# In[ ]:


flattened.loc[flattened['diff'] > 0, 'decision'] = 'sell'
flattened.loc[flattened['diff'] == 0, 'decision'] = 'hold'
flattened.loc[flattened['diff'] < 0, 'decision'] = 'buy'


# In[ ]:


flattened.head(10)


# In[ ]:


result=flattened[['forex_pair','timestamp','decision']]


# In[ ]:


data=result.to_json(orient='records')


# In[ ]:


import io, json
with io.open('predictions.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(data, ensure_ascii=False))


# In[ ]:




