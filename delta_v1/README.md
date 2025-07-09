# Algo Trading Prototype

This sample project demonstrates a small trading dashboard built with FastAPI. All data is stored in Redis. The app lets you sign up, log in, store exchange API keys and define simple trading rules. A WebSocket client records the latest BTC/USDT price from Binance and writes it to Redis.

## Running

Install requirements and start the application from the `delta_v1` folder:

```bash
cd delta_v1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A local Redis server is expected on `localhost:6379`.

Open `http://localhost:8000` to access the dashboard.
