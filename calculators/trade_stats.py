"""
Holds concrete implementations of calculators to compute statistics from the
recorded trades of stocks, like Volume Weighted Stock Price, All Share Index, etc.
"""

from datetime import datetime
import logging
from typing import Any
from calculators.base import BaseCalculator, TradeStatisticCalculator
from scipy.stats import gmean
from common.constants import STOCK_SYMBOL, TIMESTAMP
from utils.common import get_timestamp_5_mins_before


class VolumeWeightedStockPriceCalculator(TradeStatisticCalculator):
    """
    Calculator for determining the volume weighted stock price.

    Parameters:
    stock_symbol: The symbol of the stock (optional).
    """

    def __init__(self, stock_symbol: str = None):
        self.stock_symbol = stock_symbol
        filter_queries = []
        timestamp_filter = (
            f"{TIMESTAMP} >= '{get_timestamp_5_mins_before(datetime.now())}'"
        )
        filter_queries.append(timestamp_filter)
        if stock_symbol:
            stock_symbol_filter = f"{STOCK_SYMBOL} == '{stock_symbol}'"
            filter_queries.append(stock_symbol_filter)
        trade_filter = " & ".join(filter_queries)
        super().__init__(trade_filter=trade_filter)

    def calculate(self) -> Any:
        """
        Calculate the volume weighted stock price for the stock.

        Returns:
        float or pd.DataFrame: The volume weighted stock price for the specified stock,
        or a DataFrame of volume weighted stock prices for all stocks if no stock symbol is specified.
        """
        if self.input_data.empty:
            return None
        trades = self.input_data.copy()
        # Calculate the weighted sums and total quantities using vectorized operations
        trades["total_trade_value"] = trades["price"] * trades["quantity"]
        result = trades.groupby("stock_symbol").agg(
            {"total_trade_value": "sum", "quantity": "sum"}
        )

        # Calculate the Volume Weighted Stock Price
        result["volume_weighted_stock_price"] = (
            result["total_trade_value"] / result["quantity"]
        ).round(2)

        # Reset the index to turn the grouped DataFrame back to a regular DataFrame
        result = result.drop(columns=["total_trade_value", "quantity"]).reset_index()

        if self.stock_symbol:
            vwsp = result.squeeze().volume_weighted_stock_price
            logging.info(f"Calculated VWSP for {self.stock_symbol}: {vwsp}")
            return vwsp
        else:
            logging.info(f"Calculated VWSP for all stocks")
            return result


class AllShareIndexCalculator(BaseCalculator):
    """
    Calculator for determining the all-share index.
    """

    def calculate(self) -> float:
        """
        Calculate the all-share index.

        Returns:
        float: The geometric mean of the volume weighted stock prices.
        """
        # Check for valid prices (non-NaN, positive values)
        positive_prices = self.input_data["volume_weighted_stock_price"].dropna()
        positive_prices = positive_prices[positive_prices > 0]

        if positive_prices.empty:
            logging.info("No positive prices available to calculate the all-share index.")
            return 0.0

        geometric_mean = gmean(positive_prices)
        all_share_index = round(geometric_mean, 2)
        logging.info(f"Calculated All-Share Index: {all_share_index}")
        return all_share_index