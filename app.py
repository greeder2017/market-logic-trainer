import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("Market Logic Trainer - Web Version")

@st.cache_data
def generate_data():
    np.random.seed(1)
    price = 100
    prices = []

    for i in range(500):
        drift = 0.02
        shock = np.random.randn() * 0.5
        price = price + drift + shock
        prices.append(price)

    df = pd.DataFrame({"Close": prices})
    return df

df = generate_data()

step = st.slider("Replay Candle", 20, len(df), 100)
chart_data = df.iloc[:step]

st.line_chart(chart_data["Close"])

st.subheader("Trade Panel")

col1, col2 = st.columns(2)

if "position" not in st.session_state:
    st.session_state.position = None
    st.session_state.entry_price = None

with col1:
    if st.button("BUY"):
        st.session_state.position = "LONG"
        st.session_state.entry_price = chart_data["Close"].iloc[-1]

with col2:
    if st.button("SELL"):
        st.session_state.position = "SHORT"
        st.session_state.entry_price = chart_data["Close"].iloc[-1]

current_price = chart_data["Close"].iloc[-1]

if st.session_state.position:
    st.write(f"Current Position: {st.session_state.position}")
    st.write(f"Entry Price: {st.session_state.entry_price:.2f}")
    st.write(f"Current Price: {current_price:.2f}")

    if st.session_state.position == "LONG":
        pnl = current_price - st.session_state.entry_price
    else:
        pnl = st.session_state.entry_price - current_price

    st.write(f"Unrealized PnL: {pnl:.2f}")

if st.button("CLOSE TRADE"):
    st.session_state.position = None
    st.session_state.entry_price = None
    st.success("Trade closed")

st.subheader("Evaluation")
st.info("Structure + Liquidity logic coming next.")
