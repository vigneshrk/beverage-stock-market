from datetime import datetime, timedelta
from calculators.stock_stats import DividendYieldCalculator, PERatioCalculator
from calculators.trade_stats import AllShareIndexCalculator, VolumeWeightedStockPriceCalculator
from common.constants import StockType, TradeType
from exchange.market import Market
from exchange.stock import Stock, StockInfo
from exchange.trade import Trade

# Creating some stocks
# OOPS - objct
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
print(res.to_dict(), type(res))

# print('\n\n 111111 \n\n')
###############################################################################

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

#create separate file
market = Market()
market._flush_trades()
for trade in trade_entries:
    market.add_trade(trade) #Add documentation for trades

# print('\n\n 222222 \n\n')
###############################################################################

# Calculating different stats

dividend_calc = DividendYieldCalculator(stock_symbol='GIN', price=4)
dividend_calc.calculate()

# print('\n\n 333333 \n\n')

pe_ratio_calc = PERatioCalculator(stock_symbol='GIN', price=4)
pe_ratio_calc.calculate()

# print('\n\n 444444 \n\n')

vwsp_calc = VolumeWeightedStockPriceCalculator(stock_symbol='ALE')
vwsp_calc.calculate()

# print('\n\n 555555 \n\n')

all_share_vwsp_calc = VolumeWeightedStockPriceCalculator()
all_share_vwsp = all_share_vwsp_calc.calculate()
all_share_index_calc = AllShareIndexCalculator(all_share_vwsp)
all_share_index_calc.calculate()

# print('\n\n 666666 \n\n')