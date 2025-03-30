import unittest
from datetime import datetime, timedelta

import pandas as pd
from calculators.trade_stats import VolumeWeightedStockPriceCalculator, AllShareIndexCalculator
from exchange.stock import Stock, StockInfo
from exchange.trade import Trade
from exchange.market import Market
from common.constants import StockType, TradeType
from scipy.stats import gmean


class TestTradeStatsCalculators(unittest.TestCase):
    """Test cases for VolumeWeightedStockPriceCalculator and AllShareIndexCalculator."""

    @classmethod
    def setUpClass(cls):
        """Set up StockInfo and Market instances with sample data for testing."""

        cls.stock_info = StockInfo()

        # Create stock objects
        stock1 = Stock(
            stock_symbol='ABC',
            type=StockType.COMMON,
            last_dividend=5.0,
            fixed_dividend_pct=0.0,
            par_value=100.0
        )

        stock2 = Stock(
            stock_symbol='XYZ',
            type=StockType.PREFERRED,
            last_dividend=8.0,
            fixed_dividend_pct=2.0,
            par_value=100.0
        )

        stock3 = Stock(
            stock_symbol='DEF',
            type=StockType.COMMON,
            last_dividend=4.0,
            fixed_dividend_pct=0.0,
            par_value=100.0
        )

        # Add stocks to StockInfo
        cls.stock_info.add_stocks([stock1, stock2, stock3])

        # Create trade objects within the last 5 minutes and some older than 5 minutes
        cls.market = Market()

        now = datetime.now()
        cls.market.add_trade(Trade(stock_symbol='ABC', timestamp=now, quantity=50, trade_type=TradeType.BUY, price=120.0))
        cls.market.add_trade(Trade(stock_symbol='XYZ', timestamp=now - timedelta(minutes=4), quantity=100, trade_type=TradeType.SELL, price=150.0))
        cls.market.add_trade(Trade(stock_symbol='DEF', timestamp=now - timedelta(minutes=6), quantity=60, trade_type=TradeType.BUY, price=110.0))

    @classmethod
    def tearDownClass(cls):
        cls.stock_info._remove_all_stocks()


    def test_vwsp_single_stock_within_5_minutes(self):
        """Test Volume Weighted Stock Price (VWSP) calculation for a single stock within the last 5 minutes."""

        calculator = VolumeWeightedStockPriceCalculator(stock_symbol='ABC')
        result = calculator.calculate()

        # VWSP for 'ABC': (price * quantity) / total quantity
        expected_vwsp = (120.0 * 50) / 50
        self.assertAlmostEqual(result, expected_vwsp, places=2)

    def test_vwsp_multiple_stocks_within_5_minutes(self):
        """Test VWSP calculation for all stocks within the last 5 minutes."""

        calculator = VolumeWeightedStockPriceCalculator()
        result = calculator.calculate()

        expected_vwsp_abc = 120.0
        expected_vwsp_xyz = (150.0 * 100) / 100

        self.assertAlmostEqual(result.loc[result['stock_symbol'] == 'ABC', 'volume_weighted_stock_price'].values[0], expected_vwsp_abc, places=2)
        self.assertAlmostEqual(result.loc[result['stock_symbol'] == 'XYZ', 'volume_weighted_stock_price'].values[0], expected_vwsp_xyz, places=2)

    def test_vwsp_no_trades_in_filter(self):
        """Test VWSP calculation with no trades matching the filter."""

        calculator = VolumeWeightedStockPriceCalculator(stock_symbol='DEF')
        result = calculator.calculate()

        # As there are no trades for 'DEF' within the last 5 minutes
        self.assertIsNone(result, "VWSP should be None when no trades are available in the filter.")

    def test_all_share_index(self):
        """Test All Share Index calculation based on VWSP of all stocks."""

        # First calculate VWSP for all stocks
        vwsp_calculator = VolumeWeightedStockPriceCalculator()
        vwsp_result = vwsp_calculator.calculate()

        # Calculate All Share Index
        all_share_index_calculator = AllShareIndexCalculator(vwsp_result)
        result = all_share_index_calculator.calculate()

        # Geometric mean of VWSP values
        vwsp_values = vwsp_result['volume_weighted_stock_price'].values
        expected_index = gmean(vwsp_values)

        self.assertAlmostEqual(result, expected_index, places=2)

    def test_all_share_index_no_valid_prices(self):
        """Test All Share Index calculation with no valid prices."""

        empty_vwsp_result = pd.DataFrame(columns=['stock_symbol', 'volume_weighted_stock_price'])

        all_share_index_calculator = AllShareIndexCalculator(empty_vwsp_result)
        result = all_share_index_calculator.calculate()

        self.assertEqual(result, 0.0, "All Share Index should be 0 when no valid prices are available.")


