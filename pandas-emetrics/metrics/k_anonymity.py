import pandas as pd

# register function as pandas dataframe accessor
@pd.api.extensions.register_dataframe_accessor("k_anonymity")
class KAnonymityAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, quasi: list[str]) -> int:
        """
        Returns k-anonymity value of the DataFrame

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
        samples = self._obj[quasi].apply(tuple, axis=1)

        # count number of unique samples
        equivalence_classes_counts = samples.value_counts()

        # return k-value, which is the equivalence class with the minimum unique samples
        return equivalence_classes_counts.min()

