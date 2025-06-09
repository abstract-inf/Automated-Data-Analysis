# preprocess.py
import pandas as pd
from utils import *

"""
- Nulls, data info: Suhaib
- data categorization: Ashqar
- datetime: Yazan
- feature selection: Ashqar
"""
class Preprocess:
    def __init__(self, data: pd.DataFrame):
        """
        :param data: pd.DataFrame - The input data to be processed.
        Initializes the Preprocess object with a DataFrame.
        """
        self.data = data

    def check_nulls(self) -> dict:
        """
        Checks for null values in the DataFrame.
        """
        pass

    def process_nulls(self, strategy: str = "drop") -> pd.DataFrame:
        """
        Processes null values (drops or fills by avg/mean).
        'strategy' can be 'drop' or 'fill'.
        """
        pass

    def print_data_info(self) -> None:
        """
        Prints a concise summary of the DataFrame (like df.info()).
        """
        pass

    def print_data_describe(self) -> pd.DataFrame:
        """
        Generates descriptive statistics of the DataFrame (like df.describe()).
        """
        pass

    def categorize_columns(self, data: pd.DataFrame) -> dict:
        """
        Identifies and categorizes columns as categorical (words/repeated values)
        or numerical (numbers repeated within a threshold/words that consist of numbers).
        Returns a dictionary with column names and their inferred types.
        """
        pass

    def handle_datetime(self) -> pd.DataFrame:
        """
        Handles datetime columns:
        - Combines if values are in a specific format across columns.
        - Extracts year, month, day, hour into separate columns.
        - Extracts features like is_weekend, rush_hours.
        """
        pass

    def feature_selection(self, method: str = "correlation") -> list:
        """
        Performs feature selection based on a specified method.
        Returns a list of selected features.
        """
        pass