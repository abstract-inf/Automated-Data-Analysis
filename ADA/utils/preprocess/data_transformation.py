from pathlib import Path
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
 """<b>Transform the DataFrame based on predefined column categories.</b>
 
 :param df: Input DataFrame to be transformed.
 :returns pd.DataFrame: Transformed DataFrame.

 """

 # Get the current script's directory (utils/modeling/)
 current_dir = Path(__file__).parent

 # Navigate two levels up to the root, then into "saved_data" folder
 try:
  target_dir = current_dir.parent.parent / "saved_data"
 except Exception as e:
  raise FileNotFoundError("The 'saved_data' directory does not exist. Please ensure the directory structure is correct.") from e

 # Define the JSON file path
 json_path = target_dir / "columns_categories.json"

 with open(json_path, 'r') as f:
  columns_categories = json.load(f)

 transform_continuous_columns(df, columns_categories)
 transform_discrete_columns(df, columns_categories)
 transform_nominal_columns(df, columns_categories)
 transform_ordinal_columns(df, columns_categories)
 transform_datetime_columns(df, columns_categories)
 drop_string_columns(df, columns_categories)
 # Save the transformed DataFrame to a CSV file
 export_transformed_data(df, target_dir / "transformed_data.csv")
 return df
 

def transform_continuous_columns(df, columns_categories):
 """<b>Transform continuous columns using StandardScaler.</b>"""
 for col in columns_categories['continuous']:
  scaler = StandardScaler()
  df[col] = scaler.fit_transform(df[[col]])
 return df

def transform_discrete_columns(df, columns_categories):
 """<b>Transform discrete columns using MinMaxScaler.</b>"""
 for col in columns_categories['discrete']:
  scaler = MinMaxScaler()
  df[col] = scaler.fit_transform(df[[col]])
 return df

def transform_nominal_columns(df, columns_categories):
 """<b>Transform nominal columns using OneHotEncoder.</b>"""
 for col in columns_categories['nominal']:
  encoder = OneHotEncoder(sparse_output=False, drop='first')
  transformed = encoder.fit_transform(df[[col]])
  df = df.drop(col, axis=1)
  df = pd.concat([df, pd.DataFrame(transformed, columns=encoder.get_feature_names_out([col]))], axis=1)
 return df

def transform_ordinal_columns(df, columns_categories):
 """<b>Transform ordinal columns using LabelEncoder.</b>"""
 for col in columns_categories['ordinal']:
  encoder = LabelEncoder()
  df[col] = encoder.fit_transform(df[col])
 return df

def transform_datetime_columns(df, columns_categories):
 """<b>Transform datetime columns to pandas datetime format.</b>"""
 for col in columns_categories['datetime']:
  df[col] = pd.to_datetime(df[col])

def drop_string_columns(df, columns_categories):
 """<b>Drop string columns from the DataFrame.</b>"""
 for col in columns_categories['string']:
  df.drop(col, axis=1, inplace=True)
 return df

def export_transformed_data(df: pd.DataFrame, file_path: str) -> None:
 """<b>Export the transformed DataFrame to a CSV file.</b>
 
 :param df: pd.DataFrame - The DataFrame to export.
 :param file_path: str - The path where the CSV file will be saved.
 """
 df.to_csv(file_path, index=False) 
 



if __name__ == "__main__":
 transform_data(pd.read_csv(r'C:\Users\DELL\OneDrive - AL-Hussien bin Abdullah Technical University\Attachments\HTU\Projects\Automated-Data-Analysis\ADA\datasets\coffe.csv'))

 