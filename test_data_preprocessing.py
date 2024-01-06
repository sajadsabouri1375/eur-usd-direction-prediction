'''
    This is a test program to test main methods of data preprocessing.
'''

from data_provider_yfinance import DataProviderYfinance, DataProviderSource
from data_preprocessing import PreprocessRawData
import unittest
import os
from utils.utils import Utils
from dotenv import load_dotenv
load_dotenv()

class TestPreprocessDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls._data_provider = DataProviderYfinance(
            saving_directory=Utils.get_path('outputs/financial_data/yfinance/'),
            save_data_on_each_request=True,
            data_provider_source=DataProviderSource.LOCAL
        )
        
        data = cls._data_provider.get_hourly_candles(symbol='EURUSD=X')
        
        cls._data_preprocessor = PreprocessRawData(
            saving_directory=Utils.get_path('outputs/preprocessed_datasets/'),
            dataset=data
        )

    def test_preprocess_dataset(self):
        
        self.assertTrue(self._data_preprocessor.prepare_dataset())
    
if __name__ == '__main__':
    unittest.main()
    