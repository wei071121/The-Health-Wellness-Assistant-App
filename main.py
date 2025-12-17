import tkinter as tk

from bmi_page import BMI_page
from medication_page import medication_page
from wellness_page import wellness_page
from step_counter_page import step_counter_page


def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()


def main_menu():
    clear_window(root)
    root.configure(bg="#c9d6ff")

    tk.Label(root, text="Health & Wellness Assistant",
             font=("Segoe UI", 36, "bold"),
             bg="#c9d6ff").pack(pady=30)

    btn_style = {
        "font": ("Segoe UI", 14),
        "width": 25,
        "height": 2,
        "bg": "#6fa8dc",
        "fg": "white"
    }

    tk.Button(root, text="BMI & Calorie Calculator",
              command=lambda: BMI_page(root, main_menu), **btn_style).pack(pady=10)

    tk.Button(root, text="Medication Reminder",
              command=lambda: medication_page(root, main_menu), **btn_style).pack(pady=10)

    tk.Button(root, text="Daily Wellness Log",
              command=lambda: wellness_page(root, main_menu), **btn_style).pack(pady=10)

    tk.Button(root, text="Step Counter Log",
              command=lambda: step_counter_page(root, main_menu), **btn_style).pack(pady=10)

    tk.Button(root, text="Exit",
              command=root.destroy,
              bg="#e74c3c", fg="white",
              font=("Segoe UI", 14),
              width=25, height=2).pack(pady=30)


root = tk.Tk()
root.title("Health & Wellness Assistant")
root.geometry("820x550")

main_menu()
root.mainloop()
