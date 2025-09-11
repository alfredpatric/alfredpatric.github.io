import pathlib, sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

import fx
from models.portfolio import Holding, Portfolio


def test_convert(monkeypatch):
    rates = {"USD": 1.0, "EUR": 0.8}
    monkeypatch.setattr(fx, "_get_rates", lambda base: rates)

    assert fx.convert(100, "USD", "EUR") == 80.0


def test_portfolio_value(monkeypatch):
    h1 = Holding("AAA", 10, 10.0, "USD")  # 100 USD
    h2 = Holding("BBB", 5, 20.0, "EUR")   # 100 EUR
    p = Portfolio([h1, h2], base_currency="USD")

    monkeypatch.setattr(
        fx,
        "convert",
        lambda amount, from_currency, to_currency: amount * 1.2
        if (from_currency, to_currency) == ("EUR", "USD")
        else amount,
    )

    assert p.value() == 220.0
