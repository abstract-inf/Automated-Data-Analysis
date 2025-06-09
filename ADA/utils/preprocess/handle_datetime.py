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
       
def merge_date_columns(df: pd.DataFrame, day: pd.Series, month: pd.Series, year: pd.Series) -> pd.DataFrame:
    """
    Merges day, month, and year columns into a single datetime column in the DataFrame.
    Args:
        df (pd.DataFrame): The input DataFrame.
        day (pd.Series): Series containing day values.
        month (pd.Series): Series containing month values.
        year (pd.Series): Series containing year values.
    Returns:
        pd.DataFrame: The DataFrame with a new 'date' column.
    """
    if day is not None and month is not None and year is not None:
        # Create a new datetime column by combining day, month, and year
        df['date'] = pd.to_datetime(
            dict(year=year.dt.year, month=month.dt.month, day=day.dt.day),
            errors='coerce'
        )
    # else:
        # raise "Not all date components are available to merge."
    
    return df

def is_weekend(days_series: pd.Series, weekend_days: str = "sat_sun") -> pd.Series:
    """
    Checks if each day in a Pandas Series is a weekend.

    Args:
        days_series (pd.Series): A Pandas Series containing day information.
                                 This can be datetime objects, strings representing dates
                                 (e.g., "2023-10-27", "Oct 27, 2023", "Friday", etc.),
                                 or integers that can be parsed as dates (e.g., day of month
                                 if a full date context is available during parsing).
        weekend_days (str): Specifies which days constitute the weekend.
                            Options:
                            - "sat_sun": Saturday (5) and Sunday (6) are weekends. (default)
                            - "fri_sat": Friday (4) and Saturday (5) are weekends.

    Returns:
        pd.Series: A boolean Series indicating whether each day is a weekend (True) or not (False).
                   Returns a series of False if the input series cannot be converted to datetime.
    """

    # Define the mapping for weekend days to their dayofweek integers
    # Monday=0, Tuesday=1, ..., Friday=4, Saturday=5, Sunday=6
    weekend_map = {
        "sat_sun": [5, 6],  # Saturday and Sunday
        "fri_sat": [4, 5]   # Friday and Saturday
    }

    if weekend_days not in weekend_map:
        raise ValueError(f"Invalid 'weekend_days' option. Choose from {list(weekend_map.keys())}")

    try:
        # Convert the input series to datetime objects.
        # errors='coerce' will turn unparseable dates into NaT (Not a Time)
        # We explicitly set `dayfirst=False` and `yearfirst=False` to handle
        # common date formats and let pandas infer.
        # For strings like 'October 27, 2023', `pd.to_datetime` is usually quite robust.
        datetime_series = pd.to_datetime(
            days_series,
            errors='coerce',
            dayfirst=False,
            yearfirst=False
        )
    except Exception as e:
        # This catch block is mostly for unexpected internal Pandas errors,
        # as `errors='coerce'` handles parsing failures gracefully.
        print(f"Warning: Unexpected error during datetime conversion: {e}")
        print("Returning a Series of False as a fallback.")
        return pd.Series([False] * len(days_series), index=days_series.index)

    # Get the integer representation of the day of the week (Monday=0, Sunday=6)
    day_of_week = datetime_series.dt.dayofweek

    # Get the selected weekend days
    selected_weekend_integers = weekend_map[weekend_days]

    # Check if each day's dayofweek is in the selected weekend integers
    is_weekend_series = day_of_week.isin(selected_weekend_integers)

    # Handle NaT values: they are not a weekend
    # NaT values result in False for is_weekend_series after `isin` (which propagates NaN),
    # but explicitly filling ensures consistency and handles cases where `isin` might not propagate NaN.
    is_weekend_series = is_weekend_series.fillna(False)

    return is_weekend_series


