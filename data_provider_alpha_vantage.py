'''
    This class includes required methods and properties to request data online using Alpha Vantage API.
'''

from data_provider_abstract import DataProviderAbstract, DataProviderSource
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import json
import os


class DataProviderAlphaVantage(DataProviderAbstract):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self._api_key = kwargs.get('api_key')
        
        self._api_interface = TimeSeries(
            key=self._api_key,
            output_format='pandas'
        )

    def save_data_to_local_machine(self, saving_directory, data, meta_data):
        
        os.makedirs(saving_directory, exist_ok=True)
        
        # Save pandas dataframe of raw data
        data.to_csv(os.path.join(saving_directory, "data.csv"))
                
        # Save meta data json file
        with open(os.path.join(saving_directory, "meta_data.json"), 'w') as f:
            json.dump(meta_data, f)
    
    def load_data_from_local_machine(self, loading_directory):
        
        # Load dataframe
        data = pd.read_csv(os.path.join(loading_directory, "data.csv"))
        
        # Load meta data json 
        with open(os.path.join(loading_directory, "meta_data.json"), 'r') as f:
            meta_data = json.load(f)
            
        return data, meta_data
    
    def get_hourly_candles(self, symbol):
        
        data_local_directory = f"{self._saving_directory}hourly_{symbol}"

        if self._data_provider_source == DataProviderSource.EXTERNAL:
            
            data, meta_data = self._api_interface.get_intraday(symbol=symbol, interval='60min', outputsize='full')
        
            if self._save_data_on_each_request:
                self.save_data_to_local_machine(data_local_directory, data, meta_data)

        elif self._data_provider_source == DataProviderSource.LOCAL:
            
            if not os.path.exists(data_local_directory):
                raise Exception('Data is never requested from Alpha Vantage, therefore it cannot be loaded locally. Please change to "EXTERNAL" mode for online requests.')
                exit()
                
            data, meta_data = self.load_data_from_local_machine(data_local_directory)
            
            
        return data, meta_data
    
    def get_daily_candles(self, symbol, adjusted=False):
        
        data_local_directory = f"{self._saving_directory}daily_{'adjusted_' if adjusted else ''}{symbol}"

        if self._data_provider_source == DataProviderSource.EXTERNAL:
            
            if adjusted:
                data, meta_data = self._api_interface.get_daily_adjusted(symbol=symbol, outputsize='full')
            
            else:
                data, meta_data = self._api_interface.get_daily(symbol=symbol, outputsize='full')
        
            if self._save_data_on_each_request:
                self.save_data_to_local_machine(data_local_directory, data, meta_data)

        elif self._data_provider_source == DataProviderSource.LOCAL:
            
            if not os.path.exists(data_local_directory):
                raise Exception('Data is never requested from Alpha Vantage, therefore it cannot be loaded locally. Please change to "EXTERNAL" mode for online requests.')
                exit()
                
            data, meta_data = self.load_data_from_local_machine(data_local_directory)
            
            
        return data, meta_data

