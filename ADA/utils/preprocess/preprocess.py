import pandas as pd
from . import nulls_processing, column_categorization, data_transformation
"""
Test
"""
# import data_transformation
# import column_categorization

def preprocess_data(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    Preprocess the DataFrame by checking for null values, categorizing columns, and transforming data.

    :param df: pd.DataFrame - The DataFrame to preprocess.
    :param target: str - The name of the target column for ordinal checks.
    :return: pd.DataFrame - The preprocessed DataFrame.
    """
    # Check for null values and handle them
    df = nulls_processing.nulls_processing(df)

    # Categorize columns into numeric, categorical, and object types
    column_categorization.categorize_columns(df, target)

    # Transform the DataFrame based on the categorized columns
    data_transformation.transform_data(df)


if __name__ == "__main__":
    print("Preprocessing module loaded successfully.")
