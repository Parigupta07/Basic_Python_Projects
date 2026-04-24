import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv(r"C:\Users\pari0\OneDrive\Desktop\disease_dataset.csv")

print("\nDataset Loaded!")
print(df.head())


df.columns = df.columns.str.lower()


df.fillna(0, inplace=True)

# Encode ONLY target column (disease)
le = LabelEncoder()
df["disease"] = le.fit_transform(df["disease"])

# Features and target
X = df.drop("disease", axis=1)
y = df["disease"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))


print("\nEnter symptoms (0 or 1 for each):")

user_input = []
for col in X.columns:
    val = int(input(f"{col}: "))
    user_input.append(val)


user_input = pd.DataFrame([user_input], columns=X.columns)


prediction = model.predict(user_input)


predicted_label = le.inverse_transform(prediction)

print("\nPredicted Disease:", predicted_label[0])