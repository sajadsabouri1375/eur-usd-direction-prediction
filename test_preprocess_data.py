'''
    This is a test program to test main methods of Alpha Vantage data provider class.
'''

from data_provider_alpha_vantage import DataProviderAlphaVantage, DataProviderSource
from preprocess_data import PreprocessRawData
import unittest
import os
from utils import Utils
from dotenv import load_dotenv
load_dotenv()

class TestPreprocessDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls._data_provider = DataProviderAlphaVantage(
            saving_directory=Utils.get_path('outputs/financial_data/alpha_vantage/'),
            save_data_on_each_request=True,
            data_provider_source=DataProviderSource.LOCAL,
            api_key=os.getenv('alpha_vantage_api_key')
        )
        
        data, meta_data = cls._data_provider.get_daily_candles(symbol='EURUSD', adjusted=False)
        
        cls._data_preprocessor = PreprocessRawData(
            saving_directory=Utils.get_path('outputs/preprocessed_datasets/'),
            dataset=data
        )

    def test_preprocess_dataset(self):
        
        self.assertTrue(self._data_preprocessor.prepare_dataset())
    
if __name__ == '__main__':
    unittest.main()
    