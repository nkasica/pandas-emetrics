import pandas as pd

@pd.api.extensions.register_dataframe_accessor("l_diversity")
class LDiversityAccessor:

    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, quasi: list[str], sensitive: list[str]) -> int:
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
        equivalence_classes = self._obj.groupby(quasi)

        # l-value will never be > num of samples
        min_l = len(self._obj)

        for _, group in equivalence_classes:
            for attr in sensitive:
                # num of unique equivalence class combinations 
                l_eq = group[attr].drop_duplicates().shape[0]
                min_l = min(l_eq, min_l)

        return min_l