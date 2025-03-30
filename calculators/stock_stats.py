"""
Holds concrete implementations of calculators to compute statistics of an
individual stock, like Dividend Yield, P/E Ratio, etc.
"""

import logging
from typing import Optional
from calculators.base import StockStatisticCalculator
from common.constants import StockType


class DividendYieldCalculator(StockStatisticCalculator):
    """
    Calculator for determining the dividend yield of a stock.
    """

    def calculate(self) -> Optional[float]:
        """
        Calculate the dividend yield for the stock.

        Returns:
        Optional[float]: The dividend yield, or None if the price is zero or data is incomplete.
        """
        stock_info = self.input_data
        dividend_yield = None
        if self.custom_price:
            if stock_info["type"] == StockType.COMMON.value:
                dividend_yield = stock_info["last_dividend"] / self.custom_price
            elif stock_info["type"] == StockType.PREFERRED.value:
                dividend_yield = (
                    stock_info["fixed_dividend_pct"] * stock_info["par_value"]
                ) / self.custom_price

        logging.info(f"Dividend yield calculated: {dividend_yield}")
        return dividend_yield


class PERatioCalculator(StockStatisticCalculator):
    """
    Calculator for determining the P/E ratio of a stock.
    """

    def calculate(self) -> Optional[float]:
        """
        Calculate the P/E ratio for the stock.

        Returns:
        Optional[float]: The P/E ratio, or None if the price or dividend yield is zero or undefined.
        """

        dividend_calc = DividendYieldCalculator(
            stock_symbol=self.input_data.name, price=self.custom_price
        )
        dividend_yield = dividend_calc.calculate()

        pe_ratio = None
        if dividend_yield:
            pe_ratio = self.custom_price / dividend_yield

        logging.info(f"P/E ratio calculated: {pe_ratio}")
        return pe_ratio
