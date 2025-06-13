from utils.preprocess import preprocess
from utils.visualize import master
from utils.modeling import modeling
import pandas as pd

class ADA:
    def __init__(self, data, target, k_features=1000, problem_type='classification'):
        """
        Initializes the ADA class with the provided data and target column.
        :param data: pd.DataFrame - The input data to be analyzed.
        :param target: str - The name of the target column for analysis.
        """

        self.data = data
        self.target_column =target
        self.problem_type = problem_type
        self.k_features = k_features

    def preprocess(self, **kwargs):
        # Implement preprocessing logic here
        preprocess.preprocess_data(self.data, self.target_column)
        modeling.model_data(self.data, self.target_column, self.k_features,self.problem_type)

    def visualize(self):
        # Implement visualization logic here
        master.visualize_data(self.data, target_col=self.target_column)
        raise NotImplementedError("This function is not yet implemented.")

    def save_to_pdf(self):
        # Implement PDF saving logic here
        # بخ
        raise NotImplementedError("This function is not yet implemented.")
    
if __name__ == "__main__":
    # Example usage

    target_column = 'target'  # Specify your target column name
    ada = ADA(data=None, target=target_column, k_features=1000, problem_type='classification')

    ada.preprocess()
    ada.visualize()
    ada.save_to_pdf()