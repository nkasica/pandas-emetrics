from pandas_emetrics.metrics import k_anonymity
import pandas as pd
import unittest
import time

def create_df(k: int, cols: int) -> pd.DataFrame:
    """
    Creates a DataFrame that is 'k' anonymous with 'cols' number of columns
    """

    data = []
    num = 1
    rows = k**2

    for i in range(rows):
        if i % k == 0 and i >= k:
            num += 1
        row_to_add = [num] * cols
        data.append(row_to_add)

    return pd.DataFrame(data)

class TestKAnonymity(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()
        
    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    #################### PERFORMACE TESTING ####################
    def test_small(self):
        # 25 rows, 100 columns
        df = create_df(5, 100)
        quasi_ids = list(range(0, 100))
        self.assertEqual(df.k_anonymity(quasi=quasi_ids), 5)

    def test_medium(self):
        # 10000 rows, 500 columns
        df = create_df(100, 500)
        quasi_ids = list(range(0, 500))
        self.assertEqual(df.k_anonymity(quasi=quasi_ids), 100)

    # does not run -> exit code 137 execution time past 3 minutes
    # def test_large(self):
    #     # 1 million rows, 5000 columns
    #     df = create_df(1000, 5000)
    #     quasi_ids = list(range(0, 5000))
    #     self.assertEqual(df.k_anonymity(quasi=quasi_ids), 1000)
    #################### PERFORMACE TESTING ####################

if __name__ == '__main__':
    unittest.main()