import pandas as pd
import numpy as np

@pd.api.extensions.register_dataframe_accessor("k_anonymize")
class KAnonymizeAccessor:
     
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

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

            if KAnonymizeAccessor.is_number(partition[id].dtype):
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
            return pd.concat([KAnonymizeAccessor.anonymize(lhs, quasi, frequency_set, k), 
                             KAnonymizeAccessor.anonymize(rhs, quasi, frequency_set, k)])

        # return partitioned grouping to be generalized
        return KAnonymizeAccessor.summarize(partition, quasi)

    def __call__(self, quasi: list[str], k: int, inplace: bool=False) -> None | pd.DataFrame:
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

        samples = self._obj.shape[0]

        if k > samples:
            raise ValueError(f"K={k}. K must be less than or equal to the number of samples (n={samples}) in the DataFrame.")
        elif k < 1:
            raise ValueError(f"K={k}. K must be greater than or equal to 1.")

        # get value counts for each quasi identifier
        frequency_set = {}
        for id in quasi:
            frequency_set[id] = self._obj[id].nunique()

        # sort by value descending
        frequency_set = sorted(frequency_set.items(), key=lambda x: x[1], reverse=True)

        anonymized_df = KAnonymizeAccessor.anonymize(self._obj, quasi, frequency_set, k).sort_index()

        if inplace:
            # reassign dtypes to prevent warnings
            for col in anonymized_df.columns:
                self._obj[col] = self._obj[col].astype(anonymized_df[col].dtype)
            self._obj[:] = anonymized_df
            return None
        else:
            return anonymized_df