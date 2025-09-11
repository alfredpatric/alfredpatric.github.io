"""Portfolio models for tracking holdings and their value."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import fx


@dataclass
class Holding:
    """Represents a single asset holding."""

    symbol: str
    quantity: float
    price: float
    currency: str

    def value(self) -> float:
        """Return the total value of the holding in its native currency."""

        return self.quantity * self.price


@dataclass
class Portfolio:
    """Collection of holdings with a base currency."""

    holdings: List[Holding] = field(default_factory=list)
    base_currency: str = "USD"

    def add(self, holding: Holding) -> None:
        """Add a holding to the portfolio."""

        self.holdings.append(holding)

    def value(self) -> float:
        """Total value of the portfolio in the base currency."""

        total = 0.0
        for holding in self.holdings:
            val = holding.value()
            if holding.currency != self.base_currency:
                val = fx.convert(val, holding.currency, self.base_currency)
            total += val
        return total
