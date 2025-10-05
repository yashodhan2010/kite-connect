
def place_sell_order(symbol, qty):
    
    try:
        order_id = kite.place_order(tradingsymbol=symbol,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_SELL,
                                quantity=qty,
                                variety=kite.VARIETY_REGULAR,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC,
                                validity=kite.VALIDITY_DAY)

        
        return order_id
    except Exception as e:
        return None
