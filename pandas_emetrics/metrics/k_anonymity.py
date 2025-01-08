import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def k_anonymity(df: pd.DataFrame, quasi: list[str]) -> int:
    """
    Returns k-anonymity value of the DataFrame. 

    Parameters
    ----------
    quasi: list[str]
        List of DataFrame's quasi identifiers
        Example: quasi=['Age', 'Height', 'Weight']
        
    Returns
    -------
    int
        The calculated k value
    """

    # converts dataframe to tuples for optimized vector row operation
    samples = df[quasi].apply(tuple, axis=1)

    # count number of unique samples
    equivalence_classes_counts = samples.value_counts()
    
    # return k, which is the length of the equivalence class with the min. unique samples
    return equivalence_classes_counts.min()