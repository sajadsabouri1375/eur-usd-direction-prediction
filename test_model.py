'''
    This is a test program to test main modelling behaviors.
'''

from model import LstmModel 
import unittest
import pickle
from utils.utils import Utils

class TestModelling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        with open(Utils.get_path('outputs/datasets/modelling_dataset.pickle'), 'rb') as f:
            cls._dataset = pickle.load(f)

        cls._model = LstmModel(
            plot_saving_directory=Utils.get_path('outputs/plots/'),
            saving_directory=Utils.get_path('outputs/models/'),
            modelling_dataset=cls._dataset
        )
        
    def test_modelling(self):
        
        baseline_model_accuracy = self._dataset['label'].value_counts().max()/self._dataset['label'].value_counts().sum()
        print(f'=> Baseline model accuray: {baseline_model_accuracy}')
        training_model_accuracy, test_model_accuracy = self._model.run_model()
        self.assertGreater(test_model_accuracy, baseline_model_accuracy)
    
if __name__ == '__main__':
    unittest.main()
    