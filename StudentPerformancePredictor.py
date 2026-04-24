import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Sample dataset
data = {
    "hours": [1,2,3,4,5,6,7,8],
    "attendance": [50,60,65,70,75,80,85,90],
    "marks": [30,35,40,50,55,65,70,80]
}

df = pd.DataFrame(data)

X = df[["hours", "attendance"]]
y = df["marks"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction
h = float(input("Enter study hours: "))
a = float(input("Enter attendance: "))

pred = model.predict([[h, a]])
print("Predicted Marks:", pred[0])