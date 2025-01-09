import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def suppress(df: pd.DataFrame, columns: list[str], suppressor: str, inplace: bool=False) -> None | pd.DataFrame:
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
            df[column] = suppressor
        return None
    else:
        # create copy of dataframe
        ret_df = df.copy(deep=True)
        for column in columns:
            ret_df[column] = suppressor
        return ret_df