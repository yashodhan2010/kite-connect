from core.connection import connect, generate_access_token, get_login_url
from core.buy import place_buy_order
from core.sell import place_sell_order
from core.utils import log_trade, fetch_order_status,log_error
import streamlit as st
import pandas as pd
import os
import config
from kiteconnect import KiteConnect as kc
import logging
import sys 
import json
from datetime import datetime
import csv

TRADE_LOG_FILE = "logs/trading_log.csv"
ERROR_LOG_FILE = "logs/trading_errors.log"

# Handler for error logs
error_handler = logging.FileHandler("logs/trading_errors.log")
error_handler.setLevel(logging.ERROR)
error_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
error_handler.setFormatter(error_format)

# Root logger setup
logging.getLogger().handlers = []  # Remove any existing handlers
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.ERROR)

# Basic constants
kite = kc(api_key=config.API_KEY)
SESSION_FILE = "session.json"

st.set_page_config(page_title="Trading Bot", layout="centered")

st.title("💹 Zerodha Trading Bot")
st.write("Connect once per day and place BUY/SELL orders directly.")

# Step 1: Connect to Kite
if 'kite' not in st.session_state:
    st.session_state.kite = connect()

if not st.session_state.kite:
    st.warning("You need to log in to Kite first.")
    login_url = get_login_url()
    st.markdown(f"👉 [Click here to log in to Zerodha Kite Connect]({login_url})", unsafe_allow_html=True)
    request_token = st.text_input("Paste the `request_token` you got after login:")
    if st.button("🔐 Generate Access Token"):
        try:
            kite = generate_access_token(request_token)
            st.session_state.kite = kite
            st.success("✅ Successfully connected to Kite!")
            
        except Exception as e:
            st.error(f"Failed to generate access token: {e}")
    st.stop()

# Only show trade inputs after connection
st.success("✅ Logged In")


st.subheader("📋 Place an Order")

col1, col2 = st.columns(2)
with col1:
    action = st.selectbox("Select Action", ["BUY", "SELL"])
with col2:
    symbol = st.text_input("Enter Symbol (e.g. INFY)").upper()

qty = st.number_input("Enter Quantity", min_value=1, step=1)


if st.button("🚀 Place Order"):
    kite = st.session_state.kite
    try:
        if action == "BUY":
            order_id = place_buy_order(kite,symbol, qty)
        else:
            order_id = place_sell_order(kite,symbol, qty)

        # Fetch order status
        status = fetch_order_status(kite,order_id)
        order_status = status.get("status") if status else "FAILED"
        executed_price = status.get("price") if status else None

        log_trade(action, symbol, qty, executed_price, order_id, order_status)

        if order_status == "COMPLETE":
            st.success(f"✅ {action} order for {symbol} completed successfully!")
        else:
            st.warning(f"⚠️ Order placed but not complete (Status: {order_status})")

    except Exception as e:
        st.error(f"Order failed: {str(e)}")
        log_error(action, symbol, qty, executed_price, None, f"EXCEPTION: {str(e)}")

# Step 3: Logs
st.divider()
st.subheader("📊 Trade Logs")

if os.path.exists("logs/trading_log.csv"):
    df = pd.read_csv("logs/trading_log.csv")
    st.dataframe(df.tail(10))
else:
    st.info("No trades logged yet.")

st.divider()
st.subheader("⚠️ Error Logs")

if os.path.exists("logs/trading_errors.log"):
    with open("logs/trading_errors.log") as f:
        logs = f.read()
    st.text_area("Error Log", logs, height=200)
else:
    st.info("No error logs found.")