import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def train_model(data):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
    model.add(LSTM(50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=5, batch_size=32, verbose=0)

    return model, scaler


def predict_next(model, scaler, data):
    last_60 = data[-60:]
    scaled = scaler.transform(last_60.reshape(-1,1))

    X_test = np.array([scaled])
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    pred = model.predict(X_test, verbose=0)
    return scaler.inverse_transform(pred)[0][0]