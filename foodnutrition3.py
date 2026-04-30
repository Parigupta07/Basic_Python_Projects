# food nutrition analyser

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


# FOOD DATA (approx values per 100g)


foods = {
    "Fruits": [
        {"Name":"Apple","Emoji":"🍎","Protein":0.3,"Carbs":14,"Fat":0.2,"Vitamins":8},
        {"Name":"Banana","Emoji":"🍌","Protein":1.1,"Carbs":23,"Fat":0.3,"Vitamins":7},
        {"Name":"Orange","Emoji":"🍊","Protein":0.9,"Carbs":12,"Fat":0.1,"Vitamins":10},
        {"Name":"Mango","Emoji":"🥭","Protein":0.8,"Carbs":15,"Fat":0.4,"Vitamins":9},
    ],

    "Vegetables": [
        {"Name":"Broccoli","Emoji":"🥦","Protein":2.8,"Carbs":7,"Fat":0.4,"Vitamins":10},
        {"Name":"Carrot","Emoji":"🥕","Protein":0.9,"Carbs":10,"Fat":0.2,"Vitamins":10},
        {"Name":"Spinach","Emoji":"🥬","Protein":2.9,"Carbs":3.6,"Fat":0.4,"Vitamins":10},
        {"Name":"Potato","Emoji":"🥔","Protein":2,"Carbs":17,"Fat":0.1,"Vitamins":5},
    ],

    "Protein Foods": [
        {"Name":"Chicken","Emoji":"🍗","Protein":27,"Carbs":0,"Fat":14,"Vitamins":5},
        {"Name":"Egg","Emoji":"🥚","Protein":13,"Carbs":1.1,"Fat":11,"Vitamins":6},
        {"Name":"Fish","Emoji":"🐟","Protein":22,"Carbs":0,"Fat":12,"Vitamins":7},
        {"Name":"Paneer","Emoji":"🧀","Protein":18,"Carbs":1.2,"Fat":20,"Vitamins":4},
    ],

    "Grains / Dairy": [
        {"Name":"Rice","Emoji":"🍚","Protein":2.7,"Carbs":28,"Fat":0.3,"Vitamins":3},
        {"Name":"Oats","Emoji":"🌾","Protein":16.9,"Carbs":66,"Fat":6.9,"Vitamins":5},
        {"Name":"Milk","Emoji":"🥛","Protein":3.4,"Carbs":5,"Fat":1,"Vitamins":6},
        {"Name":"Bread","Emoji":"🍞","Protein":9,"Carbs":49,"Fat":3.2,"Vitamins":4},
    ]
}

all_foods = []
for group in foods.values():
    all_foods.extend(group)


# COLORS


BG = "#E8FFF1"
CARD = "#FFFFFF"
TXT = "#14532D"
BTN = "#00B894"
BLUE = "#0984E3"

selected_foods = []


# HELPERS


def get_food(name):
    for item in all_foods:
        if item["Name"] == name:
            return item
    return None

def total(items, nutrient):
    return sum(x[nutrient] for x in items)


# FOOD BUTTON SELECT


def toggle_food(name, btn, emoji):

    if name in selected_foods:
        selected_foods.remove(name)
        btn.config(
            text=f"{emoji} {name}",
            bg="white",
            fg=TXT,
            relief="raised"
        )
    else:
        selected_foods.append(name)
        btn.config(
            text=f"✓ {emoji} {name}",
            bg=BLUE,
            fg="white",
            relief="sunken"
        )

    selected_label.config(
        text="Selected: " + (", ".join(selected_foods) if selected_foods else "None")
    )


# PIE CHART COMPARE (UPDATED UNLIMITED CHARTS)


