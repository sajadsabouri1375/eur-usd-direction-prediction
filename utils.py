'''
    This static class includes a bunch of handy methods. 
    We may use these methods at any classes within this project.
'''

import os
from abc import ABC, abstractmethod


class Utils:
    
    @abstractmethod
    def get_path(path:str):
        '''
            Input: A directory within an os (linux/windows format)
            Output: The directory in the format of the machine operating system on which the program is running.
        '''
        
        # If path is defined in linux format
        address = os.path.join(*path.split('/'))

        # If windows address
        address = os.path.join(*address.split('\\'))

        root_project_dir = os.path.dirname(__file__)

        return os.path.join(root_project_dir, address)