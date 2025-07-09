import json
import threading
import time
import websocket

from .database import save_price

current_price = None


def on_message(ws, message):
    global current_price
    data = json.loads(message)
    if "p" in data:
        current_price = float(data["p"])
        save_price("BTCUSDT", current_price)


def on_error(ws, error):
    print("WebSocket error:", error)


def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed:", close_status_code, close_msg)


def on_open(ws):
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@aggTrade"],
        "id": 1,
    }
    ws.send(json.dumps(subscribe_message))


def start_websocket():
    ws = websocket.WebSocketApp(
        "wss://fstream.binance.com/ws",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()


def run_in_thread():
    thread = threading.Thread(target=start_websocket, daemon=True)
    thread.start()
    return thread


if __name__ == "__main__":
    run_in_thread()
    while True:
        if current_price is not None:
            print("Latest BTC/USDT price:", current_price)
        time.sleep(2)
