from pandas_emetrics.processing import k_anonymize
from pandas_emetrics.metrics import k_anonymity
import pandas as pd
import unittest
import random
import time

def create_random_df(rows: int, cols: int) -> pd.DataFrame:
    """
    Creates a shape (cols, rows) DataFrame filled with random integers [0, 100] 
    """

    data = []
    for _ in range(rows):
        row = [random.randint(0, 100) for _ in range(cols)]
        data.append(row)

    return pd.DataFrame(data, columns=list(range(cols)))


class TestKAnonymize(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

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
        df = create_random_df(100, 5)
        quasi_ids = list(range(0, 5))

        for k in range(1, 101):
            anon_df = df.k_anonymize(quasi=quasi_ids, k=k)
            # test if k >= because if k = x anonymous, k also = x-1, x-2, ..., 1 anonymous 
            self.assertGreaterEqual(anon_df.k_anonymity(quasi=quasi_ids), k)
    
    def test_exceptions(self):
        df = pd.DataFrame({'Q1': [1, 2, 3, 4, 5]})

        self.assertRaises(ValueError, lambda: df.k_anonymize(quasi=['Q1'], k=6))
        self.assertRaises(ValueError, lambda: df.k_anonymize(quasi=['Q1'], k=0))
        self.assertRaises(ValueError, lambda: df.k_anonymize(quasi=['Q1'], k=-100))

    def test_many_quasi(self):
        # 100 quasi identifiers
        df = create_random_df(50, 100)
        quasi_ids = list(range(0, 100))

        for k in range(1, 51, 5):
            anon_df = df.k_anonymize(quasi=quasi_ids, k=k)
            self.assertGreaterEqual(anon_df.k_anonymity(quasi=quasi_ids), k)

        # 1000 quasi identifiers
        df = create_random_df(50, 1000)
        quasi_ids = list(range(0, 1000))

        for k in range(1, 51, 5):
            anon_df = df.k_anonymize(quasi=quasi_ids, k=k)
            self.assertGreaterEqual(anon_df.k_anonymity(quasi=quasi_ids), k)


if __name__ == '__main__':
    unittest.main()