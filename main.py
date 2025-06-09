# main.py
import ADA
from sklearn.datasets import load_iris

# Load sample data
data = load_iris(as_frame=True).frame
# print(data.head())

# Initialize ADA object with the data
object = ADA(data)
object.preprocess()
object.visualize()
object.save_to_pdf()

print("Test 2")