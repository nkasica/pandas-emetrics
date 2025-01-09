import pandas as pd
import pandas_flavor as pf
import numpy as np

def is_number(value) -> bool:
    """
    Returns true if value is any numeric dtype
    """

    return np.issubdtype(value, np.number)

def summarize(partition: pd.DataFrame, quasi: list[str]) -> pd.DataFrame:
    """
    Generalize each partition for each quasi identifier based on min-max range.
    """

    for id in quasi:
        partition = partition.sort_values(by=id)

        if is_number(partition[id].dtype):
            s = f'[{partition[id].iloc[0]}-{partition[id].iloc[-1]}]'
            partition[id] = [s] * partition[id].size
        else: # handles non numeric element types
            unique_lst = partition[id].unique()
            partition[id] = [unique_lst] * partition[id].size

    return partition

def anonymize(partition: pd.DataFrame, quasi: list[str], frequency_set: list[tuple], k: int) -> pd.DataFrame:
    """
    Recursively partitions the quasi identifiers
    """

    # sorts DataFrame the quasi identifier with the most unique values
    qi = frequency_set[0][0]
    partition = partition.sort_values(by=qi)

    # find median idx to split on
    splitVal = partition[qi].count() // 2
    lhs = partition[splitVal:]
    rhs = partition[:splitVal]

    # recursively anonymize
    if (len(lhs) >= k and len(rhs) >= k):
        return pd.concat([anonymize(lhs, quasi, frequency_set, k), 
                            anonymize(rhs, quasi, frequency_set, k)])

    # return partitioned grouping to be generalized
    return summarize(partition, quasi)

@pf.register_dataframe_method
def k_anonymize(df, quasi: list[str], k: int, inplace: bool=False) -> None | pd.DataFrame:
    """
    Applies the multivariate mondrian algorithim to k-anonymize the DataFrame. This 
    partitioning is relaxed, meaning equivalence classes can have overlapping bounds. Works for 
    both numeric and categorical data.

    Parameters
    ----------
    quasi: list[str]
        List of DataFrame's quasi identifiers to be anonymized.
        Example: quasi=['Age', 'Height', 'Weight']

    k: int
        Level of anonymity. Represents the minimum number of samples in each equivalence class.
        Example: k=3

    inplace: bool
        Specifies whether or not this action modifies the DataFrame in-place, overriding current values.
        Defaults to False.
        Example: inplace=True

    Returns
    -------
    None | pd.DataFrame
        Returns None if 'inplace=True'. Otherwise, returns k-anonymized DataFrame.
    """ 

    samples = df.shape[0]

    if k > samples:
        raise ValueError(f"K={k}. K must be less than or equal to the number of samples (n={samples}) in the DataFrame.")
    elif k < 1:
        raise ValueError(f"K={k}. K must be greater than or equal to 1.")

    # get value counts for each quasi identifier
    frequency_set = {}
    for id in quasi:
        frequency_set[id] = df[id].nunique()

    # sort by value descending
    frequency_set = sorted(frequency_set.items(), key=lambda x: x[1], reverse=True)

    anonymized_df = anonymize(df, quasi, frequency_set, k).sort_index()

    if inplace:
        # reassign dtypes to prevent warnings
        for col in anonymized_df.columns:
            df[col] = df[col].astype(anonymized_df[col].dtype)
        df[:] = anonymized_df
        return None
    else:
        return anonymized_df