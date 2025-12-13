import tkinter as tk
from tkinter import ttk
from utils import clear_window
from menu import main_menu

def BMI_page(root):
    clear_window(root)
    root.configure(bg="#f2f2f2")

    # -------- MAIN CARD -------- #
    card = tk.Frame(root, bg="white", padx=40, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center")

    title = tk.Label(card, text="BMI Dashboard", font=("Segoe UI", 26, "bold"), bg="white")
    title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # -------- INPUT FIELDS -------- #
    tk.Label(card, text="Weight (kg):", font=("Segoe UI", 16), bg="white").grid(row=1, column=0, sticky="e", padx=15, pady=10)
    weight_entry = tk.Entry(card, font=("Segoe UI", 16), width=12, bd=2, relief="groove")
    weight_entry.grid(row=1, column=1, pady=10)

    tk.Label(card, text="Height (cm or m):", font=("Segoe UI", 16), bg="white").grid(row=2, column=0, sticky="e", padx=15, pady=10)
    height_entry = tk.Entry(card, font=("Segoe UI", 16), width=12, bd=2, relief="groove")
    height_entry.grid(row=2, column=1, pady=10)

    # -------- ACTIVITY LEVEL -------- #
    tk.Label(card, text="Activity Level:", font=("Segoe UI", 16), bg="white").grid(row=3, column=0, sticky="e", padx=15, pady=10)
    activity_var = tk.StringVar()
    activity_combo = ttk.Combobox(card, textvariable=activity_var, font=("Segoe UI", 14), width=14,
                                  values=[
                                      "Sedentary (little exercise)",
                                      "Lightly Active (1-3 days/wk)",
                                      "Moderately Active (3-5 days/wk)",
                                      "Very Active (6-7 days/wk)",
                                      "Extra Active (intense daily)"
                                  ])
    activity_combo.grid(row=3, column=1, pady=10)
    activity_combo.current(0)

    # -------- GOAL SELECTION -------- #
    tk.Label(card, text="Goal:", font=("Segoe UI", 16), bg="white").grid(row=4, column=0, sticky="e", padx=15, pady=10)
    goal_var = tk.StringVar()
    goal_combo = ttk.Combobox(card, textvariable=goal_var, font=("Segoe UI", 14), width=14,
                              values=["Maintain Weight", "Lose Weight", "Gain Weight"])
    goal_combo.grid(row=4, column=1, pady=10)
    goal_combo.current(0)

    # -------- GAUGE CANVAS -------- #
    gauge_canvas = tk.Canvas(card, width=300, height=180, bg="white", highlightthickness=0)
    gauge_canvas.grid(row=5, column=0, columnspan=2, pady=20)

    # -------- RESULT LABEL -------- #
    result_label = tk.Label(card, text="", font=("Segoe UI", 18), bg="white")
    result_label.grid(row=6, column=0, columnspan=2, pady=10)

    # -------- CALORIE COLOR BAR -------- #
    bar_canvas = tk.Canvas(card, width=300, height=25, bg="white", highlightthickness=0)
    bar_canvas.grid(row=7, column=0, columnspan=2, pady=10)

    bar_canvas.create_rectangle(0, 0, 75, 25, fill="#4da6ff")     # Underweight
    bar_canvas.create_rectangle(75, 0, 150, 25, fill="#66cc66")   # Normal
    bar_canvas.create_rectangle(150, 0, 225, 25, fill="#ffcc00")  # Overweight
    bar_canvas.create_rectangle(225, 0, 300, 25, fill="#ff6666")  # Obese

    bar_pointer = bar_canvas.create_line(0, 0, 0, 25, width=4, fill="black")

    # -------- CALCULATE FUNCTION -------- #
    def calculate():
        try:
            weight = float(weight_entry.get())
            height = float(height_entry.get())

            if height > 3:
                height /= 100

            bmi = weight / (height ** 2)

            # Category + pointer x-position
            if bmi < 18.5:
                cat = "Underweight"; x = 37
            elif bmi < 24.9:
                cat = "Normal"; x = 112
            elif bmi < 29.9:
                cat = "Overweight"; x = 187
            else:
                cat = "Obese"; x = 262

            # -------- ACTIVITY MULTIPLIER -------- #
            level = activity_var.get()
            if "Sedentary" in level: mult = 1.2
            elif "Lightly" in level: mult = 1.375
            elif "Moderately" in level: mult = 1.55
            elif "Very" in level: mult = 1.725
            else: mult = 1.9

            # -------- MAINTENANCE CALORIES -------- #
            maintenance = weight * 22 * mult

            # -------- GOAL CALORIES -------- #
            goal = goal_var.get()
            if goal == "Lose Weight":
                calories = maintenance - 400
            elif goal == "Gain Weight":
                calories = maintenance + 300
            else:
                calories = maintenance

            # Results text update
            result_label.config(
                text=f"BMI: {bmi:.2f} ({cat})\n"
                     f"Daily Calories ({goal}): {calories:.0f} kcal"
            )

            # Update pointer
            bar_canvas.coords(bar_pointer, x, 0, x, 25)

            # -------- GAUGE DRAW -------- #
            gauge_canvas.delete("all")

            gauge_canvas.create_arc(10, 10, 290, 290, start=180, extent=180,
                                    style="arc", width=25, outline="#e6e6e6")

            angle = min(bmi, 40) * (180 / 40)

            if cat == "Underweight": color="#4da6ff"
            elif cat == "Normal": color="#66cc66"
            elif cat == "Overweight": color="#ffcc00"
            else: color="#ff6666"

            gauge_canvas.create_arc(10, 10, 290, 290, start=180, extent=angle,
                                    style="arc", width=25, outline=color)

            gauge_canvas.create_text(150, 120, text=f"{bmi:.1f}", font=("Segoe UI", 28, "bold"), fill=color)

        except:
            result_label.config(text="Invalid input. Please enter numbers.")

    # -------- BUTTONS -------- #
    tk.Button(card, text="Calculate", font=("Segoe UI", 16),
              bg="#4da6ff", fg="white", padx=20, pady=5,
              command=calculate).grid(row=8, column=0, columnspan=2, pady=(15, 5))

    tk.Button(card, text="🔙 Back to Main Menu", font=("Segoe UI", 14),
              bg="#e0e0e0", fg="black", padx=20, pady=5,
              command=lambda: main_menu(root)).grid(row=9, column=0, columnspan=2, pady=10)