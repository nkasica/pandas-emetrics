import pandas as pd
import numpy as np
from typing import Literal

@pd.api.extensions.register_dataframe_accessor("add_noise")
class AddNoiseAccessor:

    _TRANSFORMATIONS = Literal['laplace', 'gaussian']
    _SENSITIVITIES = Literal['count']

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, columns: list[str], epsilon: float=0.5, sensitivity: _SENSITIVITIES='count',
                   type: _TRANSFORMATIONS='laplace') -> pd.DataFrame:
        """
        """

        # number of samples
        n = self._obj.shape[0]

        if sensitivity == 'count':
            b = 1 / epsilon

        for column in columns:
            noise = np.random.laplace(0, b, n)
            self._obj[column] += noise

        return self._obj
            
        

        

