'''
    This is a test program to test main methods of yfinance data provider class.
'''

from data_provider_yfinance import DataProviderYfinance
from data_provider_abstract import DataProviderSource
import unittest
import os
from utils.utils import Utils
from dotenv import load_dotenv
load_dotenv()

class TestYfinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls._data_provider = DataProviderYfinance(
            saving_directory=Utils.get_path('outputs/financial_data/yfinance/'),
            save_data_on_each_request=True,
            data_provider_source=DataProviderSource.LOCAL
        )

    def test_data_provider_yfinance(self):
        
        data = self._data_provider.get_daily_candles(symbol='EURUSD=X')
        self.assertGreater(data.shape[0], 0)
        
if __name__ == '__main__':
    unittest.main()
    