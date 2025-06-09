# main.py
from sklearn.datasets import load_iris

from ADA import ADA

# Load sample data
data = load_iris(as_frame=True).frame
# print(data.head())

# Initialize ADA object with the data
object = ADA(data, target_column='target')
object.preprocess()
object.visualize()
object.save_to_pdf()

print("Can you see me?")