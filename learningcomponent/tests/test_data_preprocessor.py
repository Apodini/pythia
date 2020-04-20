""" unittests for data_preprocessor.py
"""
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from data_preprocessor import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    """ unittests for DataPreprocessor
    """
    def setUp(self):
        """ init DataPreprocessor
        """
        self.data_preprocessor = DataPreprocessor()

    def test_preprocess_empty_data(self):
        """ test preprocess_data with empty df
        """
        df = pd.DataFrame(columns=['traceid', 'sessionid', 'servicessequence', 'starttime'])
        df = self.data_preprocessor.preprocess_data(df)
        full_df = pd.DataFrame(columns=['sessionid', 'nextcluster', 'starttime'])
        assert_frame_equal(df, full_df)

    def test_preprocess_data(self):
        """ test preprocess_data with normal df
        """
        df = pd.DataFrame([['1234', '1234', 'service-1,service-2,service-1', '1234']], columns=['traceid', 'sessionid', 'servicessequence', 'starttime'])
        df = self.data_preprocessor.preprocess_data(df)
        full_df = pd.DataFrame([[0.0, '1234', '1234', 'service-1,service-2', '1234', 0, 0, 0]], columns=['index', 'traceid', 'sessionid', 'servicessequence', 'starttime', 'currentclusternumber', 'clustersequence', 'nextcluster'])
        assert_frame_equal(df.sort_index(axis=1), full_df.sort_index(axis=1), check_dtype=False, check_index_type=False)


if __name__ == '__main__':
    # execute only if run as a script
    unittest.main()
