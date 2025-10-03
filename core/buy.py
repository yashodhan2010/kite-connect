#import logging
#import sys
#import os

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from connection import connect
#from utils import log_message, fetch_order_status

#kite = connect()

def place_buy_order(symbol, qty):
    
    try:
        order_id = kite.place_order(tradingsymbol=symbol,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=qty,
                                variety=kite.VARIETY_REGULAR,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC,
                                validity=kite.VALIDITY_DAY)

        log_message("Order placed. ID is: {}".format(order_id))
        return order_id
    except Exception as e:
        log_message("Order placement failed: {}".format(e),level = "error")
        return None
