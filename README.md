# Beverage Stock Market

This repository provides a simulation for calculating various stock market statistics based on stock and trade data. The key statistics calculated include Dividend Yield, P/E Ratio, Volume Weighted Stock Price (VWSP), and All Share Index.

## Overview

Core Functions:
1. Setting up beverage stocks and adding them to the stock market.
2. Creating buy/sell trades for different beverage stocks and recording them in the market.
3. Calculating key stock market statistics based on the recorded data - Dividend Yield, P/E Ratio, Volume Weighted Stock Price (VWSP), and All Share Index.

## Requirements

- Python 3.x
- Pandas
- SciPy

## Quick start
Navigate to the top directory of the project, and run:

```sh
export PYTHONNOCLEANSYSPATH=1; python sample_simulation.py
```

This runs a basic simulation of the entire flow - Creating Stocks and Trades records, and eventually calcualting all the stats.


Running all tests:
```sh
pytest tests/ --durations=0
```
This will automatically discover and run all tests in the tests directory. It also lists down the time taken for the tests.

## Core Entities
```python
class Stock: # Represents an individual Stock

class StockInfo: # Stores and manages stock information.
# It is designed as a Singleton class to ensure we have only one data store for Stocks related information

class Trade: # A class representing a single trade record in the market.

class Market: # A class representing the stock market, storing all buy/sell trade entries.
# It is designed as a Singleton class to ensure we have only one data store for Trades related information
```

## Statistics Calculator Infra
```python
"""
====================================================
Structure:
====================================================
BaseCalculator
|
|
|====> StockStatisticCalculator
|      |
|      |====> DividendYieldCalculator
|      |            ^
|      |            |
|      |====> PERatioCalculator
|
|====> TradeStatisticCalculator
|      |
|      |====> VolumeWeightedStockPriceCalculator
|                  ^
|                  |
|===========> AllShareIndexCalculator
"""

class BaseCalculator(ABC): # Abstract base class for all statistics calculators

class StockStatisticCalculator(BaseCalculator): # Abstract calculator for stock attribute calculators like Dividend Yield Calculator, P/E Ratio Calculator, etc.

class TradeStatisticCalculator(BaseCalculator): # Abstract Base calculator for statistics calculated from trade data, like Volume Weighted Stock Price

class DividendYieldCalculator(StockStatisticCalculator): # Calculator for determining the dividend yield of a stock.

class PERatioCalculator(StockStatisticCalculator): # Calculator for determining the P/E ratio of a stock.

class VolumeWeightedStockPriceCalculator(TradeStatisticCalculator): # Calculator for determining the volume weighted stock price of one stock / all stocks

class AllShareIndexCalculator(BaseCalculator): # Calculator for determining the all-share index.
```

## Usage

### Setting Up Stocks
Create instances of Stock and add them to the StockInfo datastore.
```python
from common.constants import StockType
from exchange.stock import Stock, StockInfo

# Creating some stocks
stocks_data = [
    Stock(stock_symbol="TEA", type=StockType.COMMON, last_dividend=0, fixed_dividend_pct=None, par_value=100),
    Stock(stock_symbol="POP", type=StockType.COMMON, last_dividend=8, fixed_dividend_pct=None, par_value=100),
    Stock(stock_symbol="ALE", type=StockType.COMMON, last_dividend=23, fixed_dividend_pct=None, par_value=60),
    Stock(stock_symbol="GIN", type=StockType.PREFERRED, last_dividend=8, fixed_dividend_pct=0.02, par_value=100),
    Stock(stock_symbol="JOE", type=StockType.COMMON, last_dividend=13, fixed_dividend_pct=None, par_value=250)
]

stock_info = StockInfo()
stock_info.add_stocks(stocks_data)

res = stock_info.get_all_stocks()
```
### Recording Trades
Create trade entries and add them to the Market.
```python
from datetime import datetime, timedelta
from exchange.trade import Trade
from common.constants import TradeType
from exchange.market import Market

# Creating some trades
dt1 = datetime.now() - timedelta(seconds=45)
dt2 = datetime.now() - timedelta(minutes=1)
dt3 = datetime.now() - timedelta(minutes=2)
dt4 = datetime.now() - timedelta(minutes=2, seconds=30)

trade_entries = [
    Trade(stock_symbol="TEA", timestamp=datetime(2025, 3, 29, 9, 0), quantity=100, trade_type=TradeType.BUY, price=105.0),
    Trade(stock_symbol="POP", timestamp=datetime(2025, 3, 29, 9, 5), quantity=200, trade_type=TradeType.BUY, price=123.5),
    Trade(stock_symbol="ALE", timestamp=datetime(2025, 3, 29, 9, 10), quantity=150, trade_type=TradeType.SELL, price=98.25),
    Trade(stock_symbol="GIN", timestamp=datetime(2025, 3, 29, 9, 15), quantity=250, trade_type=TradeType.BUY, price=156.0),
    Trade(stock_symbol="JOE", timestamp=datetime(2025, 3, 29, 9, 20), quantity=50, trade_type=TradeType.SELL, price=205.75),
    Trade(stock_symbol="TEA", timestamp=dt1, quantity=100, trade_type=TradeType.BUY, price=105.0),
    Trade(stock_symbol="POP", timestamp=dt2, quantity=200, trade_type=TradeType.BUY, price=123.5),
    Trade(stock_symbol="ALE", timestamp=dt3, quantity=150, trade_type=TradeType.SELL, price=98.25),
    Trade(stock_symbol="GIN", timestamp=dt4, quantity=250, trade_type=TradeType.BUY, price=156.0),
    Trade(stock_symbol="JOE", timestamp=dt1, quantity=50, trade_type=TradeType.SELL, price=205.75),
    Trade(stock_symbol="TEA", timestamp=dt2, quantity=10, trade_type=TradeType.BUY, price=102.0),
    Trade(stock_symbol="POP", timestamp=dt3, quantity=60, trade_type=TradeType.BUY, price=125.5),
    Trade(stock_symbol="ALE", timestamp=dt4, quantity=15, trade_type=TradeType.SELL, price=88.25),
    Trade(stock_symbol="GIN", timestamp=dt1, quantity=25, trade_type=TradeType.BUY, price=151.0),
    Trade(stock_symbol="JOE", timestamp=dt2, quantity=5, trade_type=TradeType.SELL, price=200.75)
]

market = Market()
market._flush_trades()
for trade in trade_entries:
    market.add_trade(trade)
```

### Calculating Statistics
Calculate various statistics such as Dividend Yield, P/E Ratio, VWSP, and All Share Index.
```python
from calculators.stock_stats import DividendYieldCalculator, PERatioCalculator
from calculators.trade_stats import AllShareIndexCalculator, VolumeWeightedStockPriceCalculator

# Dividend Yield Calculation
dividend_calc = DividendYieldCalculator(stock_symbol='GIN', price=4)
dividend_yield = dividend_calc.calculate()

# P/E Ratio Calculation
pe_ratio_calc = PERatioCalculator(stock_symbol='GIN', price=4)
pe_ratio = pe_ratio_calc.calculate()

# Volume Weighted Stock Price Calculation for a specific stock
vwsp_calc = VolumeWeightedStockPriceCalculator(stock_symbol='ALE')
vwsp = vwsp_calc.calculate()

# All Share Index Calculation
all_share_vwsp_calc = VolumeWeightedStockPriceCalculator()
all_share_vwsp = all_share_vwsp_calc.calculate()
all_share_index_calc = AllShareIndexCalculator(all_share_vwsp)
all_share_index = all_share_index_calc.calculate()

```

