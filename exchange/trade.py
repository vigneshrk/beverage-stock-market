"""
Holds Trade related information
"""

from common.constants import TradeType
from datetime import datetime

from exchange.stock import StockInfo



class Trade:
    """
    A class representing a trade entry in the market.
    """

    def __init__(
        self,
        stock_symbol: str,
        timestamp: datetime,
        quantity: int,
        trade_type: TradeType,
        price: float,
    ):
        """
        Initialize a trade entry with the given parameters.
        """
        self.stock_symbol = stock_symbol
        self.timestamp = timestamp
        self.quantity = quantity
        self.trade_type = trade_type.value
        self.price = price
        self._validate_inputs()

    def _validate_inputs(self) -> None:
        """
        Validate the input parameters of the trade entry.
        """
        stock_info = StockInfo()
        if not stock_info.is_valid_stock(self.stock_symbol):
            raise ValueError(f"Stock symbol {self.stock_symbol} is not valid")
        if self.quantity <= 0:
            raise ValueError(f"Quantity {self.quantity} should be more than 0")
        if self.price <= 0:
            raise ValueError(f"Price {self.price} should be more than 0")

    def __repr__(self) -> str:
        """
        Provide an unambiguous string representation of the Trade object.
        """
        return (f"Trade(stock_symbol={self.stock_symbol!r}, timestamp={self.timestamp!r}, "
                f"quantity={self.quantity}, trade_type={self.trade_type!r}, price={self.price})")
