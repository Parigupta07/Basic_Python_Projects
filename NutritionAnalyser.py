# FOOD NUTRITION ANALYZER (GUI )

import pandas as pd
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


# DATASET

data = {
    "Food": [
        "Apple", "Banana", "Rice", "Milk", "Egg", "Bread", "Chicken", "Fish",
        "Potato", "Tomato", "Cheese", "Butter", "Orange", "Mango",
        "Paneer", "Dal", "Oats", "Almonds", "Yogurt", "Spinach"
    ],
    "Calories": [
        52, 96, 130, 42, 155, 265, 239, 206,
        77, 18, 402, 717, 47, 60,
        265, 116, 389, 579, 59, 23
    ],
    "Protein": [
        0.3, 1.3, 2.7, 3.4, 13, 9, 27, 22,
        2, 0.9, 25, 1, 0.9, 0.8,
        18, 9, 17, 21, 10, 2.9
    ],
    "Carbs": [
        14, 27, 28, 5, 1.1, 49, 0, 0,
        17, 3.9, 1.3, 0.1, 12, 15,
        6, 20, 66, 22, 3.6, 3.6
    ],
    "Fat": [
        0.2, 0.3, 0.3, 1, 11, 3.2, 14, 12,
        0.1, 0.2, 33, 81, 0.1, 0.4,
        20, 0.4, 7, 50, 0.4, 0.4
    ]
}

df = pd.DataFrame(data)



# FUNCTIONS

def fill_entry(event):
    selected = listbox.get(listbox.curselection())
    entry.delete(0, tk.END)
    entry.insert(0, selected)


def search_food():
    food = entry.get().strip()
    result = df[df["Food"].str.lower() == food.lower()]

    if result.empty:
        messagebox.showerror("Error", "Food not found!")
        return

    row = result.iloc[0]

    result_text.set(
        f"Calories: {row['Calories']}\n"
        f"Protein: {row['Protein']}\n"
        f"Carbs: {row['Carbs']}\n"
        f"Fat: {row['Fat']}"
    )


def show_graph():
    food = entry.get().strip()
    result = df[df["Food"].str.lower() == food.lower()]

    if result.empty:
        messagebox.showerror("Error", "Food not found!")
        return

    row = result.iloc[0]

    labels = ["Calories", "Protein", "Carbs", "Fat"]
    values = [row["Calories"], row["Protein"], row["Carbs"], row["Fat"]]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values)
    plt.title(f"Nutrition of {food}")
    plt.show()


def compare_foods():
    foods = entry.get().split(",")
    foods = [f.strip() for f in foods]

    selected = df[df["Food"].isin(foods)]

    if selected.empty:
        messagebox.showerror("Error", "Invalid food names!")
        return

    selected.set_index("Food").plot(kind="bar", figsize=(8, 5))
    plt.title("Food Comparison")
    plt.show()



# GUI DESIGN

root = tk.Tk()
root.title("Food Nutrition Analyzer")
root.geometry("500x400")

tk.Label(root, text="Food Nutrition Analyzer", font=("Arial", 16, "bold")).pack(pady=10)

# Entry box
tk.Label(root, text="Enter Food (or comma-separated):").pack()
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Buttons
tk.Button(root, text="Search", command=search_food, width=15).pack(pady=5)
tk.Button(root, text="Show Graph", command=show_graph, width=15).pack(pady=5)
tk.Button(root, text="Compare Foods", command=compare_foods, width=15).pack(pady=5)

# Result display
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, font=("Arial", 12)).pack(pady=10)

# FOOD LIST DISPLAY

tk.Label(root, text="Available Foods:", font=("Arial", 12, "bold")).pack()

frame = tk.Frame(root)
frame.pack()

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, height=8, yscrollcommand=scrollbar.set)
for food in df["Food"]:
    listbox.insert(tk.END, food)

listbox.pack(side=tk.LEFT)
scrollbar.config(command=listbox.yview)

# Click event
listbox.bind("<<ListboxSelect>>", fill_entry)


root.mainloop()