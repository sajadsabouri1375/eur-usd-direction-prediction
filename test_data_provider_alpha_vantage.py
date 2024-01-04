'''
    This is a test program to test main methods of Alpha Vantage data provider class.
'''

from data_provider_alpha_vantage import DataProviderAlphaVantage
from data_provider_abstract import DataProviderSource
import unittest
import os
from utils.utils import Utils
from dotenv import load_dotenv
load_dotenv()

class TestAlphaVantage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls._data_provider = DataProviderAlphaVantage(
            saving_directory=Utils.get_path('outputs/financial_data/alpha_vantage/'),
            save_data_on_each_request=True,
            data_provider_source=DataProviderSource.LOCAL,
            api_key=os.getenv('alpha_vantage_api_key')
        )

    def test_data_provider_alpha_vantage(self):
        
        data, meta_data = self._data_provider.get_daily_candles(symbol='EURUSD', adjusted=False)
        
        self.assertEqual('EURUSD', meta_data['2. Symbol'])
        self.assertEqual('US/Eastern', meta_data['5. Time Zone'])
    
if __name__ == '__main__':
    unittest.main()
    