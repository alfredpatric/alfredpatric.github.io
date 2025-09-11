import datetime as dt
import pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from quotes import alphavantage, yahoo


def test_alphavantage_get_price(monkeypatch):
    payload = {
        "Global Quote": {
            "05. price": "101.23",
            "07. latest trading day": "2024-01-02",
        }
    }

    monkeypatch.setenv("ALPHAVANTAGE_API_KEY", "key")
    monkeypatch.setattr(alphavantage, "_get_json", lambda url, params: payload)

    price, currency, ts = alphavantage.get_price("AAPL", "NASDAQ")

    assert price == 101.23
    assert currency == "USD"
    assert ts == dt.datetime(2024, 1, 2)


def test_yahoo_get_price(monkeypatch):
    now_ts = 1710000000
    payload = {
        "quoteResponse": {
            "result": [
                {
                    "regularMarketPrice": 150.0,
                    "currency": "USD",
                    "regularMarketTime": now_ts,
                }
            ]
        }
    }

    monkeypatch.setattr(yahoo, "_get_json", lambda url, params, headers=None: payload)

    price, currency, ts = yahoo.get_price("MSFT", "NASDAQ")

    assert price == 150.0
    assert currency == "USD"
    assert ts == dt.datetime.fromtimestamp(now_ts, tz=dt.timezone.utc)
