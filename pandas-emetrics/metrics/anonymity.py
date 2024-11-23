import pandas as pd

def k_anonymity(quasi: pd.DataFrame) -> int:
    """Calculates k-anonymity value of the DataFrame

    Parameters
    ------------
    quasi: pd.DataFrame
        List of DataFrame's quasi identifiers
        Exampele: df[['col1', 'col2', 'col3']]
    
    Returns
    -------
    int
        The calculated k value
    """

    # converts dataframe to tuples for optimized vector row operation
    samples = quasi.apply(tuple, axis=1)

    # count number of unique samples
    equivalence_classes = samples.value_counts()

    # return k-value, which is the equivalence class with the minimum unique samples
    return equivalence_classes.min()



    


