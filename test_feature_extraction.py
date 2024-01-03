'''
    This is a test program to test main feature extraction methods.
'''

from feature_extraction import FeatureExtraction
import unittest
import pickle
from utils import Utils

class TestFeatureExtraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        with open(Utils.get_path('outputs/preprocessed_datasets/processed_dataset.pickle'), 'rb') as f:
            cls._dataset = pickle.load(f)

        cls._feature_extractor = FeatureExtraction(
            saving_directory=Utils.get_path('outputs/preprocessed_datasets/'),
            preprocessed_dataset=cls._dataset
        )
        
    def test_feature_extraction(self):
        
        self._feature_extractor.extract_features()
    
if __name__ == '__main__':
    unittest.main()
    