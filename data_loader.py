import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)
def download_btc_data(period="5y", interval="1d"):
    ticker = yf.Ticker("BTC-USD")
    df = ticker.history(period=period, interval=interval)
    df = df.dropna()
    return df

def get_close_prices(df):
    return df["Close"].values
