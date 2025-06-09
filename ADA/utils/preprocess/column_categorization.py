import numpy as np
import pandas as pd
from scipy.stats import kruskal

def categorize_columns(df: pd.DataFrame, target: str) -> dict:
 """
 <b>Categorizes columns in a DataFrame into numeric (continuos, discrete), categorical (nominal, ordinal), and object (datetime, string).</b>

 :param df: pd.DataFrame - The DataFrame to categorize.
 :param target: str - The name of the target column for ordinal checks.
 :returns dict: A dictionary with keys 'continuous', 'discrete', 'nominal', 'ordinal', 'string' and 'datetime', each containing a list of column names.
 
 """
 columns_categories = {
  'continuous': [],
  'discrete': [],
  'nominal': [],
  'ordinal': [],
  'string': [],
  'datetime': []
 }

 for col in df.columns:
  #print(f"Processing column: {col}")
  if is_numeric(df[col]):
   
   if is_continuous(df[col]):
    columns_categories['continuous'].append(col)
   
   else:
    columns_categories['discrete'].append(col)
  
  elif is_object(df[col]):
  
   if is_datetime(df[col]):
    columns_categories['datetime'].append(col)
  
   elif is_categorical(df[col]):
     if is_ordinal(df[col], df[target]):
      columns_categories['ordinal'].append(col)
     else:
      columns_categories['nominal'].append(col)
   else:
    columns_categories['string'].append(col)

  else:
   raise ValueError(f"Column {col} does not fit any category.")
 return columns_categories


def is_numeric(col):
 """Check if a column is numeric."""
 return pd.api.types.is_numeric_dtype(col)

def is_continuous(col):
 """Check if a numeric column is continuous."""
 return pd.api.types.is_float_dtype(col)

def is_object(col):
 """Check if a column is of object type."""
 return pd.api.types.is_object_dtype(col)

def is_categorical(col):
 """Check if a column is categorical."""
 return col.nunique()/len(col) < 0.05  # Arbitrary threshold for categorical data

def is_ordinal(col: pd.Series, target_col: pd.Series, threshold: float = 0.05) -> bool:
 """check if a categorical column is ordinal or nominal."""
 # Kruskal-Wallis test or similar statistical tests can be used to determine if a categorical column is ordinal.
 # For simplicity, we assume that if a categorical column has more than 2 unique values, it is nominal.
 
 if not is_numeric(target_col):
  return False  # Kruskal-Wallis requires numeric target
 
 df = pd.DataFrame({'col': col, 'target': target_col})
 
 groups = df['col'].unique()
 
 if len(groups) < 2:
  return False
 
 data = [df[df['col'] == group]['target'].values for group in groups]
 
 stat, p_value = kruskal(*data)
 
 return p_value < threshold
  
import re
import pandas as pd

def is_datetime(col):
 """
 Check if a column contains datetime strings in any of these formats:
 - 27-Apr-22 (DD-MMM-YY)
 - 2025-03-18 (YYYY-MM-DD)
 - 2025-03-18 14:43:35.117 (YYYY-MM-DD HH:MM:SS.milliseconds)
 
 Returns:
  bool: True if at least one value matches a datetime format.
 """
 if pd.api.types.is_datetime64_any_dtype(col):
  return True  # Already datetime dtype
 
 sample = col.dropna().head(1000)  # Check first 1000 non-null values for efficiency
 if sample.empty:
  return False
 
 # Define regex patterns for the 3 formats
 patterns = [
  r'^\d{2}-[A-Za-z]{3}-\d{2}$',               # DD-MMM-YY (e.g., 27-Apr-22)
  r'^\d{4}-\d{2}-\d{2}$',                     # YYYY-MM-DD (e.g., 2025-03-18)
  r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+$'  # YYYY-MM-DD HH:MM:SS.milliseconds (e.g., 2025-03-18 14:43:35.117)
 ]
 
 # Check if any value matches any pattern
 for val in sample:
  val_str = str(val).strip()  # Convert to string and strip whitespace
  for pattern in patterns:
   if re.fullmatch(pattern, val_str):
    return True  # At least one valid datetime format found
 
 return False  # No matches found


if __name__ == "__main__":
 # Example usage
 import os
 path = r"C:\Users\DELL\OneDrive - AL-Hussien bin Abdullah Technical University\Attachments\HTU\Projects\Automated-Data-Analysis\ADA\datasets"
 targets = ['Boxes Shipped','money', 'Outcome', 'liveness_%','Survived']
 for file, target in zip(os.listdir(path),targets):
  if file.endswith('.csv') and file != 'spotify_2023.csv':
   print(f"Processing file: {file} with target: {target}")
   df = pd.read_csv(os.path.join(path, file))
   result = categorize_columns(df, target)
   print(result, "\n\n")
 #df = pd.read_csv(r"C:\Users\DELL\OneDrive - AL-Hussien bin Abdullah Technical University\Attachments\HTU\Projects\Automated-Data-Analysis\ADA\datasets\coffe.csv")
 