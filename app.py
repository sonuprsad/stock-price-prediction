import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from auth import login_user, register_user
from utils import add_indicators, generate_signal
from model import train_model, predict_next

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

st.sidebar.title(" Login/Register")

option = st.sidebar.selectbox("Select", ["Login", "Register"])

if option == "Register":
    new_user = st.sidebar.text_input("Username")
    new_pass = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Register"):
        if register_user(new_user, new_pass):
            st.sidebar.success("Registered! Now login.")
        else:
            st.sidebar.error("User already exists")

elif option == "Login":
    user = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if login_user(user, password):
            st.session_state['login'] = True
            st.session_state['user'] = user
        else:
            st.sidebar.error("Invalid credentials")

if 'login' not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.title(f"📈 Welcome {st.session_state['user']}")

data_source = st.sidebar.radio("Data Source", ["Upload CSV",])

df = None

if data_source == "Upload CSV":
    file = st.sidebar.file_uploader("Upload CSV")
    if file:
        df = pd.read_csv(file)
        if 'Date' in df.columns:
         df['Date'] = pd.to_datetime(df['Date'])
         df.set_index('Date', inplace=True)

else:
    stock = st.sidebar.text_input("Stock Symbol", "AAPL")
    df = yf.download(stock, start="2015-01-01")

if df is not None and 'Close' in df.columns:

    df = add_indicators(df)
    df = df.dropna()   

    col1, col2, col3 = st.columns(3)
    col1.metric("Price", round(df['Close'].iloc[-1],2))
    col2.metric("RSI", round(df['RSI'].iloc[-1],2))
    trend = "Bullish" if df['Close'].iloc[-1] > df['MA50'].iloc[-1] else "Bearish"
    col3.metric("Trend", trend)

    
    st.subheader("📊 Chart")
    fig = go.Figure()

    fig.add_trace(go.Scatter(y=df['Close'], name='Close'))
    fig.add_trace(go.Scatter(y=df['MA50'], name='MA50'))
    fig.add_trace(go.Scatter(y=df['EMA20'], name='EMA20'))
    fig.add_trace(go.Scatter(y=df['BB_upper'], name='BB Upper'))
    fig.add_trace(go.Scatter(y=df['BB_lower'], name='BB Lower'))
    fig.update_layout(
    title="Stock Price with Indicators",
    xaxis_title="Date",
    yaxis_title="Price"
)

    st.plotly_chart(fig, width='stretch')

    signal = generate_signal(df)

    if signal == "BUY":
        st.success("📈 BUY")
    elif signal == "SELL":
        st.error("📉 SELL")
    else:
        st.warning("⚠️ HOLD")

    if st.button("Predict Next Price"):
        model, scaler = train_model(df[['Close']])
        pred = predict_next(model, scaler, df['Close'].values)
        st.info(f"Predicted Price: {round(pred,2)}")

    st.dataframe(df.tail())

    
    st.download_button("Download CSV", df.to_csv(index=False), "report.csv")
