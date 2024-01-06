'''
    Feature selection class would provide methods and properties to evaluate each feature against output feature.
    The candidate features would be evaluated and the best set of features would be selected for final modelling.
'''

from operation_abstract import OperationParentAbstract
import pandas as pd
from utils.plot_utils import PlotUtils
import os
import pickle
from datetime import datetime


class FeatureSelection(OperationParentAbstract):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._saving_directory = kwargs.get('saving_directory')
        self._dataset:pd.DataFrame = kwargs.get('features_dataset')
    
    def drop_nan_records(self):
        
        self._dataset.dropna(inplace=True)
        
    def plot_categorical_against_output(self):
        
        dataset_copy = self._dataset.copy()
        categorical_features = ['month_index', 'day_of_week', 'hour']
        
        PlotUtils.plot_percentage_stacked(
            dataset_copy,
            categorical_features, 
            "Categorical Features Selection Part I",
            os.path.join(self._plot_saving_directory, "categorical_features_stacked_part_01.jpg"),
            number_of_columns=1
        )
    
        dataset_copy['label_-1'] = dataset_copy['label'].shift(1).dropna()
        categorical_features = ['is_holiday', 'label_-1']
        
        PlotUtils.plot_percentage_stacked(
            dataset_copy,
            categorical_features, 
            "Categorical Features Selection Part II",
            os.path.join(self._plot_saving_directory, "categorical_features_stacked_part_02.jpg"),
            number_of_columns=2
        )
        
    def plot_continuous_against_output(self):
        
        dataset_copy = self._dataset.copy()
        dataset_copy['close_-1'] = dataset_copy['close'].shift(1)
        dataset_copy['open_-1'] = dataset_copy['open'].shift(1)
        dataset_copy['high_-1'] = dataset_copy['high'].shift(1)
        dataset_copy['low_-1'] = dataset_copy['low'].shift(1)
        dataset_copy['ma_7_-1'] = dataset_copy['ma_7'].shift(1)
        dataset_copy['ma_14_-1'] = dataset_copy['ma_14'].shift(1)
        dataset_copy['ma_28_-1'] = dataset_copy['ma_28'].shift(1)
        dataset_copy['atr_14_-1'] = dataset_copy['atr_14'].shift(1)
        dataset_copy['rsi_14_-1'] = dataset_copy['rsi_14'].shift(1)

        dataset_copy = dataset_copy.dropna()
        
        continuous_features_ohlc = ['close_-1', 'open_-1', 'high_-1', 'low_-1']
        
        PlotUtils.histogram_plots(
            dataset_copy, 
            continuous_features_ohlc,
            "OHLC Shift(-1) Features Selection",
            os.path.join(self._plot_saving_directory, "ohlc_features_distributions.jpg"),
            number_of_columns=2
        )
    
        continuous_features_ma = ['ma_7_-1', 'ma_14_-1', 'ma_28_-1']
        
        PlotUtils.histogram_plots(
            dataset_copy, 
            continuous_features_ma,
            "Moving Average Features Selection",
            os.path.join(self._plot_saving_directory, "ma_features_distributions.jpg"),
            number_of_columns=2
        )
        
        continuous_features_other_indicators = ['atr_14_-1', 'rsi_14_-1']
        
        PlotUtils.histogram_plots(
            dataset_copy, 
            continuous_features_other_indicators,
            "ATR/RSI Features Selection",
            os.path.join(self._plot_saving_directory, "atr_rsi_features_distributions.jpg"),
            number_of_columns=2
        )
    
    def store_dataset(self):
        
        os.makedirs(self._saving_directory, exist_ok=True)
        
        self._dataset = self._dataset.drop(
            columns=[
                'date',
                'datetime',
                'datetime_str',
                'timestamp'
            ]
        )
        
        self._dataset = self._dataset.reset_index(drop=True)
        
        with open(os.path.join(self._saving_directory, 'modelling_dataset.pickle'), 'wb') as f:
            pickle.dump(self._dataset, f)        
        
        
    def select_features(self):
        
        # Categorical features
        self.plot_categorical_against_output()
        
        # Continuous features
        self.plot_continuous_against_output()
    
        self.drop_nan_records()
        
        self.store_dataset()