import pandas as pd
import numpy as np
from typing import Literal

@pd.api.extensions.register_dataframe_accessor("add_noise")
class AddNoiseAccessor:

    _TRANSFORMATIONS = Literal['laplace', 'gaussian']
    _SENSITIVITIES = Literal['count', 'mean', 'sum']

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def calc_sens_mean(column: pd.Series, n: int):
        """
        Calculates sensitivity for differential privacy when using the mean as a query
        """
    
        # convert to nparray
        d = column.to_numpy()

        davg = np.average(d)
        dsum = np.sum(d)

        # finds max(|avg(all samples) - avg(all samples - curr sample)|) for each sample
        # average(dprime) = (sum(d) - d[i]) / (n - 1)
        # sensitivity[i] = |davg - average(dprime)|
        sensitivities = np.abs(davg - (dsum - d) / n - 1)

        return np.max(sensitivities)

    def calc_sens_sum(column: pd.Series):
        """
        Calculates sensitivity for differential privacy when using the sum as a query
        """

        d = column.to_numpy()

        dsum = np.sum(d)

        # finds max(|sum(all samples) - sum(all samples - curr samples)|) for each sample
        sensitivities = np.abs(dsum - d)

        return np.max(sensitivities)

    def calc_sens_median(column: pd.Series, n: int):
        """
        Calculates sensitivity for differential privacy when using the median as a query
        """

        d = column.to_numpy()
        d = np.sort(d)

        dmed = np.median(d)
        max_sens = -1

        # compares max(|median(all samples) - median(all samples - current sample)) 
        # for each sample with the current maximum sensitivity
        for i in range(n):
            dprime = np.concatenate(d[:i], d[i+1:]) # removes one element from the list at a time
            curr_sens = np.abs(dmed - np.median(dprime))
            max_sens = np.max(max_sens, curr_sens)
            
        return max_sens

    def __call__(self, columns: list[str], epsilon: float=0.5, sensitivity: _SENSITIVITIES='count',
                   type: _TRANSFORMATIONS='laplace') -> pd.DataFrame:
        """
        Adds noise to the specifed columns in a way that is in-line with differential privacy

        Parameters
        ----------
        columns: list[str]
            Numeric columns to add noise to
            Example: columns=['Salary']

        epsilon: float
            Quantifies the level of privacy protection. Smaller epsilon values yield increased 
                privacy at the risk of degenerated data utility. Defaults to 0.5
            Example: epsilon=0.01
        
        sensitivity: 'count' or 'mean'
            Indicated which type of query is being perfomed on the DataFrame. In differential privacy,
                sensitivity represents MAX(|f(D1) - f(D2)|). In our case, we are picking what function to 
                use for 'f' in that equation.
            Example: sensitivity='mean'

        type: 'laplace' or 'gaussian'
            Indicates the type of noise to be added. Defaults to 'laplace'
            Example: type='gaussian'

        Returns
        -------
        pd.DataFrame
            DataFrame with added noise
        """

        # number of samples
        n = self._obj.shape[0]

        # create sensitivity list for each column based on query
        if n <= 1:
            sens_vals = [0 * len(columns)]
        elif sensitivity == 'count':
            sens_vals = [(1 / epsilon) * len(columns)]
        elif sensitivity == 'mean':
            sens_vals = [AddNoiseAccessor.calc_sens_mean(column, n) / epsilon for column in columns]
        elif sensitivity == 'sum':
            sens_vals = [AddNoiseAccessor.calc_sens_sum(column) / epsilon for column in columns]
        else:
            sens_vals = [AddNoiseAccessor.calc_sens_median(column, n) / epsilon for column in columns]
  
        # add noise to each column
        for idx, column in enumerate(columns):
            noise = np.random.laplace(0, sens_vals[idx], n)
            self._obj[column] += noise

        return self._obj