import pandas as pd
import numpy as np
from typing import Literal

@pd.api.extensions.register_dataframe_accessor("add_noise")
class AddNoiseAccessor:

    _TRANSFORMATIONS = Literal['laplace', 'gaussian']
    _SENSITIVITIES = Literal['count', 'mean']

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def calc_sens_mean(column: pd.Series):
        """
        Calculates local sensitivity for differential privacy when using the mean as a query
        """

        # sample size
        n = len(column)

        if n <= 1:
            return 0
    
        # convert to nparray
        d = column.to_numpy()

        davg = np.average(d)
        dsum = np.sum(d)

        # finds max(|avg(all samples) - avg(all samples - curr sample)|) for each sample
        # average(dprime) = (sum(d) - d[i]) / (n - 1)
        # sensitivity[i] = |davg - average(dprime)|
        sensitivities = np.abs(davg - (dsum - d) / n - 1)

        return np.max(sensitivities)

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

        if sensitivity == 'count':
            mean = False
            b = 1 / epsilon
        elif sensitivity == 'mean':
            mean = True

        
        for column in columns:
            noise = np.random.laplace(0, AddNoiseAccessor.calc_sens_mean(column) if mean else b, n)
            self._obj[column] += noise

        return self._obj