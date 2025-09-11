"""AlphaVantage quote client."""

from __future__ import annotations

import datetime as _dt
import json
import os
import time
import urllib.parse
import urllib.request
from typing import Tuple

API_KEY_ENV = "ALPHAVANTAGE_API_KEY"
RETRIES = 3
BACKOFF = 0.5


def _get_json(url: str, params: dict) -> dict:
    """Return JSON payload for *url* with *params* using retry logic."""
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(full_url) as resp:
                data = resp.read().decode()
                return json.loads(data)
        except Exception:
            if attempt == RETRIES - 1:
                raise
            time.sleep(BACKOFF * (2 ** attempt))


def get_price(symbol: str, exchange: str | None = None, api_key: str | None = None) -> Tuple[float, str, _dt.datetime]:
    """Fetch latest price for *symbol* from AlphaVantage.

    Parameters
    ----------
    symbol: str
        Ticker symbol, e.g. ``"AAPL"``.
    exchange: str | None
        Exchange code.  Currently unused but kept for API symmetry.
    api_key: str | None
        API key.  If ``None`` we look in the ``ALPHAVANTAGE_API_KEY`` env var.

    Returns
    -------
    tuple
        ``(price, currency, timestamp)``
    """

    key = api_key or os.getenv(API_KEY_ENV)
    if not key:
        raise RuntimeError(f"AlphaVantage API key not provided; set {API_KEY_ENV}")

    url = "https://www.alphavantage.co/query"
    params = {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": key}
    payload = _get_json(url, params).get("Global Quote", {})

    price_str = payload.get("05. price")
    if price_str is None:
        raise ValueError("Price not found in AlphaVantage response")

    price = float(price_str)
    currency = "USD"  # AlphaVantage does not return currency
    date_str = payload.get("07. latest trading day")
    if date_str:
        timestamp = _dt.datetime.strptime(date_str, "%Y-%m-%d")
    else:
        timestamp = _dt.datetime.utcnow()

    return price, currency, timestamp
