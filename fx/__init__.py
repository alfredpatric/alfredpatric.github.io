"""Foreign exchange utilities."""

from __future__ import annotations

import datetime as dt
import json
from urllib import request

# Simple in-memory cache: {base_currency: (date, rates)}
_cache: dict[str, tuple[dt.date, dict[str, float]]] = {}

_API_URL = "https://open.er-api.com/v6/latest/{}"


def _get_rates(base: str) -> dict[str, float]:
    """Fetch FX rates for the given base currency.

    Results are cached per-day to avoid repeated network calls.
    """

    today = dt.date.today()
    cached = _cache.get(base)
    if cached and cached[0] == today:
        return cached[1]

    with request.urlopen(_API_URL.format(base)) as resp:
        data = json.loads(resp.read().decode())
    rates = data["rates"]
    _cache[base] = (today, rates)
    return rates


def convert(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert ``amount`` from one currency into another."""

    if from_currency == to_currency:
        return amount

    rates = _get_rates(from_currency)
    if to_currency not in rates:
        raise ValueError(f"Unknown currency: {to_currency}")
    return amount * rates[to_currency]
