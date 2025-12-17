import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from storage import load_wellness, save_wellness


def wellness_page(root, main_menu):
    # =====================================================
    # CLEAR WINDOW
    # =====================================================
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#eef2f7")

    container = tk.Frame(root, bg="#eef2f7")
    container.pack(expand=True, fill="both")

    tk.Label(container, text="Daily Wellness Log 🌱",
             font=("Segoe UI", 26, "bold"),
             bg="#eef2f7").pack(pady=20)

    form = tk.Frame(container, bg="white", padx=40, pady=30)
    form.pack()

    mood_var = tk.IntVar(value=5)
    stress_var = tk.IntVar(value=5)
    sleep_var = tk.IntVar(value=5)
    energy_var = tk.IntVar(value=5)

    def slider_row(text, var, row):
        tk.Label(form, text=text, font=("Segoe UI", 16),
                 bg="white").grid(row=row, column=0, sticky="w", pady=15)
        tk.Scale(form, from_=1, to=10, orient="horizontal",
                 variable=var, length=300,
                 bg="white", highlightthickness=0)\
            .grid(row=row, column=1, padx=20)

    slider_row("Mood 😊", mood_var, 0)
    slider_row("Stress 😰", stress_var, 1)
    slider_row("Sleep 😴", sleep_var, 2)
    slider_row("Energy ⚡", energy_var, 3)

    def save_log():
        record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "mood": mood_var.get(),
            "stress": stress_var.get(),
            "sleep": sleep_var.get(),
            "energy": energy_var.get()
        }

        logs = load_wellness()
        logs.append(record)
        save_wellness(logs)

        messagebox.showinfo(
            "Saved",
            "Wellness log saved successfully 🌱"
        )

    tk.Button(container, text="💾 Save Log",
              font=("Segoe UI", 16),
              bg="#4caf50", fg="white",
              padx=20, pady=5,
              command=save_log).pack(pady=20)

    tk.Button(container, text="🔙 Back to Main Menu",
              font=("Segoe UI", 14),
              bg="#dcdcdc",
              padx=20, pady=5,
              command=main_menu).pack(pady=10)
