"""
Holds code related to the Beverage stock market - adding trades, filtering
trades for different computations,  etc.
"""

import logging
import pandas as pd
from exchange.trade import Trade
from utils.classutils import singleton


@singleton
class Market:
    """
    A singleton class representing the market, storing trade entries.
    """

    def __init__(self):
        """
        Initialize the market with an empty dataframe for trades.
        """
        logging.info("Initializing the market with an empty dataframe for trades.")
        self._trades = []


    def add_trade(self, trade_entry: Trade) -> None:
        """
        Add a trade entry to the market.
        """
        self._trades.append(trade_entry.__dict__)
        logging.info(f"Trade entry {trade_entry} added successfully.")


    def _flush_trades(self) -> None:
        """
        Clear all the trades from the market.

        Returns:
        None
        """
        self._trades = []
        logging.info("All previous trades have been flushed.")


    def get_trades(self, trade_filter: str = "") -> pd.DataFrame:
        """
        Get trades from the market, optionally filtered by the given filter.

        Parameters:
        trade_filter (str): A query string to filter trades. Defaults to an empty string.

        Returns:
        pd.DataFrame: A dataframe containing the filtered trade entries, or all entries if no filter is provided.

        Example:
            trade_filter="stock_symbol=='XYZ' and trade_type='buy'"
            Market().get_trades(trade_filter)
        """
        trades_df = pd.DataFrame(self._trades)
        if trade_filter:
            logging.info(f"Filtering trades with filter: {trade_filter}")
            try:
                filtered_trades = trades_df.query(trade_filter)
                return filtered_trades
            except Exception as e:
                logging.error(f"Error occurred during trade filter: {e}")
                raise ValueError(
                    f"Filtering Trades failed. Trade filter '{trade_filter}' maybe malformed"
                )
        else:
            logging.info(f"Returning all trades without filtering:\n{trades_df}")
            return trades_df