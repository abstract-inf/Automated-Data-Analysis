import pandas as pd

def check_nulls(df: pd.DataFrame) -> dict:
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    return nulls.to_dict()

"""
:param data: pd.DataFrame - The input data to be checked
Filters on columns names that contain missing values and return column name and its corresponding missing value,
if no missing values found it returns an empty dict
"""


if __name__ == "__main__":
    df = pd.read_csv(r"C:\ADA Project\Automated-Data-Analysis\ADA\datasets\coffe.csv")
    print(check_nulls(df))