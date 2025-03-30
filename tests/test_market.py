import unittest
from datetime import datetime

from pandas import Timestamp
from common.constants import TradeType
from exchange.stock import StockInfo, Stock, StockType
from exchange.trade import Trade  # Adjust the import based on your module structure
from exchange.market import Market  # Adjust based on your actual import paths


class TestMarket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setting up StockInfo with valid stocks
        cls.stock_info = StockInfo()
        cls.stock_info._remove_all_stocks()
        cls.stock_info.add_stocks(
            [
                Stock(
                    stock_symbol="JUICE",
                    type=StockType.COMMON,
                    last_dividend=0.8,
                    fixed_dividend_pct=0.0,
                    par_value=100.0,
                ),
                Stock(
                    stock_symbol="MILK",
                    type=StockType.PREFERRED,
                    last_dividend=1.0,
                    fixed_dividend_pct=0.02,
                    par_value=200.0,
                ),
                Stock(
                    stock_symbol="WATER",
                    type=StockType.COMMON,
                    last_dividend=1.2,
                    fixed_dividend_pct=0.01,
                    par_value=150.0,
                ),
                Stock(
                    stock_symbol="SODA",
                    type=StockType.PREFERRED,
                    last_dividend=0.9,
                    fixed_dividend_pct=0.015,
                    par_value=120.0,
                ),
            ]
        )

    @classmethod
    def tearDownClass(cls):
        cls.stock_info._remove_all_stocks()

    def setUp(self):
        self.market = Market()
        self.market._flush_trades()  # Ensure a fresh state for each test
        self.trade_a = Trade(
            stock_symbol="JUICE",
            timestamp=datetime(2023, 10, 5, 14, 0),
            quantity=100,
            trade_type=TradeType.BUY,
            price=150.0,
        )
        self.trade_b = Trade(
            stock_symbol="MILK",
            timestamp=datetime(2023, 10, 6, 10, 0),
            quantity=200,
            trade_type=TradeType.SELL,
            price=2500.0,
        )

    def test_add_trade(self):
        self.market.add_trade(self.trade_a)
        trades = self.market.get_trades()
        expected = {
            "stock_symbol": {0: "JUICE"},
            "timestamp": {0: Timestamp("2023-10-05 14:00:00")},
            "quantity": {0: 100},
            "trade_type": {0: "buy"},
            "price": {0: 150.0},
        }
        self.assertDictEqual(trades.to_dict(), expected)

    def test_add_multiple_trades(self):
        self.market.add_trade(self.trade_a)
        self.market.add_trade(self.trade_b)
        trades = self.market.get_trades()
        expected = {
            "stock_symbol": {0: "JUICE", 1: "MILK"},
            "timestamp": {
                0: Timestamp("2023-10-05 14:00:00"),
                1: Timestamp("2023-10-06 10:00:00"),
            },
            "quantity": {0: 100, 1: 200},
            "trade_type": {0: "buy", 1: "sell"},
            "price": {0: 150.0, 1: 2500.0},
        }
        self.assertDictEqual(trades.to_dict(), expected)

    def test_get_trades_with_filter(self):
        self.market.add_trade(self.trade_a)
        self.market.add_trade(self.trade_b)
        trades = self.market.get_trades("stock_symbol == 'JUICE'")
        expected = {
            "stock_symbol": {0: "JUICE"},
            "timestamp": {0: Timestamp("2023-10-05 14:00:00")},
            "quantity": {0: 100},
            "trade_type": {0: "buy"},
            "price": {0: 150.0},
        }
        self.assertDictEqual(trades.to_dict(), expected)

    def test_get_trades_with_no_trades_filter(self):
        self.market.add_trade(self.trade_a)
        self.market.add_trade(self.trade_b)
        no_trades_filter = "stock_symbol == 'INVALID'"
        result = self.market.get_trades(no_trades_filter)
        self.assertTrue(result.empty, f"Trade filter {no_trades_filter} is expected to return empty data")

    def test_flush_trades(self):
        self.market.add_trade(self.trade_a)
        self.market.add_trade(self.trade_b)
        self.market._flush_trades()
        trades = self.market.get_trades()
        expected = {}
        self.assertDictEqual(trades.to_dict(), expected)

    def test_large_number_of_trades(self):
        # Adding a large number of trades for multiple stocks
        num_trades = 100000
        for i in range(num_trades):
            stock_symbol = ['JUICE', 'MILK', 'WATER', 'SODA'][i % 4]
            trade = Trade(
                stock_symbol = stock_symbol,
                timestamp = datetime(2023, 10, 5, 14, 0),
                quantity = i + 1,
                trade_type = TradeType.BUY if i % 2 == 0 else TradeType.SELL,
                price = 150.0 + i
            )
            self.market.add_trade(trade)

        trades = self.market.get_trades()
        # Ensure all trades are added
        self.assertEqual(len(trades), num_trades)

        # Filtering for specific stock
        juice_trades = self.market.get_trades("stock_symbol == 'JUICE'")
        juice_count = len(juice_trades)
        self.assertEqual(juice_count, num_trades // 4)

        milk_trades = self.market.get_trades("stock_symbol == 'MILK'")
        milk_count = len(milk_trades)
        self.assertEqual(milk_count, num_trades // 4)

        water_trades = self.market.get_trades("stock_symbol == 'WATER'")
        water_count = len(water_trades)
        self.assertEqual(water_count, num_trades // 4)

        soda_trades = self.market.get_trades("stock_symbol == 'SODA'")
        soda_count = len(soda_trades)
        self.assertEqual(soda_count, num_trades // 4)

        # Filtering for buy trades
        buy_trades = self.market.get_trades("trade_type == 'buy'")
        self.assertEqual(len(buy_trades), num_trades // 2)

        # Filtering for sell trades
        sell_trades = self.market.get_trades("trade_type == 'sell'")
        self.assertEqual(len(sell_trades), num_trades // 2)