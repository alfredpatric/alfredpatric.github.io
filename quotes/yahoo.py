"""Yahoo Finance quote client."""

from __future__ import annotations

import datetime as _dt
import json
import os
import time
import urllib.parse
import urllib.request
from typing import Tuple

API_KEY_ENV = "YAHOO_API_KEY"
RETRIES = 3
BACKOFF = 0.5


def _get_json(url: str, params: dict, headers: dict | None = None) -> dict:
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{query}", headers=headers or {})
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(req) as resp:
                data = resp.read().decode()
                return json.loads(data)
        except Exception:
            if attempt == RETRIES - 1:
                raise
            time.sleep(BACKOFF * (2 ** attempt))


def get_price(symbol: str, exchange: str | None = None, api_key: str | None = None) -> Tuple[float, str, _dt.datetime]:
    """Fetch latest price for *symbol* from Yahoo Finance."""

    key = api_key or os.getenv(API_KEY_ENV)
    headers = {"x-api-key": key} if key else None

    query_symbol = f"{symbol}.{exchange}" if exchange else symbol

    url = "https://query1.finance.yahoo.com/v7/finance/quote"
    params = {"symbols": query_symbol}
    result = _get_json(url, params, headers=headers)["quoteResponse"]["result"][0]

    price = float(result["regularMarketPrice"])
    currency = result.get("currency", "USD")
    ts_val = result.get("regularMarketTime", 0)
    timestamp = _dt.datetime.fromtimestamp(ts_val, tz=_dt.timezone.utc)

    return price, currency, timestamp
