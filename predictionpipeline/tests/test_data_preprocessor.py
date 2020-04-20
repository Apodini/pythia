""" unittests for data_preprocessor.py
"""
import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from data_preprocessor import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    """ unittests for DataPreprocessor
    """

    def test_preprocess_empty_data(self):
        """ test preprocess_data with empty df
        """
        df = pd.DataFrame(columns=['traceid', 'sessionid', 'servicessequence', 'starttime'])
        df = DataPreprocessor().preprocess_data(df)
        assert_frame_equal(df, df)

    def test_preprocess_data(self):
        """ test preprocess_data with normal df
        """
        df = pd.DataFrame([['1234', '1234', 'front-end,carts,front-end', '1234']], columns=['traceid', 'sessionid', 'servicessequence', 'starttime'])
        df = DataPreprocessor().preprocess_data(df)
        df_test = pd.DataFrame([['1234', '1234', 'front-end,carts', '1234', 1]], columns=['traceid', 'sessionid', 'servicessequence', 'starttime', 'currentclusternumber'])
        assert_frame_equal(df.sort_index(axis=1), df_test.sort_index(axis=1), check_dtype=False, check_index_type=False)


if __name__ == '__main__':
    # execute only if run as a script
    unittest.main()
