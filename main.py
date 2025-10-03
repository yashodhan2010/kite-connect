from core.connection import connect
from core.buy import place_buy_order
from core.sell import place_sell_order
from core.utils import log_trade, fetch_order_status

def main(symbol=None, action=None, qty=None):
    """
    symbol: string like "INFY"
    action: "BUY" or "SELL"
    qty: int
    """

    # Step 1: Get user inputs if not provided via kwargs
    if symbol is None:
        symbol = input("Enter symbol (e.g. INFY): ").upper()
    if action is None:
        action = input("Enter action (BUY/SELL): ").upper()
    if qty is None:
        qty = int(input("Enter quantity: "))

    # Step 2: Connect to Kite
    kite = connect()

    # Step 3: Place order based on action
    try:
        if action == "BUY":
            order_id = place_buy_order(kite, symbol, qty)
        elif action == "SELL":
            order_id = place_sell_order(kite, symbol, qty)
        else:
            print("Invalid action. Choose BUY or SELL.")
            return

        # Step 4: Fetch status
        status = fetch_order_status(kite, order_id)
        order_status = status.get("status") if status else "FAILED"

        # Step 5: Log order
        log_trade(action, symbol, qty, "MARKET", order_id, order_status)

        print(f"{action} order for {symbol} Qty={qty} | Status={order_status}")

    except Exception as e:
        log_trade(action, symbol, qty, "MARKET", None, f"EXCEPTION: {str(e)}")
        print("Order failed:", str(e))


if __name__ == "__main__":
    # Run interactively
    main()