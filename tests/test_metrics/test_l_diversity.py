from pandas_emetrics.metrics import l_diversity
import pandas as pd
import unittest

class TestLDiversity(unittest.TestCase):

    def test_simple(self):
        # k = 2; l = 6
        df = pd.DataFrame({'Age': [24] * 6 + [32] * 6,
                          'Sen': list(range(6)) + list(range(6))}) # l = 6
        
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen']), 6)

    def test_mulitple_quasi(self):
        # k = 2; l = 5
        df = pd.DataFrame({'Age': [24] * 6 + [32] * 6,
                          'Weight': [140] * 6 + [180] * 6,
                          'Sen': list(range(5)) + [4] + list(range(5)) + [4]}) # l = 5

        self.assertEqual(df.l_diversity(quasi=['Age', 'Weight'], sensitive=['Sen']), 5)

    def test_multiple_sens(self):
        df = pd.DataFrame({'Age': [24] * 6 + [32] * 6,
                           'Sen1': list(range(6)) + list(range(6)),
                           'Sen2': list(range(6)) + list(range(6))}) # l = 6
        
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen1', 'Sen2']), 6)

        df = pd.DataFrame({'Age': [24] * 6 + [32] * 6,
                           'Sen1': list(range(6)) + list(range(6)),
                           'Sen2': list(range(5)) + [4] + list(range(5)) + [4]}) # l = 5
        
        self.assertEqual(df.l_diversity(quasi=['Age'], sensitive=['Sen1', 'Sen2']), 5)



if __name__ == '__main__':
    unittest.main()