from pandas_emetrics.processing import diff_privacy
import pandas as pd
import unittest

class TestDiffPrivacy(unittest.TestCase):

    def test_bad_args(self):
        df = pd.DataFrame({'Test': [0, 1, 2, 3, 4]})

        self.assertRaises(ValueError, lambda: df.diff_privacy(columns=['Test'], sensitivity='WRONG'))
        self.assertRaises(ValueError, lambda: df.diff_privacy(columns=['Test'], noise='WRONG'))

    def test_summary_stats_before_after(self):
        scholarships = pd.read_csv('./tests/test_processing/scholarship.csv')

        # only focus on the sensitive attribute
        summary_stats_before = scholarships['Scholarship Dollars'].describe()

        # apply differential privacy on each query
        queries = ['count', 'mean', 'sum', 'median']
        for q in queries:
            # apply dp
            new_df = scholarships.diff_privacy(columns=['Scholarship Dollars'], sensitivity=q)
            # get summary stats
            summary_stats_after = new_df['Scholarship Dollars'].describe()

            self.assertAlmostEqual(summary_stats_before['mean'], summary_stats_after['mean'], delta=1000)
            self.assertAlmostEqual(summary_stats_before['std'], summary_stats_after['std'], delta=250)

    def test_inplace(self):
        # create original test DataFrame and retain original values
        df = pd.DataFrame({'Weight': [225, 140, 150, 300, 409, 240, 180, 195]})
        orig_df = df.copy(deep=True)

        # apply differential privacy inplace
        df.diff_privacy(columns=['Weight'], inplace=True)

        self.assertFalse(df.equals(orig_df))

    def test_not_inplace(self):
        # create original test DataFrame and retain original values
        df = pd.DataFrame({'Weight': [225, 140, 150, 300, 409, 240, 180, 195]})
        orig_df = df.copy(deep=True)

        # apply differential privacy not inplace
        new_df = df.diff_privacy(columns=['Weight'], inplace=False)

        self.assertTrue(df.equals(orig_df))
        self.assertFalse(df.equals(new_df))

    
if __name__ == '__main__':
    unittest.main()