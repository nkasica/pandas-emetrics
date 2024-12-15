import pandas as pd

# register function as pandas dataframe accessor
@pd.api.extensions.register_dataframe_accessor("suppress")
class SuppressAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, columns: list[str], suppressor: str, inplace: bool=False) -> pd.DataFrame:
        """
        Returns an updated DataFrame with entries in the given columns suppressed
        
        Parameters
        ----------
        columns: list[str]
            List of DataFrame's columns to suppress
            Example: columns=['Name', 'ID']

        supressor: str
            A string or symbol used to replaces the column's entries
            Example: supressor='*'

        inplace: bool
            Optional parameter. If True, does not modify the dataframe and returns a copy instead
            Example: inplace=True

        Returns
        -------
        pd.DataFrame
            DataFrame with suppressed columns
        """

        # in-place modification
        if inplace:
            # replaces all values in given columns with the supressor
            for column in columns:
                self._obj[column] = suppressor

            return self._obj

        else:
            # create copy of dataframe
            df = self._obj.copy(deep=True)

            for column in columns:
                df[column] = suppressor

            return df
