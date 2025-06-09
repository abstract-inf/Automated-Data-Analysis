import datetime
import glob

import pandas as pd
import warnings
import numpy as np

def find_datetime_columns(df: pd.DataFrame) -> list[str]:
    """
    Checks all columns in the DataFrame to identify those that are either already
    datetime types or can be reliably converted to datetime objects.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        list[str]: A list of column names identified as datetime columns.
    """
    datetime_columns = []
    for col in df.columns:
        # Step 1: First, check if the column is already a datetime dtype
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_columns.append(col)
            continue # Move to the next column, no further conversion needed

        # Step 2: If not, and it's an object (string) dtype, try converting it.
        if pd.api.types.is_object_dtype(df[col]):
            # Use warnings.catch_warnings to suppress the specific UserWarning
            # that occurs when 'format' cannot be inferred and dateutil is used for parsing.
            with warnings.catch_warnings():
                # Ignore the UserWarning specifically about format inference falling back to dateutil.
                warnings.simplefilter("ignore", UserWarning)

                # Attempt to convert the column to datetime.
                converted_series = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)

                # Step 3: Validate successful conversion.
                conversion_success_threshold = 0.8 # Define a threshold, e.g., 80% non-NaT values
                if pd.api.types.is_datetime64_any_dtype(converted_series) and \
                   converted_series.count() > 0 and \
                   (converted_series.count() / len(converted_series)) > conversion_success_threshold:
                    datetime_columns.append(col)

    return datetime_columns

def find_date_columns(df: pd.DataFrame):
    """
    Identifies day, month, and year columns in the DataFrame.
    and returns them as separate Series.
    Args:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        tuple: A tuple containing three Series: day, month, and year.
        If a column is not found, its corresponding Series will be None.
    """
    day = None
    month = None
    year = None
    for column in df.columns:
        if "day" in column.lower():
            df[column] = pd.to_datetime(df[column], dayfirst=True, errors='coerce')  # Ensure day is parsed correctly
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                day = df[column]
        elif "month" in column.lower():
            df[column] = pd.to_datetime(df[column], format='%m', errors='coerce')  # Ensure month is parsed correctly
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                month = df[column]
        elif "year" in column.lower():
            df[column] = pd.to_datetime(df[column], format='%Y', errors='coerce')  # Ensure year is parsed correctly
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                year = df[column]
        else:
            continue

    return day, month, year
       
    
if __name__ == "__main__":
    # List of specific dataset names to process.
    datasets_names = ["Chocolate Sales.csv", "coffe.csv", "diabetes.csv", "titanic.csv", "video-games-2022.csv"]

    for file_name in datasets_names:
        print("="*50)
        print(f"Processing file: {file_name}")
        file_path = f"ADA/datasets/{file_name}"
        
        df = pd.read_csv(file_path)
        
        # Find datetime columns in the DataFrame
        # columns = find_datetime_columns(df)
        # if columns:
        #     print(f"Identified datetime columns in {file_name}: {columns}")
        # else:
        #     print(f"No datetime columns found in {file_name}.")

        # Find and merge date columns if they exist
        print(find_date_columns(df)) 
        