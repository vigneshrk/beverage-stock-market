
import unittest
from datetime import datetime
from common.constants import TradeType
from exchange.stock import StockInfo, Stock, StockType
from exchange.trade import Trade  # Adjust the import based on your module structure

class TestTrade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setting up StockInfo with valid stocks
        cls.stock_info = StockInfo()
        cls.stock_info._remove_all_stocks()
        cls.stock_info.add_stocks([
            Stock(stock_symbol='JUICE', type=StockType.COMMON, last_dividend=0.8, fixed_dividend_pct=0.0, par_value=100.0),
            Stock(stock_symbol='MILK', type=StockType.PREFERRED, last_dividend=1.0, fixed_dividend_pct=0.02, par_value=200.0)
        ])

    def test_trade_initialization(self):
        trade = Trade(
            stock_symbol='JUICE',
            timestamp=datetime(2023, 10, 5, 14, 0),
            quantity=100,
            trade_type=TradeType.BUY,
            price=150.0
        )
        self.assertEqual(trade.stock_symbol, 'JUICE')
        self.assertEqual(trade.timestamp, datetime(2023, 10, 5, 14, 0))
        self.assertEqual(trade.quantity, 100)
        self.assertEqual(trade.trade_type, TradeType.BUY.value)
        self.assertEqual(trade.price, 150.0)

    def test_invalid_stock_symbol(self):
        with self.assertRaises(ValueError):
            Trade(
                stock_symbol='INVALID',
                timestamp=datetime(2023, 10, 5, 14, 0),
                quantity=100,
                trade_type=TradeType.BUY,
                price=150.0
            )

    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            Trade(
                stock_symbol='JUICE',
                timestamp=datetime(2023, 10, 5, 14, 0),
                quantity=0,
                trade_type=TradeType.BUY,
                price=150.0
            )
        with self.assertRaises(ValueError):
            Trade(
                stock_symbol='JUICE',
                timestamp=datetime(2023, 10, 5, 14, 0),
                quantity=-50,
                trade_type=TradeType.BUY,
                price=150.0
            )

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            Trade(
                stock_symbol='JUICE',
                timestamp=datetime(2023, 10, 5, 14, 0),
                quantity=100,
                trade_type=TradeType.BUY,
                price=0.0
            )
        with self.assertRaises(ValueError):
            Trade(
                stock_symbol='JUICE',
                timestamp=datetime(2023, 10, 5, 14, 0),
                quantity=100,
                trade_type=TradeType.BUY,
                price=-100.0
            )

    def test_repr(self):
        trade = Trade(
            stock_symbol='MILK',
            timestamp=datetime(2023, 10, 5, 14, 0),
            quantity=50,
            trade_type=TradeType.SELL,
            price=2500.0
        )
        expected_repr = "Trade(stock_symbol='MILK', timestamp=datetime.datetime(2023, 10, 5, 14, 0), quantity=50, trade_type='sell', price=2500.0)"
        self.assertEqual(repr(trade), expected_repr)