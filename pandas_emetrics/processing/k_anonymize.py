import pandas as pd

# register function as pandas dataframe accessor
@pd.api.extensions.register_dataframe_accessor("k_anonymize")
class KAnonymizeAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, quasi: list[str], k: int) -> pd.DataFrame:
        """
        Returns DataFrame, if possible, after being k-anonymized with the given k value.

        Parameters
        ----------
        quasi: list[str]
            List of DataFrame's quasi identifiers
            Example: quasi=['Age', 'Height', 'Weight']
        k: int
            The k-value for anonymization
            Example: k=3   

        Returns
        -------
        pd.DataFrame
            K-Anonymized DataFrame, if possible
        """ 

        
