'''
    This is a test program to test main methods of Trader Made data provider class.
'''

from data_provider_trader_made import DataProviderTraderMade
from data_provider_abstract import DataProviderSource
import unittest
import os
from utils import Utils
from dotenv import load_dotenv
load_dotenv()

class TestTraderMade(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls._data_provider = DataProviderTraderMade(
            saving_directory=Utils.get_path('outputs/financial_data/trader_made/'),
            save_data_on_each_request=True,
            data_provider_source=DataProviderSource.LOCAL,
            api_key=os.getenv('trader_made_api_key')
        )

    def test_data_provider_trader_made(self):
        
        data = self._data_provider.get_daily_candles(symbol='EURUSD')
        self.assertGreater(data.shape[0], 0)
        
if __name__ == '__main__':
    unittest.main()
    