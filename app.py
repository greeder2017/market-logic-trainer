import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("Market Logic Trainer - Structure Version")

# --- Generate Simulated Market Data ---
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

# --- Replay ---
step = st.slider("Replay Candle", 20, len(df), 100)
chart_data = df.iloc[:step]

st.line_chart(chart_data["Close"])

# --- Structure Detection ---
lookback = 3

def detect_structure(data):
    swings_high = []
    swings_low = []

    for i in range(lookback, len(data)-lookback):
        high_range = data["Close"][i-lookback:i+lookback+1]
        if data["Close"][i] == max(high_range):
            swings_high.append((i, data["Close"][i]))

        if data["Close"][i] == min(high_range):
            swings_low.append((i, data["Close"][i]))

    return swings_high, swings_low

swings_high, swings_low = detect_structure(chart_data)
# --- Liquidity Detection (Equal Highs / Lows) ---
liquidity_highs = []
liquidity_lows = []

tolerance = 0.2  # how close prices must be to count as equal

if len(swings_high) >= 2:
    last_high = swings_high[-1][1]
    prev_high = swings_high[-2][1]
    if abs(last_high - prev_high) < tolerance:
        liquidity_highs.append(last_high)

if len(swings_low) >= 2:
    last_low = swings_low[-1][1]
    prev_low = swings_low[-2][1]
    if abs(last_low - prev_low) < tolerance:
        liquidity_lows.append(last_low)
if len(swings_low) >= 2:
    last_low = swings_low[-1][1]
    prev_low = swings_low[-2][1]
    if abs(last_low - prev_low) < tolerance:
        liquidity_lows.append(last_low)

if len(swings_low) >= 2:
    last_low = swings_low[-1][1]
    prev_low = swings_low[-2][1]
    if abs(last_low - prev_low) < tolerance:
        liquidity_lows.append(last_low)

# --- Sweep Detection ---
sweep_high = False
sweep_low = False

current_price = chart_data["Close"].iloc[-1]

if liquidity_highs:
    if current_price > liquidity_highs[-1]:
        sweep_high = True

if liquidity_lows:
    if current_price < liquidity_lows[-1]:
        sweep_low = True

liquidity_highs = []
liquidity_lows = []

tolerance = 0.2  # how close prices must be to count as equal

if len(swings_high) >= 2:
    last_high = swings_high[-1][1]
    prev_high = swings_high[-2][1]
    if abs(last_high - prev_high) < tolerance:
        liquidity_highs.append(last_high)

if len(swings_low) >= 2:
    last_low = swings_low[-1][1]
    prev_low = swings_low[-2][1]
    if abs(last_low - prev_low) < tolerance:
        liquidity_lows.append(last_low)

# --- Determine Bias ---
bias = "RANGE"

if len(swings_high) >= 2 and len(swings_low) >= 2:
    if swings_high[-1][1] > swings_high[-2][1] and swings_low[-1][1] > swings_low[-2][1]:
        bias = "BULLISH"
    elif swings_high[-1][1] < swings_high[-2][1] and swings_low[-1][1] < swings_low[-2][1]:
        bias = "BEARISH"

st.subheader("Structure Panel")
st.subheader("Liquidity Panel")

if liquidity_highs:
    st.write("Equal Highs Detected ✅")
else:
    st.write("Equal Highs Detected ❌")

if liquidity_lows:
    st.write("Equal Lows Detected ✅")
else:
    st.write("Equal Lows Detected ❌")
if sweep_high:
    st.write("Liquidity HIGH Swept 🚨")

if sweep_low:
    st.write("Liquidity LOW Swept 🚨")

st.write(f"Current Bias: **{bias}**")
st.write(f"Swing Highs Detected: {len(swings_high)}")
st.write(f"Swing Lows Detected: {len(swings_low)}")

# --- Trade Panel ---
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
st.info("Next: Liquidity detection + entry validation")
