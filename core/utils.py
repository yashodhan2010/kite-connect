import os
import csv
from datetime import datetime
import logging
from core.connection import connect

TRADE_LOG_FILE = "logs/trading_log.csv"
ERROR_LOG_FILE = "logs/trading_errors.log"



def log_trade(action, tradingsymbol, qty, price, order_id, status="SUCCESS"):
    """Log only successful trades to CSV"""
    if status == "COMPLETE":
        exists = os.path.exists(TRADE_LOG_FILE)
        with open(TRADE_LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(["datetime", "action", "symbol", "qty", "price", "order_id", "status"])
            writer.writerow([datetime.now(), action, tradingsymbol, qty, price, order_id, status])
    else:
        log_error(action, tradingsymbol, qty, price, order_id, status)

def log_error(action, tradingsymbol, qty, price, order_id, error_message):
    """Log errors to a separate log file"""
    with open(ERROR_LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {action} - {tradingsymbol} - {qty} - {price} - {order_id} - ERROR: {error_message}\n")
    
def fetch_order_status(kite,order_id):
    """Fetch status of a given order by ID."""
    kite =connect()
    try:
        orders = kite.orders()
        for order in orders:
            if order["order_id"] == str(order_id):
                return {
                    "status": order["status"],
                    "tradingsymbol": order["tradingsymbol"],
                    "transaction_type": order["transaction_type"],
                    "filled_quantity": order["filled_quantity"],
                    "price": order.get("average_price", None),
                    "order_timestamp": order["order_timestamp"],
                }
        return {"error": "Order ID not found"}
    except Exception as e:
        log_error("FETCH_STATUS", "N/A", 0, "N/A", order_id, str(e))
        return {"error": str(e)}