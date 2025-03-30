"""
Holds infomation about all stocks
"""

import logging
from common.constants import FIXED_DIVIDEND_PCT, LAST_DIVIDEND, PAR_VALUE, STOCK_SYMBOL, STOCK_TYPE, StockType, TradeType
from utils.classutils import singleton
import pandas as pd
from typing import List


class Stock:
    """
    A class to represent an individual Stock.
    """
    def __init__(self, stock_symbol: str, type: StockType, last_dividend: float, fixed_dividend_pct: float, par_value: float):
        """
        Initialize a Stock object.

        Parameters:
        stock_symbol (str): The symbol of the stock.
        type (StockType): The type of the stock (e.g., common, preferred).
        last_dividend (float): The last dividend value of the stock.
        fixed_dividend_pct (float): The fixed dividend percentage of the stock.
        par_value (float): The par value of the stock.
        """
        self.stock_symbol = stock_symbol
        self.type = type.value
        self.last_dividend = last_dividend
        self.fixed_dividend_pct = fixed_dividend_pct
        self.par_value = par_value
        self._validate_inputs()

    def _validate_inputs(self):
        if self.fixed_dividend_pct and self.fixed_dividend_pct < 0:
            raise ValueError(f"fixed_dividend_pct {self.fixed_dividend_pct} cannot be negative")
        if self.par_value and self.par_value < 0:
            raise ValueError(f"par_value {self.par_value} cannot be negative")

    def __repr__(self):
        return (f"Stock(stock_symbol='{self.stock_symbol}', type='{self.type}', last_dividend={self.last_dividend}, "
                f"fixed_dividend_pct={self.fixed_dividend_pct}, par_value={self.par_value})")



@singleton
class StockInfo:
    """
    A class to store and manage stock information. It is designed as a Singleton
    class to ensure we have only one data store for Stocks related information.

    Attributes:
        _stocks (pd.DataFrame): A DataFrame to store stock information.

    Methods:
        add_stocks(stocks_list):
            Adds stock information to the DataFrame.

        get_all_stocks():
            Returns a DataFrame containing all stock information.
    """

    def __init__(self) -> None:
        """
        Initialize a StockInfo object with an empty DataFrame.
        """
        self._stocks = pd.DataFrame()

    def add_stocks(self, stocks_list: List[Stock]) -> None:
        """
        Add stock information to the DataFrame.

        Parameters:
        stocks_list (list of Stock): List of Stock objects containing stock information.

        Raises:
        ValueError: If there are duplicate stock symbols in the new data.
        """
        new_stocks = pd.DataFrame([stock.__dict__ for stock in stocks_list])
        new_stocks = new_stocks.astype(
            {
                STOCK_TYPE: "str",
                LAST_DIVIDEND: "float",
                PAR_VALUE: "float",
                FIXED_DIVIDEND_PCT: "float",
            }
        )
        new_stocks = new_stocks.set_index(STOCK_SYMBOL)
        merged_table = (
            pd.concat([self._stocks, new_stocks])
            if not self._stocks.empty
            else new_stocks
        )

        # Check for duplicates in the new index
        if merged_table.index.duplicated().any():
            raise ValueError("Duplicate stock symbols found")
        else:
            # No duplicates, proceed to save data
            self._stocks = merged_table
            logging.info(f"New stocks {stocks_list} successfully added to the data store")

    def is_valid_stock(self, stock_symbol: str) -> bool:
        """
        Check if a stock symbol is valid
        """
        return stock_symbol in self._stocks.index

    def get_stock_info(self, stock_symbol: str) -> pd.Series:
        """
        Retrieve the information of a specific stock by its symbol.

        Parameters:
        stock_symbol (str): The symbol of the stock to retrieve.

        Returns:
        pd.Series: A Series containing the stock information.

        Raises:
        ValueError: If the stock symbol does not exist.
        """
        if self.is_valid_stock(stock_symbol):
            return self._stocks.loc[stock_symbol]
        else:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found")

    def get_all_stocks(self) -> pd.DataFrame:
        """
        Returns a DataFrame containing information about all stocks
        """
        return self._stocks

    def _remove_all_stocks(self) -> None:
        """
        Removes all stocks from the data store
        """
        self._stocks = pd.DataFrame()
