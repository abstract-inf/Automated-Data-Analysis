from ADA.utils.preprocess import preprocess


import pandas as pd

class ADA:
    def __init__(self, data_path, target, k_features=1000, problem_type='classification'):
        """
        Initializes the ADA class with the provided data and target column.
        :param data: pd.DataFrame - The input data to be analyzed.
        :param target: str - The name of the target column for analysis.
        :param k_features: int - The number of features to select for modeling.
        :param problem_type: str - The type of problem ('classification' or 'regression').
        :raises ValueError: If the target column is not found in the data.
        :raises FileNotFoundError: If the data file does not exist at the specified path.
        :raises Exception: If the data cannot be read or processed.
        :return: None
        :description: This class is designed to handle data preprocessing, modeling, and visualization for a given dataset.
        :example: ada = ADA(data_path="path/to/data.csv", target="target_column", k_features=1000, problem_type='classification')
        :note: Ensure that the data file exists at the specified path and that the target column is present in the data.
        :note: The class uses utility functions from the 'utils' package for preprocessing and modeling.
        :note: The preprocess method handles data cleaning and transformation, while the visualize method generates visualizations.
        :note: The class is designed to be flexible for different datasets and target columns, making it suitable for various machine learning tasks.
        :note: The class is intended for use in a machine learning pipeline, where data preprocessing, modeling, and visualization are essential steps.
        :note: The class is part of the ADA package, which provides tools for data analysis and machine learning.
        :note: The class is designed to be extensible, allowing for future enhancements and additional features.
        :note: The class is intended for users familiar with Python and machine learning concepts, providing a structured approach to data analysis.
        :note: The class is designed to be used in a modular way, allowing users to integrate it into larger projects or workflows.
        :note: The class is built with the assumption that the input data is in CSV format, and it uses pandas for data manipulation.
        """

        self.data_path = data_path
        self.data = pd.read_csv(data_path)
        self.target_column =target
        self.problem_type = problem_type
        self.k_features = k_features

    def preprocess(self, **kwargs):
        # Implement preprocessing logic here
        preprocess.preprocess_data(self.data, self.target_column)

        from ADA.utils.modeling import modeling
        modeling.model_data(self.target_column, self.k_features,self.problem_type)

    def visualize(self):
        # Implement visualization logic here
        from ADA.utils.visualize import master
        master.visualize_data(self.data_path, target_col=self.target_column)


    
if __name__ == "__main__":
    # Example usage

    target_column = 'Survived'  # Specify your target column name
    ada = ADA(data_path = "ADA/datasets/titanic.csv", target=target_column, k_features=1000, problem_type='classification')

    ada.preprocess()
    ada.visualize()
