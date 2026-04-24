import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(r"C:\Users\pari0\OneDrive\Desktop\sales_dataset.csv")

print(df)

# Line Plot
plt.plot(df["Day"], df["Sales"])
plt.title("Sales Trend")
plt.xlabel("Day")
plt.ylabel("Sales")
plt.show()

# Bar Chart
plt.bar(df["Day"], df["Sales"])
plt.title("Sales Bar Chart")
plt.show()

# Histogram
plt.hist(df["Sales"])
plt.title("Sales Distribution")
plt.show()