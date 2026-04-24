import pandas as pd

# Load dataset (no user input needed)
df = pd.read_csv(r"C:\Users\pari0\OneDrive\Desktop\student_dataset.csv")

print("\n--- Dataset Info ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nStatistics:")
print(df.describe())