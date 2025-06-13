import os
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score
import pandas as pd
from pathlib import Path
import json

def model_data(df: pd.DataFrame, target_col: str,n: int = 1000, model_type: str = 'classification') -> None:
 """<b>Model the DataFrame using various machine learning algorithms.</b>
 
 :param df: pd.DataFrame - The DataFrame to model.
 :param target_col: str - The name of the target column.
 :param n: int - Number of features to select using RFE (Recursive Feature Elimination).
 :param model_type: str - Type of model to use ('classification' or 'regression').
 :returns dict: A dictionary containing model performance metrics.
 
 """
 selected_model = model_selection(df, target_col, model_type)
 X = df.drop(columns=[target_col])
 y = df[target_col]
 rfe = RFE(estimator=selected_model, n_features_to_select=n)
 rfe.fit_transform(X, y)
 if rfe.support_.any():
  # Get the current script's directory (utils/modeling/)
  current_dir = Path(__file__).parent

  # Navigate two levels up to the root, then into "data" folder
  target_dir = current_dir.parent.parent / "saved_data"
  target_dir.mkdir(exist_ok=True)  # Create the folder if it doesn't exist

  # Define the JSON file path
  json_path = target_dir / "selected_features.json"

  with open(json_path, 'w') as f:
   selected_features = X.columns[rfe.support_].tolist()
   selected_features.append(target_col)  # Include the target column
   json.dump(selected_features, f, indent=4)
   print("Selected features saved to 'selected_features.json'")
  return selected_features.append(target_col)
 return None

def model_selection(df: pd.DataFrame, target_col: str, model_type: str = 'classification') -> dict:
 """<b>Select and evaluate machine learning models on the DataFrame.</b>"""
 # Split the data into features and target
 X = df.drop(columns=[target_col])
 y = df[target_col]

 # Split into training and testing sets
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

 # Initialize models based on the type
 if model_type == 'classification':
  models = {
   'Logistic Regression': LogisticRegression(max_iter=1000),
   'Random Forest': RandomForestClassifier(),
   #'SVC': SVC(),
   'Decision Tree': DecisionTreeClassifier(),
   #'KNN': KNeighborsClassifier()
  }
 else:
  models = {
   'Linear Regression': LinearRegression(),
   'Random Forest': RandomForestRegressor(),
   #'SVR': SVR(),
   'Decision Tree': DecisionTreeRegressor(),
   #'KNN': KNeighborsRegressor()
  }

 results = [None, -999999999999]

 for name, model in models.items():
  # Fit the model
  print(f"Training {name}...")
  model.fit(X_train, y_train)
  
  # Make predictions
  y_pred = model.predict(X_test)
  
  # Calculate performance metrics
  if model_type == 'classification':
   accuracy = accuracy_score(y_test, y_pred)
   f1 = f1_score(y_test, y_pred, average='weighted')
   results = [model, 5*accuracy + 10*f1] if 5*accuracy + 10*f1 > results[1] else results
  else:
   mse = mean_squared_error(y_test, y_pred)
   r2 = r2_score(y_test, y_pred)
   results = [model, 5*r2 - mse] if 5*r2 - mse > results[1] else results


 return results[0]


if __name__ == "__main__":
 # Example usage
 data_path = Path(r'C:\Users\DELL\OneDrive - AL-Hussien bin Abdullah Technical University\Attachments\HTU\Projects\Automated-Data-Analysis\ADA\saved_data')
 data = pd.read_csv(data_path / 'transformed_data.csv')
 data.dropna(inplace=True)  # Drop rows with NaN values

 #print(data.info())  # Ensure no NaN values for modeling

 results = model_data(data, target_col='Survived',model_type='classification')
 #print(results)