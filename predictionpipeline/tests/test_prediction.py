""" unittests for prediction.py
"""
import unittest

from entities.prediction import Prediction
from entities.service import Service

class TestPrediction(unittest.TestCase):
    """ unittests for Prediction
    """
    def test_convert_prediction(self):
        """ test preprocess_data with empty df
        """
        # TODO: Mock Service?
        result = ['front-end']
        prediction = Prediction(result)
        services = []
        service = Service('front-end', 1, 'sock-shop')
        services.append(service)
        print(prediction.services[0].__dict__)
        self.assertEqual(len(prediction.services), len(services))
        self.assertEqual(prediction.services[0].__dict__, services[0].__dict__)

if __name__ == '__main__':
    # execute only if run as a script
    unittest.main()
