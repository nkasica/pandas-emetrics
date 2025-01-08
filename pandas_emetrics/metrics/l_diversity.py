import pandas as pd
import pandas_flavor as pf

@pf.register_dataframe_method
def l_diversity(df, quasi: list[str], sensitive: list[str]) -> int:
    """
    Returns l-diversity value of the DataFrame.

    Parameters
    ----------
    quasi: list[str]
        List of DataFrame's quasi identifiers
        Example: quasi=['Age', 'Height', 'Weight']

    sensitive: list[str]
        List of DataFrame's sensitive attribute(s)
        Example: sensitive=['Salary']

    Returns
    -------
    int 
        The l-value of the DataFrame.
    """
        
    # get equivalence classes
    equivalence_classes = df.groupby(quasi)

    # l-value will never be > num of samples
    min_l = len(df)

    for _, group in equivalence_classes:
        for attr in sensitive:
            # num of unique equivalence class combinations 
            l_eq = group[attr].drop_duplicates().shape[0]
            min_l = min(l_eq, min_l)

    return min_l