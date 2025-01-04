from pandas_emetrics.processing import k_anonymize
from pandas_emetrics.metrics import k_anonymity
import pandas as pd
import unittest
import random

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

    def test_anonymize(self):
        q1 = []
        q2 = []
        for _ in range(100):
            q1.append(random.randint(0, 99))
            q2.append(random.randint(100, 200))

        df = pd.DataFrame({'Q1': q1, 'Q2': q2})

        # tests df on k = [1, ... , 100]
        for k in range(1, 101):
            anon_df = df.k_anonymize(quasi=['Q1', 'Q2'], k=k)
            # test if k >= because if k = x anonymous, k also = x-1, x-2, ..., 1 anonymous 
            self.assertTrue(anon_df.k_anonymity(quasi=['Q1', 'Q2']) >= k)
    
    def test_exceptions(self):
        df = pd.DataFrame({'Q1': [1, 2, 3, 4, 5]})

        self.assertRaises(ValueError, lambda: df.k_anonymize(quasi=['Q1'], k=6))
        self.assertRaises(ValueError, lambda: df.k_anonymize(quasi=['Q1'], k=0))
        self.assertRaises(ValueError, lambda: df.k_anonymize(quasi=['Q1'], k=-100))


if __name__ == '__main__':
    unittest.main()