import pandas as pd
import pandas_flavor as pf
import numpy as np

def calc_sens_mean(column: pd.Series, n: int) -> np.number:
    """
    Calculates sensitivity when using the mean as a query
    """
    
    d = column.to_numpy()
    davg = np.average(d)
    dsum = np.sum(d)

    # finds max(|avg(all samples) - avg(all samples - curr sample)|) for each sample
    # mean(d') = (sum(d) - d[i]) / (n - 1)
    # sensitivity[i] = |davg - mean(d')|
    sensitivities = np.abs((davg - (dsum - d)) / (n - 1))

    return np.max(sensitivities)

def calc_sens_sum(column: pd.Series) -> np.number:
    """
    Calculates sensitivity when using the sum as a query
    """

    d = column.to_numpy()
    min_d = min(d)
    max_d = max(d)

    # min-max normalization so data points are between [0, 1]
    # this helps prevent unbounded values and outliers affecting added noise
    d = (d - min_d) / (max_d - min_d)

    # finds max(|sum(all samples) - sum(all samples - curr samples)|) for each sample
    return np.max(np.abs(d))

def calc_sens_median(column: pd.Series, n: int) -> np.number:
    """
    Calculates sensitivity when using the median as a query
    """

    d = column.to_numpy()
    d = np.sort(d)
    dmed = np.median(d)

    # temporary value; sensitivity will never be < 0
    max_sens = -1.0

    # compares max(|median(all samples) - median(all samples - current sample)|) 
    # for each sample with the current maximum sensitivity
    for i in range(n):
        dprime = np.concatenate((d[:i], d[i+1:])) # removes one element from the list at a time
        curr_sens = np.abs(dmed - np.median(dprime))
        max_sens = max(max_sens, curr_sens)
            
    return max_sens

@pf.register_dataframe_method
def diff_privacy(df, columns: list[str], epsilon: float=0.5, sensitivity: str='count', 
                 noise: str='laplace', inplace: bool=False) -> None | pd.DataFrame:
    """
    Adds noise to the specifed columns in a manner similar to differential privacy. 

    Parameters
    ----------
    columns: list[str]
        Columns to add noise to. Must be numeric.
        Example: columns=['Salary']

    epsilon: float
        Quantifies the level of privacy protection. Smaller epsilon values yield increased 
            privacy at the risk of degenerated data utility. Defaults to 0.5
        Example: epsilon=0.01
        
    sensitivity: 'count', 'mean', 'sum', or 'median'
        Indicates which type of query is being performed on the DataFrame. In differential privacy,
            sensitivity represents MAX(|f(D1) - f(D2)|), where D1 and D2 are databases that differ in 
            only  one element or row. In our case, we are picking what function for f().
        Example: sensitivity='mean'

    noise: 'laplace' or 'gaussian'
        Indicates the type of noise to be added. Defaults to 'laplace'
        Example: noise='gaussian'

    inplace: bool
        Specifies whether or not this action modifies the DataFrame in-place, overriding current values. 
        Defaults to False.
        Example: inplace=True

    Returns
    -------
    None | pd.DataFrame
        Returns None if 'inplace=True'. Otherwise, returns DataFrame with added noise.
    """

    ret_df = df if inplace else df.copy(deep=True)

    # assert type paramter is valid
    if (noise != 'laplace' and noise != 'gaussian'):
        raise ValueError('Incorrect type parameter. Please use "laplace" or "gaussian".')

    # number of samples
    n = ret_df.shape[0]

    # create sensitivity list for each column based on query
    if n <= 1:
        sens_vals = [0 * len(columns)]
    elif sensitivity == 'count':
        sens_vals = [(1 / epsilon) * len(columns)]
    elif sensitivity == 'mean':
        sens_vals = [calc_sens_mean(ret_df[column], n) / epsilon for column in columns]
    elif sensitivity == 'sum':
        sens_vals = [calc_sens_sum(ret_df[column]) / epsilon for column in columns]
    elif sensitivity == 'median':
        sens_vals = [calc_sens_median(ret_df[column], n) / epsilon for column in columns]
    else:
        raise ValueError('Incorrect sensitivity parameter. Please use "count", "mean", "sum", or "median".')
  
    # add noise to each column
    for idx, column in enumerate(columns):
        noise = np.random.laplace(0, sens_vals[idx], n) if type == 'laplace' else np.random.normal(0, sens_vals[idx], n)
        ret_df[column] += noise

    return None if inplace else ret_df