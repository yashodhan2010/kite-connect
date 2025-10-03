import logging
import sys
import os
import json
from kiteconnect import KiteConnect as kc
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Set logging
logging.basicConfig(level=logging.DEBUG)

# Basic constants
kite = kc(api_key=config.API_KEY)
SESSION_FILE = "session.json"

# Save token to a file
""" We use this to save and reuse the access token so that we don't have to login every time but only once a day """

def save_token(token_data):
    with open(SESSION_FILE, "w") as f:
        json.dump(token_data, f)

# Load token from a file if it exists
def load_token():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

# Request fresh token from user
def get_request_token():
    print("⚠️ Saved token expired, need fresh login. Go to the following URL in your browser:")
    print(kite.login_url())
    request_token = input("Copy the request token here and press ENTER: ")
    return request_token

def connect():
    # Try to reuse existing token if valid
    data = load_token()
    if data and data.get("date") == datetime.today().strftime("%Y-%m-%d"):
        kite.set_access_token(data["access_token"])
        logging.info("✅ Reusing existing access token")
        return kite

    # Else require fresh login
    request_token = get_request_token()
    data = kite.generate_session(request_token, api_secret=config.API_SECRET)
    kite.set_access_token(data["access_token"])
    save_token({
        "access_token": data["access_token"],
        "date": datetime.today().strftime("%Y-%m-%d")
    })
           
    logging.info("✅ Successfully connected to Kite Connect and saved new token")
    return kite

if __name__ == "__main__":
    connect()