def generate_chart():

    if not selected_foods:
        messagebox.showerror("Error", "Select foods first")
        return

    selected_by_cat = {}

    for food_name in selected_foods:
        for cat, items in foods.items():
            for item in items:
                if item["Name"] == food_name:
                    selected_by_cat.setdefault(cat, []).append(food_name)

    used_categories = list(selected_by_cat.keys())

    same_category = len(used_categories) == 1
    one_each = all(len(v) == 1 for v in selected_by_cat.values())

    if not same_category and not one_each:
        messagebox.showinfo(
            "Compare Rule",
            "To compare items:\n\n"
            "• Select only ONE item from each category\nOR\n"
            "• Select all desired items from the SAME category."
        )
        return

    # UPDATED PART: show all selected foods
    chosen = [get_food(x) for x in selected_foods]

    total_charts = len(chosen)
    cols = 3
    rows = (total_charts + cols - 1) // cols

    labels = ["Protein", "Carbs", "Fat"]
    colors = ["#4CAF50", "#FFD166", "#EF476F"]

    plt.figure(figsize=(5 * cols, 4 * rows))

    for i, item in enumerate(chosen):
        plt.subplot(rows, cols, i + 1)

        vals = [item["Protein"], item["Carbs"], item["Fat"]]

        wedges, texts, autotexts = plt.pie(
            vals,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title(item["Name"], fontsize=11, fontweight="bold")
        plt.legend(wedges, labels, fontsize=8)

    if same_category:
        plt.suptitle("Same Category Comparison", fontsize=13, fontweight="bold")
    else:
        plt.suptitle("Cross Category Comparison", fontsize=13, fontweight="bold")

    plt.tight_layout()
    plt.show()


# DIET WINDOW


def suggest_diet_window():

    win = tk.Toplevel(root)
    win.title("Suggest Diet Plan")
    win.geometry("780x620")
    win.config(bg=BG)

    current_selected = []
    nutrient_selected = []

    tk.Label(
        win,
        text="🥗 Smart Diet Planner",
        font=("Segoe UI",18,"bold"),
        bg=BG, fg=TXT
    ).pack(pady=10)

    top = tk.LabelFrame(
        win,
        text="Choose Nutrients To Prioritise",
        bg=CARD, fg=TXT,
        font=("Segoe UI",11,"bold")
    )
    top.pack(padx=10,pady=10,fill="x")

    nutrients = ["Protein","Carbs","Fat","Vitamins"]

    def toggle_nutrient(n,b):
        if n in nutrient_selected:
            nutrient_selected.remove(n)
            b.config(bg="white", fg=TXT, relief="raised")
        else:
            nutrient_selected.append(n)
            b.config(bg=BLUE, fg="white", relief="sunken")

    for n in nutrients:
        b = tk.Button(top,text=n,width=14,bg="white",
                      font=("Segoe UI",10,"bold"))
        b.config(command=lambda x=n,btn=b: toggle_nutrient(x,btn))
        b.pack(side="left", padx=8, pady=8)

    food_frame = tk.LabelFrame(
        win,
        text="Select Foods You Currently Eat",
        bg=CARD, fg=TXT,
        font=("Segoe UI",11,"bold")
    )
    food_frame.pack(padx=10,pady=10,fill="both",expand=True)

    def toggle_current(name, btn, emoji):
        if name in current_selected:
            current_selected.remove(name)
            btn.config(text=f"{emoji} {name}", bg="white", fg=TXT)
        else:
            current_selected.append(name)
            btn.config(text=f"✓ {emoji} {name}", bg=BLUE, fg="white")

    for category, items in foods.items():

        row = tk.Frame(food_frame,bg=CARD)
        row.pack(pady=6)

        tk.Label(
            row,text=category+":",
            width=12,bg=CARD,fg=TXT,
            font=("Segoe UI",10,"bold")
        ).pack(side="left")

        for item in items:

            btn = tk.Button(
                row,
                text=f"{item['Emoji']} {item['Name']}",
                bg="white",
                width=11,
                font=("Segoe UI",9)
            )

            btn.config(
                command=lambda n=item["Name"],b=btn,e=item["Emoji"]:
                toggle_current(n,b,e)
            )

            btn.pack(side="left", padx=4)

    result = tk.Label(
        win,
        text="",
        wraplength=720,
        bg=BG, fg=TXT,
        font=("Segoe UI",10)
    )
    result.pack(pady=10)

    graph_data = {}

    def create_plan():

        if not nutrient_selected:
            messagebox.showerror("Error","Choose nutrients first")
            return

        if not current_selected:
            messagebox.showerror("Error","Choose foods first")
            return

        current = [get_food(x) for x in current_selected]

        score_list = []

        for food in all_foods:
            score = 0
            for n in nutrient_selected:
                score += food[n]
            score_list.append((score, food))

        score_list.sort(reverse=True, key=lambda x:x[0])

        suggested = [x[1] for x in score_list[:4]]

        current_names = ", ".join(current_selected)
        suggested_names = ", ".join(x["Name"] for x in suggested)

        result.config(
            text=f"Current Diet:\n{current_names}\n\n"
                 f"Add to your Current Diet:\n{suggested_names}\n\n"
                 f"Click Show 1 Year Graph below."
        )

        graph_data["current"] = current
        graph_data["suggested"] = suggested
        graph_data["nutrients"] = nutrient_selected

    def show_graph():

        if not graph_data:
            messagebox.showerror("Error", "Generate plan first")
            return

        weeks = list(range(4, 53, 4))
        labels = [f"W{i}" for i in weeks]

        plt.figure(figsize=(10, 5))

        colors = {
            "Protein": "#00B894",
            "Carbs": "#F39C12",
            "Fat": "#E74C3C",
            "Vitamins": "#0984E3"
        }

        for nutrient in graph_data["nutrients"]:

            cur = total(graph_data["current"], nutrient)
            sug = total(graph_data["suggested"], nutrient)

            if sug <= cur:
                sug = cur * 1.25

            current_line = []
            suggested_line = []

            for i in range(len(weeks)):

                base_current = cur * (1 + i * 0.045)
                base_suggest = sug * (1 + i * 0.065)

                wave1 = np.sin(i * 0.8) * cur * 0.04
                wave2 = np.sin(i * 0.8 + 0.7) * sug * 0.05

                current_line.append(base_current + wave1)
                suggested_line.append(base_suggest + wave2)

            c = colors.get(nutrient, "blue")

            plt.plot(
                labels,
                current_line,
                linestyle="--",
                marker="o",
                linewidth=2,
                color=c,
                alpha=0.6,
                label=f"Current {nutrient}"
            )

            plt.plot(
                labels,
                suggested_line,
                linestyle="-",
                marker="o",
                linewidth=3,
                color=c,
                label=f"Suggested {nutrient}"
            )

        plt.title("1 Year Nutrient Progress Comparison",
                  fontsize=14, fontweight="bold")
        plt.xlabel("Time Passed (Every 4 Weeks)")
        plt.ylabel("Estimated Nutrient Intake Score")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    btn_frame = tk.Frame(win,bg=BG)
    btn_frame.pack(pady=12)

    tk.Button(
        btn_frame,
        text="Generate Diet Plan",
        bg=BTN, fg="white",
        width=18,
        font=("Segoe UI",11,"bold"),
        command=create_plan
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="Show 1 Year Graph",
        bg=BLUE, fg="white",
        width=18,
        font=("Segoe UI",11,"bold"),
        command=show_graph
    ).pack(side="left", padx=10)


# MAIN GUI


root = tk.Tk()
root.title("🥗 Food Nutrition Analyzer")
root.geometry("820x620")
root.resizable(False, False)
root.config(bg=BG)

tk.Label(
    root,
    text="🥗 Food Nutrition Analyzer",
    font=("Segoe UI",22,"bold"),
    bg=BG, fg=TXT
).pack(pady=8)

main = tk.Frame(root,bg=BG)
main.pack()

positions = [(0,0),(0,1),(1,0),(1,1)]

for idx,(category,items) in enumerate(foods.items()):

    r,c = positions[idx]

    card = tk.LabelFrame(
        main,
        text=category,
        bg=CARD, fg=TXT,
        font=("Segoe UI",11,"bold"),
        padx=8,pady=8
    )
    card.grid(row=r,column=c,padx=10,pady=10)

    for i,item in enumerate(items):

        btn = tk.Button(
            card,
            text=f"{item['Emoji']} {item['Name']}",
            width=14,
            bg="white",
            font=("Segoe UI",9)
        )

        btn.config(
            command=lambda n=item["Name"],b=btn,e=item["Emoji"]:
            toggle_food(n,b,e)
        )

        btn.grid(row=i//2,column=i%2,padx=4,pady=4)

selected_label = tk.Label(
    root,
    text="Selected: None",
    font=("Segoe UI",10,"bold"),
    bg=BG, fg=TXT
)
selected_label.pack(pady=5)

bottom = tk.Frame(root,bg=BG)
bottom.pack(pady=10)

tk.Button(
    bottom,
    text="📊 Generate Chart",
    width=18,height=2,
    bg=BTN, fg="white",
    font=("Segoe UI",11,"bold"),
    command=generate_chart
).pack(side="left", padx=10)

tk.Button(
    bottom,
    text="🥗 Suggest Diet Plan",
    width=18,height=2,
    bg=BLUE, fg="white",
    font=("Segoe UI",11,"bold"),
    command=suggest_diet_window
).pack(side="left", padx=10)

tk.Label(
    root,
    text="Healthy choices = Better life 💚",
    font=("Segoe UI",9,"italic"),
    bg=BG, fg=TXT
).pack(side="bottom", pady=10)

root.mainloop()