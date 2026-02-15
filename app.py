import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(layout="wide")
st.title("Market Logic Trainer")

# -------------------------------------------------
# DARK TERMINAL STYLE
# -------------------------------------------------
st.markdown("""
<style>
body { background-color: #0e1117; }
.stApp { background-color: #0e1117; color: #e6e6e6; }
h1, h2, h3, h4 { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DATA GENERATION
# -------------------------------------------------
@st.cache_data
def generate_data():
    np.random.seed(1)
    price = 100
    prices = []
    for i in range(500):
        drift = 0.02
        shock = np.random.randn() * 0.5
        price += drift + shock
        prices.append(price)
    return pd.DataFrame({"Close": prices})

df = generate_data()

# -------------------------------------------------
# REPLAY
# -------------------------------------------------
step = st.slider("Replay Candle", 20, len(df), 150)
chart_data = df.iloc[:step]
current_price = chart_data["Close"].iloc[-1]

# -------------------------------------------------
# STRUCTURE DETECTION
# -------------------------------------------------
lookback = 3

def detect_structure(data):
    highs = []
    lows = []
    for i in range(lookback, len(data)-lookback):
        window = data["Close"][i-lookback:i+lookback+1]
        if data["Close"][i] == max(window):
            highs.append((i, data["Close"][i]))
        if data["Close"][i] == min(window):
            lows.append((i, data["Close"][i]))
    return highs, lows

swings_high, swings_low = detect_structure(chart_data)

bias = "RANGE"
if len(swings_high) >= 2 and len(swings_low) >= 2:
    if swings_high[-1][1] > swings_high[-2][1] and swings_low[-1][1] > swings_low[-2][1]:
        bias = "BULLISH"
    elif swings_high[-1][1] < swings_high[-2][1] and swings_low[-1][1] < swings_low[-2][1]:
        bias = "BEARISH"

# -------------------------------------------------
# LIQUIDITY DETECTION
# -------------------------------------------------
tolerance = 1.0
liquidity_highs = []
liquidity_lows = []

if len(swings_high) >= 2:
    if abs(swings_high[-1][1] - swings_high[-2][1]) < tolerance:
        liquidity_highs.append(swings_high[-1][1])

if len(swings_low) >= 2:
    if abs(swings_low[-1][1] - swings_low[-2][1]) < tolerance:
        liquidity_lows.append(swings_low[-1][1])

# -------------------------------------------------
# SWEEP DETECTION
# -------------------------------------------------
sweep_high = liquidity_highs and current_price >= liquidity_highs[-1]
sweep_low = liquidity_lows and current_price <= liquidity_lows[-1]

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
if "position" not in st.session_state:
    st.session_state.position = None
    st.session_state.entry_price = None
    st.session_state.entry_bias = None
    st.session_state.entry_sweep_high = False
    st.session_state.entry_sweep_low = False

# -------------------------------------------------
# LANDSCAPE LAYOUT
# -------------------------------------------------
st.markdown("---")
left, right = st.columns([4,1])

# ---------------- LEFT: CHART ----------------
with left:
    st.subheader("Price Chart")
    st.line_chart(chart_data["Close"])

# ---------------- RIGHT: CONTROL PANEL ----------------
with right:

    with st.expander("📊 Structure", expanded=True):
        st.write(f"Bias: **{bias}**")
        st.write(f"Swing Highs: {len(swings_high)}")
        st.write(f"Swing Lows: {len(swings_low)}")

    with st.expander("📍 Liquidity"):
        st.write(f"Equal Highs: {'✅' if liquidity_highs else '❌'}")
        st.write(f"Equal Lows: {'✅' if liquidity_lows else '❌'}")
        if sweep_high:
            st.write("High Swept 🚨")
        if sweep_low:
            st.write("Low Swept 🚨")

    with st.expander("💰 Trade Panel", expanded=True):

        buy_col, sell_col = st.columns(2)

        with buy_col:
            if st.button("BUY"):
                st.session_state.position = "LONG"
                st.session_state.entry_price = current_price
                st.session_state.entry_bias = bias
                st.session_state.entry_sweep_high = sweep_high
                st.session_state.entry_sweep_low = sweep_low

        with sell_col:
            if st.button("SELL"):
                st.session_state.position = "SHORT"
                st.session_state.entry_price = current_price
                st.session_state.entry_bias = bias
                st.session_state.entry_sweep_high = sweep_high
                st.session_state.entry_sweep_low = sweep_low

        if st.session_state.position:
            pnl = (
                current_price - st.session_state.entry_price
                if st.session_state.position == "LONG"
                else st.session_state.entry_price - current_price
            )

            st.write(f"Position: {st.session_state.position}")
            st.write(f"Entry: {st.session_state.entry_price:.2f}")
            st.write(f"Unrealized PnL: {pnl:.2f}")

    with st.expander("📊 Trade Evaluation", expanded=True):

        if st.button("CLOSE TRADE") and st.session_state.position:

            quality = "LOW"

            if st.session_state.entry_bias == "BULLISH" and st.session_state.entry_sweep_low:
                quality = "HIGH"
            elif st.session_state.entry_bias == "BEARISH" and st.session_state.entry_sweep_high:
                quality = "HIGH"
            elif st.session_state.entry_bias in ["BULLISH", "BEARISH"]:
                quality = "MEDIUM"

            st.success("Trade Closed")
            st.write(f"Trade Quality: **{quality}**")

            st.session_state.position = None
            st.session_state.entry_price = None

# -------------------------------------------------
# BOTTOM TABS
# -------------------------------------------------
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["Positions", "Orders", "Session Stats"])

with tab1:
    if st.session_state.position:
        st.write("Active Position:")
        st.write(st.session_state.position)
    else:
        st.write("No open positions.")

with tab2:
    st.write("Order tracking coming soon.")

with tab3:
    st.write("Session performance analytics coming soon.")
