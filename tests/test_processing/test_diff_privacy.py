from pandas_emetrics.processing import diff_privacy
import pandas as pd
import unittest
import os

class TestDiffPrivacy(unittest.TestCase):

    def test_bad_args(self):
        df = pd.DataFrame({'Test': [0, 1, 2, 3, 4]})

        self.assertRaises(ValueError, lambda: df.diff_privacy(columns=['Test'], sensitivity='WRONG'))
        self.assertRaises(ValueError, lambda: df.diff_privacy(columns=['Test'], type='WRONG'))

    def test_summary_stats_before_after(self):
        scholarships = pd.read_csv('./tests/test_processing/scholarship.csv')  

        



if __name__ == '__main__':
    unittest.main()