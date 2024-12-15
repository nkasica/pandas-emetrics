from pandas_emetrics.processing import suppress
import pandas as pd
import unittest

# create simple DataFrames for testing
def create_sample_df():
        df = pd.DataFrame({'ID': [0, 1, 2, 3, 4, 5], 
                           'Weight': [140, 145, 180, 110, 220, 185]})
        correct_df = pd.DataFrame({'ID': ['*', '*', '*', '*', '*', '*'], 
                                   'Weight': [140, 145, 180, 110, 220, 185]})
        
        return df, correct_df

class TestSupress(unittest.TestCase):

    def test_inplace(self):
        df, correct_df = create_sample_df()

        # supress inplace
        new_df = df.suppress(columns=['ID'], suppressor='*', inplace=True)

        self.assertTrue(df.equals(correct_df))
        self.assertTrue(df.equals(new_df))

    def test_not_inplace(self):
         df, correct_df = create_sample_df()

         # supress not inplace
         new_df = df.suppress(columns=['ID'], suppressor='*', inplace=False)

         self.assertTrue(new_df.equals(correct_df))
         self.assertFalse(df.equals(new_df))



if __name__ == '__main__':
    unittest.main()
        
