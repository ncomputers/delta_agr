import redis
import time
import json

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# User management

def create_user(username: str, hashed_password: str):
    if redis_client.hexists("users", username):
        return None
    user_id = redis_client.incr("next_user_id")
    redis_client.hset("users", username, user_id)
    redis_client.hset(f"user:{user_id}", mapping={"username": username, "password": hashed_password})
    return user_id

def get_user(username: str):
    user_id = redis_client.hget("users", username)
    if not user_id:
        return None
    data = redis_client.hgetall(f"user:{user_id}")
    data["id"] = int(user_id)
    return data

# API keys

def save_api_keys(user_id: int, api_key: str, api_secret: str):
    redis_client.hset(f"api_keys:{user_id}", mapping={"api_key": api_key, "api_secret": api_secret})

# Trade rules

def save_trade_rule(user_id: int, loss_threshold: float, quantity: float, profit_target: float):
    redis_client.hset(
        f"trade_rule:{user_id}",
        mapping={"loss_threshold": loss_threshold, "quantity": quantity, "profit_target": profit_target},
    )

# Price storage

def save_price(symbol: str, price: float):
    redis_client.hset("latest_price", symbol, price)
    redis_client.lpush("price_history", json.dumps({"timestamp": time.time(), "symbol": symbol, "price": price}))
    redis_client.ltrim("price_history", 0, 999)  # keep last 1000 entries
