'''
    This class would preprocess and verify data integrity.
'''

import pandas as pd
from datetime import datetime
import os
import pickle

class PreprocessRawData:
    
    def __init__(self, **kwargs):
        
        self._saving_directory = kwargs.get('saving_directory')

        self._dataset:pd.DataFrame = kwargs.get('dataset')
    
    def rename_fields(self):
        
        self._dataset.rename(
            columns={
                'Datetime': 'datetime_str',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            },
            inplace=True
        )
    
    def sort_in_chronological_order(self):
        
        self._dataset.sort_values(by='timestamp', ascending=True, inplace=True)

    def verify_chronological_order(self):
        
        self._dataset['datetime'] = self._dataset['datetime_str'].apply(lambda ds: datetime.strptime(ds.split(':')[0], '%Y-%m-%d %H'))
        self._dataset['date'] = self._dataset['datetime'].apply(lambda d: d.date())
        self._dataset['timestamp'] = self._dataset['datetime'].apply(lambda d: d.timestamp())
        timestamps_diffs = self._dataset['timestamp'].diff()
        timestamps_diffs.dropna(inplace=True)
        timestamps_diffs_sign = timestamps_diffs.apply(lambda time_difference: time_difference > 0)
        
        return timestamps_diffs_sign.all()
    
    def verify_fields_integrity(self):
        
        is_high_the_highest_value = self._dataset.apply(
            lambda record:
            record['high']>=record.filter(['high', 'open', 'low', 'close']).max(),
            axis=1
        ).all()
    
        is_low_the_lowest_value = self._dataset.apply(
            lambda record:
            record['low']<=record.filter(['high', 'open', 'low', 'close']).min(),
            axis=1
        ).all()
        
        is_open_in_the_middle = self._dataset.apply(
            lambda record:
            record['open']>=record.filter(['high', 'open', 'low', 'close']).min() and record['open']<=record.filter(['high', 'open', 'low', 'close']).max(),
            axis=1
        ).all()
        
        is_close_in_the_middle = self._dataset.apply(
            lambda record:
            record['close']>=record.filter(['high', 'open', 'low', 'close']).min() and record['close']<=record.filter(['high', 'open', 'low', 'close']).max(),
            axis=1
        ).all()
        
        return is_high_the_highest_value and is_low_the_lowest_value and is_open_in_the_middle and is_close_in_the_middle
           
    def verify_type_integrity(self):
        
        types = self._dataset.dtypes
        
        return types['open'] == float and types['close'] == float and types['high'] == float and types['low'] == float
    
    def verify_market_hours(self):
        
        self._dataset['day_of_week'] = self._dataset['datetime'].apply(lambda d: d.day_of_week)
        
        return len(self._dataset[self._dataset['day_of_week'].isin([5, 6])]) == 0
    
    def verify_time_integrity(self):
        
        dataset_copy = self._dataset.copy()
        dataset_copy['timestamp_diff'] = dataset_copy['timestamp'].diff()
        dataset_copy.dropna(inplace=True)
        timestamp_diffs_validation = dataset_copy.apply(
            lambda record: record['timestamp_diff'] == 60*60 if record['day_of_week'] != 0 else record['timestamp_diff'] == 259200.0,
            axis=1
        )
        
        return timestamp_diffs_validation.all()
        
    def verify_missing_values(self):
        
        return self._dataset.isna().any().any() 
    
    def verify_dataset(self):
        
        self.rename_fields()
    
        if not self.verify_chronological_order():
            self.sort_in_chronological_order()
        
        if not self.verify_fields_integrity():
            print('OHLC fields rational order is not verified.')
            return False
        
        if not self.verify_type_integrity():
            print('OHLC fields types are not safe.')
            return False
            
        if not self.verify_market_hours():
            print('There are data points which are dated as Saturday or Sunday.')
            return False
        
        if self.verify_missing_values():
            print('There are some null values in this dataset. Please fill these values.') 
            return False

        return True
    
    def filter_columns_of_interest(self):
        
        self._dataset = self._dataset.filter(
            [
                'datetime_str',
                'datetime',
                'date',
                'timestamp',
                'day_of_week',
                'hour_of_day',
                'day_of_year',
                'open',
                'high',
                'low',
                'close'
            ]
        )
    
    def store_dataset(self):
        
        os.makedirs(self._saving_directory, exist_ok=True)
        
        with open(os.path.join(self._saving_directory, 'processed_dataset.pickle'), 'wb') as f:
            pickle.dump(self._dataset, f)
        
    def prepare_dataset(self):
        
        if self.verify_dataset():   
            
            self.filter_columns_of_interest()
             
            self.store_dataset()    
            
            return True
        
        else:
            return False