import unittest
from datetime import datetime
from calculators.stock_stats import DividendYieldCalculator, PERatioCalculator
from exchange.stock import Stock, StockInfo
from common.constants import StockType


class TestStockStatsCalculators(unittest.TestCase):
    """Test cases for DividendYieldCalculator and PERatioCalculator."""

    @classmethod
    def setUpClass(cls):
        """Set up a StockInfo instance and add a few stock objects for testing."""

        cls.stock_info = StockInfo()

        # Create stock objects
        stock_common = Stock(
            stock_symbol="ABC",
            type=StockType.COMMON,
            last_dividend=8.0,
            fixed_dividend_pct=0.0,
            par_value=100.0,
        )

        stock_preferred = Stock(
            stock_symbol="XYZ",
            type=StockType.PREFERRED,
            last_dividend=8.0,
            fixed_dividend_pct=2.0,
            par_value=100.0,
        )

        # Add stocks to StockInfo
        cls.stock_info.add_stocks([stock_common, stock_preferred])

    @classmethod
    def tearDownClass(cls):
        cls.stock_info._remove_all_stocks()


    def test_dividend_yield_common(self):
        """Test Dividend Yield for a common stock."""

        calculator = DividendYieldCalculator(stock_symbol="ABC", price=200.0)
        result = calculator.calculate()

        # The dividend yield for common stock is last_dividend / price
        expected_yield = 8.0 / 200.0
        self.assertAlmostEqual(result, expected_yield, places=2)


    def test_dividend_yield_preferred(self):
        """Test Dividend Yield for a preferred stock."""
        calculator = DividendYieldCalculator(stock_symbol="XYZ", price=200.0)
        result = calculator.calculate()

        # The dividend yield for preferred stock is (fixed_dividend_pct * par_value) / price
        expected_yield = (2.0 * 100.0) / 200.0
        self.assertAlmostEqual(result, expected_yield, places=2)


    def test_pe_ratio(self):
        """Test P/E Ratio calculation."""
        # For common stock
        calculator = PERatioCalculator(stock_symbol="ABC", price=200.0)
        result = calculator.calculate()

        # The PE ratio is price / dividend_yield
        dividend_yield = 8.0 / 200.0
        expected_pe = 200.0 / dividend_yield
        self.assertAlmostEqual(result, expected_pe, places=2)

        # For preferred stock
        calculator = PERatioCalculator(stock_symbol="XYZ", price=300.0)
        result = calculator.calculate()

        dividend_yield = (2.0 * 100.0) / 300.0
        expected_pe = 300.0 / dividend_yield
        self.assertAlmostEqual(result, expected_pe, places=2)


    def test_dividend_yield_zero_price(self):
        """Test Dividend Yield with zero price."""
        with self.assertRaises(ValueError):
            DividendYieldCalculator(stock_symbol="ABC", price=0).calculate()


    def test_pe_ratio_zero_price(self):
        """Test P/E Ratio with zero price."""
        with self.assertRaises(ValueError):
            PERatioCalculator(stock_symbol="ABC", price=0.0).calculate()


    def test_negative_price(self):
        """Test calculations with negative price."""
        with self.assertRaises(ValueError):
            DividendYieldCalculator(stock_symbol="ABC", price=-10.0).calculate()

        with self.assertRaises(ValueError):
            PERatioCalculator(stock_symbol="ABC", price=-10.0).calculate()


    def test_missing_stock_symbol(self):
        """Test calculations with a missing stock symbol."""
        with self.assertRaises(ValueError):
            DividendYieldCalculator(stock_symbol="MISSING", price=100.0).calculate()

        with self.assertRaises(ValueError):
            PERatioCalculator(stock_symbol="MISSING", price=100.0).calculate()

    def test_zero_dividend(self):
        """Test calculations with zero last dividend."""

        # Add a stock with zero last dividend
        stock_zero_dividend = Stock(
            stock_symbol='ZEROX',
            type=StockType.COMMON,
            last_dividend=0.0,
            fixed_dividend_pct=0.0,
            par_value=100.0
        )
        stock_info = StockInfo()
        stock_info.add_stocks([stock_zero_dividend])

        calculator = DividendYieldCalculator(stock_symbol='ZEROX', price=100.0)
        result = calculator.calculate()

        self.assertEqual(result, 0.0, "Dividend yield should be 0 when last dividend is zero.")
