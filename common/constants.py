from enum import Enum


STOCK_SYMBOL = "stock_symbol"
STOCK_TYPE = "type"
LAST_DIVIDEND = "last_dividend"
PAR_VALUE = "par_value"
FIXED_DIVIDEND_PCT = "fixed_dividend_pct"
TIMESTAMP = "timestamp"

class StockType(Enum):
    COMMON = "Common"
    PREFERRED = "Preferred"

class TradeType(Enum):
    BUY = 'buy'
    SELL = 'sell'