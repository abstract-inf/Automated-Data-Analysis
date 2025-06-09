import utils
import visualize
import preprocess
import pandas as pd
class ADA:
    def __init__(self, data, target_column:str):
        """
        Hello
        :param data: pd.DataFrame - The input data to be processed.
        :param target_column: str - The name of the target column for classification or regression tasks.
        """
        self.data = data
        self.target_column = target_column


    def preprocess(self, data: pd.DataFrame) -> None:
        """
        does preprocessing on the data.
        """
        raise NotImplementedError("This function is not yet implemented.")

    def visualize(self):
        # Implement visualization logic here
        raise NotImplementedError("This function is not yet implemented.")

    def save_to_pdf(self):
        # Implement PDF saving logic here
        # بخ
        raise NotImplementedError("This function is not yet implemented.")