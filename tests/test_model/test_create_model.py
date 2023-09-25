import os
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import create_model
import tensorflow as tf

class TestCreateModel(unittest.TestCase):
    def test_create_model(self):
        # Test case 1: Check if the returned model is an instance of Sequential
        model = create_model(seed=42)
        assert isinstance(model, tf.keras.Sequential)
        
        # Test case 2: Check if the model has the correct number of layers
        assert len(model.layers) == 7 # 3 hidden layers + 3 dropout layers + 1 output
        
        # Test case 3: Check if the model's first layer has the correct activation function
        assert model.layers[0].activation.__name__ == "elu"
        
        # Test case 4: Check if the model's last layer has the correct number of units
        assert model.layers[-1].units == 1
        
        # Test case 5: Check if the model's optimizer is Adam with the correct learning rate
        assert isinstance(model.optimizer, tf.keras.optimizers.Adam) or isinstance(model.optimizer, tf.keras.optimizers.legacy.Adam)
        assert model.optimizer.learning_rate == 1e-3

if __name__ == '__main__':
    unittest.main()