if __name__ == "__main__":
    # List of specific dataset names to process.
    # datasets_names = ["Chocolate Sales.csv", "coffe.csv", "diabetes.csv", "titanic.csv", "video-games-2022.csv"]

    # for file_name in datasets_names:
    #     print("="*50)
    #     print(f"Processing file: {file_name}")
    #     file_path = f"ADA/datasets/{file_name}"
        
    #     df = pd.read_csv(file_path)
        
        # Find datetime columns in the DataFrame
        # columns = find_datetime_columns(df)
        # if columns:
        #     print(f"Identified datetime columns in {file_name}: {columns}")
        # else:
        #     print(f"No datetime columns found in {file_name}.")

        # Find date columns if they exist
        # day, month, year = find_date_columns(df)    

    print("\n--- Running Examples for is_weekend function ---")

    # Helper function to print detailed debug info
    def print_debug_info(original_series, datetime_series, day_of_week_series):
        print("\n--- Debug Info ---")
        debug_df = pd.DataFrame({
            'Original': original_series,
            'Parsed Datetime': datetime_series,
            'Day of Week (0=Mon, 6=Sun)': day_of_week_series
        })
        print(debug_df.to_string())
        print("------------------")

    # Example 1: Series with full dates
    dates1 = pd.Series([
        "2025-06-06",  # Friday
        "2025-06-07",  # Saturday
        "2025-06-08",  # Sunday
        "2025-06-09",  # Monday
        "October 27, 2023", # Friday
        "1/1/2024", # Monday
    ])
    print("\n--- Example 1: Full Dates (Sat/Sun weekend) ---")
    print("Original Series:\n", dates1)
    # Debug prints for Example 1
    datetime_series_1_sat_sun = pd.to_datetime(dates1, errors='coerce', dayfirst=False, yearfirst=False)
    day_of_week_1_sat_sun = datetime_series_1_sat_sun.dt.dayofweek
    print_debug_info(dates1, datetime_series_1_sat_sun, day_of_week_1_sat_sun)
    print("Is weekend (Sat/Sun):\n", is_weekend(dates1, weekend_days="sat_sun"))

    print("\n--- Example 1: Full Dates (Fri/Sat weekend) ---")
    print("Original Series:\n", dates1)
    # Debug prints for Example 1 (re-parsing for clarity, though it's the same series)
    datetime_series_1_fri_sat = pd.to_datetime(dates1, errors='coerce', dayfirst=False, yearfirst=False)
    day_of_week_1_fri_sat = datetime_series_1_fri_sat.dt.dayofweek
    print_debug_info(dates1, datetime_series_1_fri_sat, day_of_week_1_fri_sat)
    print("Is weekend (Fri/Sat):\n", is_weekend(dates1, weekend_days="fri_sat"))

    # Example 2: Series with named days
    dates2 = pd.Series([
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ])
    print("\n--- Example 2: Named Days (Sat/Sun weekend) ---")
    print("Original Series:\n", dates2)
    # Debug prints for Example 2
    # Note: pd.to_datetime for standalone day names will infer a date based on the current system date.
    # Results for these will depend on when you run the script.
    datetime_series_2 = pd.to_datetime(dates2, errors='coerce', dayfirst=False, yearfirst=False)
    day_of_week_2 = datetime_series_2.dt.dayofweek
    print_debug_info(dates2, datetime_series_2, day_of_week_2)
    print("Is weekend (Sat/Sun):\n", is_weekend(dates2, weekend_days="sat_sun"))

    # Example 3: Series with mixed data and some unparseable entries
    dates3 = pd.Series([
        "2025-06-13",  # Friday
        "Invalid Date",
        "2025-06-14",  # Saturday
        "25-12-2024",  # Christmas Day, Wednesday
        12345,         # Unlikely to be parsed as a date without specific format
        "Sunday"
    ])
    print("\n--- Example 3: Mixed Data (Fri/Sat weekend) ---")
    print("Original Series:\n", dates3)
    # Debug prints for Example 3
    datetime_series_3 = pd.to_datetime(dates3, errors='coerce', dayfirst=False, yearfirst=False)
    day_of_week_3 = datetime_series_3.dt.dayofweek
    print_debug_info(dates3, datetime_series_3, day_of_week_3)
    print("Is weekend (Fri/Sat):\n", is_weekend(dates3, weekend_days="fri_sat"))

    # Example 4: Numbered Days (as part of full dates)
    dates4 = pd.Series([
        "2025-06-01", # Sunday
        "2025-06-02", # Monday
        "2025-06-07", # Saturday
        "2025-06-08"  # Sunday
    ])
    print("\n--- Example 4: Numbered Days (as part of full dates) (Sat/Sun weekend) ---")
    print("Original Series:\n", dates4)
    # Debug prints for Example 4
    datetime_series_4 = pd.to_datetime(dates4, errors='coerce', dayfirst=False, yearfirst=False)
    day_of_week_4 = datetime_series_4.dt.dayofweek
    print_debug_info(dates4, datetime_series_4, day_of_week_4)
    print("Is weekend (Sat/Sun):\n", is_weekend(dates4, weekend_days="sat_sun"))

    # Example 5: Empty Series
    empty_series = pd.Series([])
    print("\n--- Example 5: Empty Series ---")
    print("Original Series:\n", empty_series)
    # Debug prints for Example 5
    datetime_series_5 = pd.to_datetime(empty_series, errors='coerce', dayfirst=False, yearfirst=False)
    day_of_week_5 = datetime_series_5.dt.dayofweek
    print_debug_info(empty_series, datetime_series_5, day_of_week_5)
    print("Is weekend (Sat/Sun):\n", is_weekend(empty_series, weekend_days="sat_sun"))