import pandas as pd
from nulls_checking import check_nulls

def nulls_processing(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """
        Processes null values based on the selected strategy.
        - 'drop': drop rows or columns depending on null ratio
        - 'fill_avg': fill with mean (numeric) or mode (categorical)
        - 'fill_ffill': forward fill
        - 'fill_bfill': backward fill
        """
        null_info = check_nulls(df)
        if not null_info:
            print("No missing values to process.")
            return df

        threshold = 0.3  # Max allowed null ratio (30%)
        total_rows = len(df)

        for col, null_count in null_info.items():
            null_ratio = null_count / total_rows

            if null_ratio >= threshold:
                df = df.drop(columns=[col])
                print(f"{col} has been droped")
                continue  # Skip to next column

            # Handle based on strategy
            if strategy == "drop":
                df = df.dropna(subset=[col])

            elif strategy == "fill_avg":
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    mode_val = df[col].mode(dropna=True)
                    if not mode_val.empty:
                        df[col] = df[col].fillna(mode_val[0])
                    else:
                        df = df.drop(columns=[col])  # no valid mode

            elif strategy == "fill_ffill":
                df[col] = df[col].fillna(method="ffill")

            elif strategy == "fill_bfill":
                df[col] = df[col].fillna(method="bfill")

            print(f"Dropped or filled column: {col}") # can be remoed after finishing

        return df


if __name__ == "__main__":
    df = pd.read_csv(r"C:\ADA Project\Automated-Data-Analysis\ADA\datasets\coffe.csv")
    print("\n Coffe Data")
    print(f"Missing Data Before processing{check_nulls(df)}")
    df = nulls_processing(df)
    print(f"Missing Data After processing: {check_nulls(df)}")

    df = pd.read_csv(r"C:\ADA Project\Automated-Data-Analysis\ADA\datasets\Chocolate Sales.csv")
    print("\n Chocolate Data")
    print(f"Missing Data Before processing{check_nulls(df)}")
    df = nulls_processing(df)
    print(f"Missing Data After processing: {check_nulls(df)}")

    df = pd.read_csv(r"C:\ADA Project\Automated-Data-Analysis\ADA\datasets\diabetes.csv")
    print("\n diabetes Data")
    print(f"Missing Data Before processing{check_nulls(df)}")
    df = nulls_processing(df)
    print(f"Missing Data After processing: {check_nulls(df)}")

    df = pd.read_csv(r"C:\ADA Project\Automated-Data-Analysis\ADA\datasets\titanic.csv")
    print("\n titanic Data")
    print(f"Missing Data Before processing{check_nulls(df)}")
    df = nulls_processing(df)
    print(f"Missing Data After processing: {check_nulls(df)}")
