# main.py
from sklearn.datasets import fetch_openml
from ADA import ADA

def load_titanic():
    """Load Titanic dataset from OpenML"""
    data = fetch_openml('titanic', version=1, as_frame=True)
    df = data.frame
    # Rename target column if needed
    if 'survived' in df.columns:
        df = df.rename(columns={'survived': 'target'})
    return df

def main():
    # Load data
    data = load_titanic()
    #print("Data loaded successfully. Shape:", data.shape)
    #print("Columns:", data.columns.tolist())
    # Initialize ADA object
    analyzer = ADA(data_path="ADA/datasets/house_price.csv", target='median_house_value', problem_type='regression')
    
    # Process and visualize
    analyzer.preprocess()
    analyzer.visualize()
    
    print("Analysis completed successfully!")

if __name__ == "__main__":
    main()