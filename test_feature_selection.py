'''
    This is a test program to test main feature selection methods.
'''

from feature_selection import FeatureSelection
import unittest
import pickle
from utils.utils import Utils

class TestFeatureSelection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        with open(Utils.get_path('outputs/preprocessed_datasets/features_dataset.pickle'), 'rb') as f:
            cls._dataset = pickle.load(f)

        cls._feature_selector = FeatureSelection(
            plot_saving_directory=Utils.get_path('outputs/plots/'),
            saving_directory=Utils.get_path('outputs/preprocessed_datasets/'),
            features_dataset=cls._dataset
        )
        
    def test_feature_selection(self):
        
        self._feature_selector.select_features()
    
if __name__ == '__main__':
    unittest.main()
    