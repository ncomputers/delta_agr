import time
import ccxt
from typing import Optional

from . import config  # config module expected

class DeltaExchangeClient:
    def __init__(self, api_key: str, api_secret: str):
        self.exchange = ccxt.delta({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'adjustForTimeDifference': True,
        })
        self._market_cache = None
        self._market_cache_time = 0

    def load_markets(self, reload: bool = False):
        current_time = time.time()
        if not reload and self._market_cache and current_time - self._market_cache_time < 60:
            return self._market_cache
        markets = self.exchange.load_markets(reload)
        self._market_cache = markets
        self._market_cache_time = current_time
        return markets

    def fetch_balance(self):
        return self.exchange.fetch_balance()

    def create_order(self, symbol: str, order_type: str, side: str, amount: float, price: Optional[float] = None, params=None):
        return self.exchange.create_order(symbol, order_type, side, amount, price, params or {})
