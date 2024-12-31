from pandas_emetrics.metrics import l_diversity
import pandas as pd
import unittest

def create_df() -> pd.DataFrame:
    """
    Creates a sample DataFrame to be used for testing
    """
    return pd.DataFrame({'Age': [24] * 6 + [32] * 6,
                         'Weight': [140] * 6 + [180] * 6, # k = 2
                         'Sen1': list(range(6)) + list(range(6)), # l = 6
                         'Sen2': list(range(5)) + [4] + list(range(5)) + [4], # l = 5
                         'Sen3': list(range(3)) * 2 + list(range(3)) * 2}) # l = 3


class TestLDiversity(unittest.TestCase):

    def test_simple(self):
        # k = 2; l = 6
        df = create_df()
        
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen1']), 6)
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen2']), 5)
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen3']), 3)


    def test_mulitple_quasi(self):
        df = create_df()

        self.assertEqual(df.l_diversity(quasi=['Age', 'Weight'], sensitive=['Sen1']), 6)
        self.assertEqual(df.l_diversity(quasi=['Age', 'Weight'], sensitive=['Sen2']), 5)
        self.assertEqual(df.l_diversity(quasi=['Age', 'Weight'], sensitive=['Sen3']), 3)


    def test_multiple_sens(self):
        df = create_df()
        
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen1', 'Sen2']), 5)    
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen1', 'Sen2', 'Sen3']), 3)


    def test_multiple_both(self):
        df = create_df()
        
        self.assertEqual(df.l_diversity(quasi=['Age', 'Weight'], sensitive=['Sen1', 'Sen2']), 5)
        self.assertEqual(df.l_diversity(quasi=['Age', 'Weight'], sensitive=['Sen1', 'Sen2', 'Sen3']), 3)


if __name__ == '__main__':
    unittest.main()