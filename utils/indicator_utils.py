'''
    Utility function to calculate famous trading indicators.
'''

import pandas as pd
import numpy as np


class IndicatorUtils:
    
    @staticmethod
    def calculate_moving_average(dataset, n_intervals):
        
        moving_average_series = pd.Series(dataset['close'].rolling(n_intervals).mean()) 
        
        dataset[f'ma_{n_intervals}'] = moving_average_series
         
        return dataset

    @staticmethod
    def calculate_exponentially_weighted_moving_average(dataset, n_intervals): 
        
        ewma = pd.Series(dataset['close'].ewm(span = n_intervals, min_periods = n_intervals - 1).mean()) 
        
        dataset[f'ewma_{n_intervals}'] = ewma
        
        return dataset

    @staticmethod
    def calculate_relative_strength_index(dataset, n_intervals):
        
        close_diffs = dataset['close'].diff()

        # Make two series: one for lower closes and one for higher closes
        up = close_diffs.clip(lower=0)
        down = -1 * close_diffs.clip(upper=0)
        
        ma_up = up.ewm(com = n_intervals - 1, adjust=True, min_periods = n_intervals).mean()
        ma_down = down.ewm(com = n_intervals - 1, adjust=True, min_periods = n_intervals).mean()

        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        
        dataset[f'rsi_{n_intervals}'] = rsi
        
        return dataset    

    @staticmethod    
    def calculate_average_true_range(dataset, n_intervals=14):
        
        true_range = np.amax(np.vstack(((dataset['high'] - dataset['low']).to_numpy(), (abs(dataset['high'] - dataset['close'])).to_numpy(), (abs(dataset['low'] - dataset['close'])).to_numpy())).T, axis=1)
        
        dataset[f'atr_{n_intervals}'] = pd.Series(true_range).rolling(n_intervals).mean()
        
        return dataset