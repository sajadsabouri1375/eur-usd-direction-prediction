'''
    This is an abstract class which implements the very basic behaviors and properties of all operators in this project.
'''

from abc import ABC


class OperationParentAbstract(ABC):
    
    def __init__(self, **kwargs):
        super().__init__()
        
        self._plot_saving_directory = kwargs.get('plot_saving_directory', 'outputs')