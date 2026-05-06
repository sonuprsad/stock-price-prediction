import pandas as pd
import numpy as np

def add_indicators(df):
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['BB_upper'] = df['Close'].rolling(20).mean() + 2 * df['Close'].rolling(20).std()
    df['BB_lower'] = df['Close'].rolling(20).mean() - 2 * df['Close'].rolling(20).std()

    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

def generate_signal(df):
    latest = df.iloc[-1]

    if latest['Close'] > latest['MA50'] and latest['RSI'] < 70:
        return "BUY"
    elif latest['Close'] < latest['MA50'] and latest['RSI'] > 30:
        return "SELL"
    else:
        return "HOLD"