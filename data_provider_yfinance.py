'''
    This class includes required methods and properties to request data online using yfinance.
'''

from data_provider_abstract import DataProviderAbstract, DataProviderSource
import pandas as pd
import os
import yfinance as yf


class DataProviderYfinance(DataProviderAbstract):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
                
    def save_data_to_local_machine(self, saving_directory, data):
        
        os.makedirs(saving_directory, exist_ok=True)
        
        # Save pandas dataframe of raw data
        data.to_csv(os.path.join(saving_directory, "data.csv"))
    
    def load_data_from_local_machine(self, loading_directory):
        
        # Load dataframe
        data = pd.read_csv(os.path.join(loading_directory, "data.csv"))
            
        return data
    
    def get_daily_candles(self, symbol):
        
        data_local_directory = f"{self._saving_directory}daily_{symbol}"

        if self._data_provider_source == DataProviderSource.EXTERNAL:
                            
            symbol_data = yf.Ticker(symbol) 
            
            data = symbol_data.history(period="max", interval="1d")
            
            if self._save_data_on_each_request:
                self.save_data_to_local_machine(data_local_directory, data)

        elif self._data_provider_source == DataProviderSource.LOCAL:
            
            if not os.path.exists(data_local_directory):
                raise Exception('Data is never requested from yfinance API, therefore it cannot be loaded locally. Please change to "EXTERNAL" mode for online requests.')
                exit()
                
            data = self.load_data_from_local_machine(data_local_directory)
        
        return data
    
    def get_hourly_candles(self, symbol):
        
        data_local_directory = f"{self._saving_directory}hourly_{symbol}"

        if self._data_provider_source == DataProviderSource.EXTERNAL:
                            
            symbol_data = yf.Ticker(symbol) 
            
            data = symbol_data.history(period="2y", interval="60m")
            
            if self._save_data_on_each_request:
                self.save_data_to_local_machine(data_local_directory, data)

        elif self._data_provider_source == DataProviderSource.LOCAL:
            
            if not os.path.exists(data_local_directory):
                raise Exception('Data is never requested from yfinance API, therefore it cannot be loaded locally. Please change to "EXTERNAL" mode for online requests.')
                exit()
                
            data = self.load_data_from_local_machine(data_local_directory)
            
        return data

