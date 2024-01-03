'''
    This is an abstract class which hosts generic properties and behaviors that all
    data providers must have. In this class we implement methods and properties which 
    might be used in all concerete data provider classes.
'''

from abc import ABC
from enum import Enum

# This enum includes two main sources: 
# LOCAL for loading data from local machine hard dist (in case data is previously requested from external sources and is online enough)
# EXTERNAL for requesting latest data from external sources
class DataProviderSource(Enum):
    LOCAL = 1
    EXTERNAL = 2


class DataProviderAbstract(ABC):
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        
        self._saving_directory = kwargs.get('saving_directory')
        self._save_data_on_each_request = kwargs.get('save_data_on_each_request', True)
        self._data_provider_source = kwargs.get('data_provider_source', DataProviderSource.LOCAL)