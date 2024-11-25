import pandas as pd
from typing import TYPE_CHECKING

# Registering the function as a pandas accessor
@pd.api.extensions.register_dataframe_accessor("k_anonymity")
class KAnonymityAccessor:
    def __init__(self, pandas_obj):
        self.df = pandas_obj

    def __call__(self, quasi: pd.DataFrame) -> int:
        """
        Calculates k-anonymity value of the DataFrame

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
    
if TYPE_CHECKING:
    class DataFrame(pd.DataFrame):
        k_anonymity: KAnonymityAccessor





### TESTING ###
def main():
    data = {'Name': ['A', 'B', 'C', 'D', 'E', 'F'],
            'Age': [21, 21, 24, 27, 27, 24],
            'Weight': [140, 140, 240, 270, 270, 240]}

    # Create DataFrame
    df = pd.DataFrame(data)

    # print(df.k_anonymity(quasi=df[['Age', 'Weight']]))

main()


