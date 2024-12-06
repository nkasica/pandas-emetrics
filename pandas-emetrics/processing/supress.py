import pandas as pd

# register function as pandas dataframe accessor
@pd.api.extensions.register_dataframe_accessor("supress")
class SupressAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, columns: list[str], supressor: str) -> pd.DataFrame:
        """
        Returns an updated DataFrame with entries in the given columns supressed
        
        Parameters
        ----------
        columns: list[str]
            List of DataFrame's columns to supress
            Example: columns=['Name', 'ID']

        supressor: str
            A string or symbol used to replaces the column's entries
            Example: supressor='*'

        Returns
        -------
        pd.DataFrame
            DataFrame with supressed columns
        """

        # replaces all values in given columns with the supressor
        for column in columns:
            self._obj[column] = supressor

        return self._obj