


from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def train_model(data):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

    X = np.arange(len(scaled_data)).reshape(-1, 1)
    y = scaled_data

    model = LinearRegression()
    model.fit(X, y)

    return model, scaler


def predict_next(model, scaler, data):
    next_day = np.array([[len(data)]])
    pred_scaled = model.predict(next_day)
    return scaler.inverse_transform(pred_scaled)[0][0]




