class TestTradeStatsCalculatorsLargeData(unittest.TestCase):
    """Test cases for VolumeWeightedStockPriceCalculator and AllShareIndexCalculator with large data."""

    @classmethod
    def setUpClass(cls):
        """Set up StockInfo and Market instances with a large dataset for testing."""

        # Create StockInfo instance and add some stock objects
        cls.stock_info = StockInfo()

        stock1 = Stock(
            stock_symbol='ABC',
            type=StockType.COMMON,
            last_dividend=5.0,
            fixed_dividend_pct=0.0,
            par_value=100.0
        )

        stock2 = Stock(
            stock_symbol='XYZ',
            type=StockType.PREFERRED,
            last_dividend=8.0,
            fixed_dividend_pct=2.0,
            par_value=100.0
        )

        # Add stocks to StockInfo
        cls.stock_info.add_stocks([stock1, stock2])

        # Create Market instance and add a large number of trade objects
        cls.market = Market()

        now = datetime.now()
        trade_list = []

        # Creating trades for stock 'ABC' within the last 5 minutes
        for i in range(45000):
            trade_list.append(Trade(stock_symbol='ABC', timestamp=now - timedelta(seconds=i//200), quantity=100, trade_type=TradeType.BUY, price=50.0 + (i % 100)))

        # Creating trades for stock 'ABC' outside the last 5 minutes
        for i in range(5000):
            trade_list.append(Trade(stock_symbol='ABC', timestamp=now - timedelta(minutes=6) - timedelta(seconds=i//200), quantity=100, trade_type=TradeType.BUY, price=50.0 + (i % 100)))

        # Creating trades for stock 'XYZ' within the last 5 minutes
        for i in range(45000):
            trade_list.append(Trade(stock_symbol='XYZ', timestamp=now - timedelta(seconds=i//200), quantity=200, trade_type=TradeType.SELL, price=100.0 + (i % 50)))

        # Creating trades for stock 'XYZ' outside the last 5 minutes
        for i in range(5000):
            trade_list.append(Trade(stock_symbol='XYZ', timestamp=now - timedelta(minutes=6) - timedelta(seconds=i//200), quantity=200, trade_type=TradeType.SELL, price=100.0 + (i % 50)))

        for trade in trade_list:
            cls.market.add_trade(trade)

    @classmethod
    def tearDownClass(cls):
        cls.stock_info._remove_all_stocks()

    def test_vwsp_large_data(self):
        """Test Volume Weighted Stock Price (VWSP) calculation with large data."""

        calculator = VolumeWeightedStockPriceCalculator(stock_symbol='ABC')
        result = calculator.calculate()

        # Compute the expected VWSP considering only the trades within the last 5 minutes
        valid_trades = [Trade(stock_symbol='ABC', timestamp=datetime.now() - timedelta(seconds=i//200), quantity=100, trade_type=TradeType.BUY, price=50.0 + (i % 100)) for i in range(45000)]
        total_trade_value = sum(trade.price * trade.quantity for trade in valid_trades)
        total_quantity = sum(trade.quantity for trade in valid_trades)
        expected_vwsp = total_trade_value / total_quantity

        self.assertAlmostEqual(result, expected_vwsp, places=2)

    def test_all_share_index_large_data(self):
        """Test All Share Index calculation with large data."""

        # Calculate VWSP for all stocks
        vwsp_calculator = VolumeWeightedStockPriceCalculator()
        vwsp_result = vwsp_calculator.calculate()

        # Calculate All Share Index
        all_share_index_calculator = AllShareIndexCalculator(vwsp_result)
        result = all_share_index_calculator.calculate()

        # Geometric mean of VWSP values
        vwsp_values = vwsp_result['volume_weighted_stock_price'].values
        expected_index = gmean(vwsp_values)

        self.assertAlmostEqual(result, expected_index, places=2)