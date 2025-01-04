from pandas_emetrics.processing import k_anonymize
import pandas as pd
import unittest

class TestKAnonymize(unittest.TestCase):

    def test_inplace(self):
        df = pd.DataFrame({'Q1': [1, 4, 3, 2, 6, 5], 'Q2': [20, 40, 60, 30, 50, 10]})
        orig_df = df.copy(deep=True)
        correct_df = pd.DataFrame({'Q1': ['[1-3]', '[4-6]', '[1-3]', '[1-3]', '[4-6]', '[4-6]'],
                                   'Q2': ['[20-60]', '[10-50]', '[20-60]', '[20-60]', '[10-50]', '[10-50]']})
        
        df.k_anonymize(quasi=['Q1', 'Q2'], k=2, inplace=True)

        self.assertFalse(df.equals(orig_df))
        self.assertTrue(df.equals(correct_df))

    def test_not_inplace(self):
        df = pd.DataFrame({'Q1': [1, 4, 3, 2, 6, 5], 'Q2': [20, 40, 60, 30, 50, 10]})
        orig_df = df.copy(deep=True)
        correct_df = pd.DataFrame({'Q1': ['[1-3]', '[4-6]', '[1-3]', '[1-3]', '[4-6]', '[4-6]'],
                                   'Q2': ['[20-60]', '[10-50]', '[20-60]', '[20-60]', '[10-50]', '[10-50]']})

        new_df = df.k_anonymize(quasi=['Q1', 'Q2'], k=2)

        self.assertTrue(df.equals(orig_df))
        self.assertTrue(new_df.equals(correct_df))
    

if __name__ == '__main__':
    unittest.main()