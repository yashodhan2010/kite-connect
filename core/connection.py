import os
import json
import logging
from kiteconnect import KiteConnect as kc
import config
from datetime import datetime
# Set logging
logging.basicConfig(level=logging.DEBUG,format="%(asctime)s - %(levelname)s - %(message)s")

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

# Get Login URL
def get_login_url():
    """Return Kite login URL"""
    return kite.login_url()

#  Request fresh token from user
def generate_access_token(request_token):
    """Generate and save new access token"""
   
    data = kite.generate_session(request_token, api_secret=config.API_SECRET)
    kite.set_access_token(data["access_token"])

    save_token({
        "access_token": data["access_token"],
        "date": datetime.today().strftime("%Y-%m-%d")
    })

    logging.info("New access token generated and saved")
    return kite

def connect():
    # Try to reuse existing token if valid
    data = load_token()
    if data and data.get("date") == datetime.today().strftime("%Y-%m-%d"):
        kite.set_access_token(data["access_token"])
        logging.info("✅ Reusing existing access token")
        return kite

    # Else require fresh login
    else:
        return None