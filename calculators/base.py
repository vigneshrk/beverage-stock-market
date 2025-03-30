"""
Holds all the abstract base clasees for different types of stat calculators
"""

from abc import ABC, abstractmethod
import logging
from typing import Any

from exchange.market import Market
from exchange.stock import StockInfo


class BaseCalculator(ABC):
    """
    Abstract base class for all statistics calculators

    Parameters:
    input_data: The data required for calculation. Derived/Concrete classes
    are expected to be initialized with input_data as a parameter.
    """

    def __init__(self, input_data: Any) -> None:
        """
        Initialize the BaseCalculator with input data.

        Parameters:
        input_data (Any): The data required for calculation.
        """
        self.input_data = input_data
        logging.info(f"Initialized {self.__class__.__name__} with input data:\n {input_data}")

    @abstractmethod
    def calculate(self, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method for performing calculations.
        Must be implemented by subclasses.

        Returns:
        Any: Result of the calculation.
        """
        pass


class StockStatisticCalculator(BaseCalculator):
    """
    Abstract Base calculator for stock attribute calculations.

    Parameters:
    stock_symbol: The symbol of the stock.
    price: The price of the stock.

    Example:
        class ConcreteStockAttributeCalculator(StockStatisticCalculator):
            def calculate(self):
                ...
                return stat_value

            stock_attr_calc = ConcreteStockAttributeCalculator(stock_symbol='XYZ', price=100)
            stock_attr_calc.calculate()
    """

    def __init__(self, stock_symbol: str, price: float) -> None:
        """
        Initialize the StockStatisticCalculator with stock symbol and price.

        Parameters:
        stock_symbol (str): The symbol of the stock.
        price (float): The price of the stock.
        """
        self.custom_price = price
        if not self.custom_price or self.custom_price <= 0:
            raise ValueError(f"Given price {self.custom_price} is invalid, provide a positive number")
        stock_info = StockInfo().get_stock_info(stock_symbol)
        super().__init__(input_data=stock_info)


class TradeStatisticCalculator(BaseCalculator):
    """
    Abstract Base calculator for statistics calculated from trade data, like Volume Weighted Stock Price

    Parameters:
    trade_filter: The filter to apply to trades.

    Example:
        class ConcreteTradeStatCalculator(TradeStatisticCalculator):
            def calculate(self):
                ...
                return stat_value

        stat_calc = ConcreteTradeStatCalculator(trade_filter="stock_symbol=='XYZ' and trade_type='buy'")
    """

    def __init__(self, trade_filter: str):
        """
        Initialize the TradeStatisticCalculator with a trade filter.

        Parameters:
        trade_filter (str): The filter to apply to trades.
        """
        market = Market()
        filtered_trades = market.get_trades(trade_filter)
        super().__init__(input_data=filtered_trades)