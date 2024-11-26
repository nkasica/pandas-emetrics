import pandas as pd

@pd.api.extensions.register_dataframe_accessor("l_diversity")
class KAnonymityAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, quasi: list[str], sensitive: list[str]) -> int:
        """
        Returns l-diversity value of the dataset

        Parameters
        ----------
        quasi: list[str]
            List of DataFrame's quasi identifiers
            Example: quasi=['Age', 'Height', 'Weight']
        sensitive
            List of DataFrame's sensitive attribute(s)
            Example: sensitive=['Salary']

        Returns
        -------
        int 
            The calculated l value
        """
        
        # get equivalence classes
        equivalence_classes = self._obj.groupby(quasi)

        # define list to hold unique sensitive attribute counts
        unique_sens_vals = []

        # iterate through equivalence classes, summing up the number of unique sensitive values 
        for _, group in equivalence_classes:
            unique_sens_vals.append(group[sensitive].nunique().sum())

        # return l-value, which is the minimum number of unique sensitive attributes in all equivalence classes
        return min(unique_sens_vals)