
from common.constants import FIXED_DIVIDEND_PCT, LAST_DIVIDEND, PAR_VALUE, STOCK_SYMBOL, STOCK_TYPE, StockType
from exchange.stock import Stock, StockInfo
import unittest


class TestStock(unittest.TestCase):
    def test_stock_initialization(self):
        stock = Stock(stock_symbol='BEER', type=StockType.COMMON, last_dividend=0.85, fixed_dividend_pct=0.0, par_value=100.0)
        self.assertEqual(stock.stock_symbol, 'BEER')
        self.assertEqual(stock.type, StockType.COMMON.value)
        self.assertEqual(stock.last_dividend, 0.85)
        self.assertEqual(stock.fixed_dividend_pct, 0.0)
        self.assertEqual(stock.par_value, 100.0)

    def test_negative_fixed_dividend_pct(self):
        with self.assertRaises(ValueError):
            Stock(stock_symbol='WINE', type=StockType.PREFERRED, last_dividend=2.0, fixed_dividend_pct=-0.1, par_value=50.0)

    def test_negative_par_value(self):
        with self.assertRaises(ValueError):
            Stock(stock_symbol='WHISKEY', type=StockType.PREFERRED, last_dividend=2.0, fixed_dividend_pct=0.1, par_value=-50.0)

    def test_repr(self):
        stock = Stock(stock_symbol='RUM', type=StockType.COMMON, last_dividend=1.5, fixed_dividend_pct=0.0, par_value=100.0)
        self.assertEqual(repr(stock), "Stock(stock_symbol='RUM', type='Common', last_dividend=1.5, fixed_dividend_pct=0.0, par_value=100.0)")



class TestStockInfo(unittest.TestCase):
    # @patch('logging.info')
    def setUp(self):
        self.stock_info = StockInfo()
        self.stock_a = Stock(stock_symbol='RUM', type=StockType.COMMON, last_dividend=0.8, fixed_dividend_pct=0.0, par_value=100.0)
        self.stock_b = Stock(stock_symbol='BEER', type=StockType.PREFERRED, last_dividend=1.0, fixed_dividend_pct=0.02, par_value=200.0)
        self.stock_info.add_stocks([self.stock_a, self.stock_b])

    def test_add_stocks(self):
        expected = {
                    'type': {'RUM': 'Common', 'BEER': 'Preferred'},
                    'last_dividend': {'RUM': 0.8, 'BEER': 1.0},
                    'fixed_dividend_pct': {'RUM': 0.0, 'BEER': 0.02},
                    'par_value': {'RUM': 100.0, 'BEER': 200.0}
                }
        self.assertDictEqual(self.stock_info.get_all_stocks().to_dict(), expected)
        self.stock_info._remove_all_stocks()

    def test_duplicate_stock_symbols(self):
        with self.assertRaises(ValueError):
            self.stock_info.add_stocks([self.stock_a])  # Adding the same stock again
        self.stock_info._remove_all_stocks()


    def test_get_stock_info(self):
        result = self.stock_info.get_stock_info('RUM').to_dict()
        expected = {'type': 'Common', 'last_dividend': 0.8, 'fixed_dividend_pct': 0.0, 'par_value': 100.0}
        self.assertDictEqual(result, expected)
        self.stock_info._remove_all_stocks()

    def test_get_stock_info_invalid(self):
        with self.assertRaises(ValueError):
            self.stock_info.get_stock_info('INVALID')
        self.stock_info._remove_all_stocks()

    def test_is_valid_stock(self):
        self.assertTrue(self.stock_info.is_valid_stock('RUM'))
        self.assertTrue(self.stock_info.is_valid_stock('BEER'))
        self.assertFalse(self.stock_info.is_valid_stock('WHISKEY'))
        self.stock_info._remove_all_stocks()