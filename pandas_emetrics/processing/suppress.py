import pandas as pd

# register function as pandas dataframe accessor
@pd.api.extensions.register_dataframe_accessor("suppress")
class SuppressAccessor:

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, columns: list[str], suppressor: str, inplace: bool=False) -> None | pd.DataFrame:
        """
        Replaces columns in the DataFrame with the given suppressor.
        
        Parameters
        ----------
        columns: list[str]
            List of DataFrame's columns to suppress.
            Example: columns=['Name', 'ID']

        supressor: str
            A string used to replaces the column's entries
            Example: supressor='*'

        inplace: bool
            Determines whether or not to override current DataFrame values.
            Defaults to False.
            Example: inplace=True

        Returns
        -------
        None | pd.DataFrame
            Returns None if 'inplace=True'. Otherwise, returns DataFrame with suppressed columns.
        """

        # prevents future assignment errors
        if not isinstance(suppressor, str):
            raise ValueError("Suppressor must be a string.")

        if inplace:
            # replaces all values in given columns with the suppressor
            for column in columns:
                self._obj[column] = suppressor
            return None
        else:
            # create copy of dataframe
            df = self._obj.copy(deep=True)
            for column in columns:
                df[column] = suppressor
            return df