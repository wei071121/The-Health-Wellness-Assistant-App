import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from storage import load_steps, save_steps


def step_counter_page(root, main_menu):
    # =====================================================
    # CLEAR WINDOW
    # =====================================================
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#f3f6fb")

    steps = tk.IntVar(value=0)

    frame = tk.Frame(root, bg="white", padx=40, pady=40)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Step Counter 🚶‍♂️",
             font=("Segoe UI", 26, "bold"),
             bg="white").pack(pady=(0, 20))

    step_label = tk.Label(frame, textvariable=steps,
                          font=("Segoe UI", 40, "bold"),
                          bg="white", fg="#1e88e5")
    step_label.pack(pady=10)

    def add_steps(amount):
        steps.set(steps.get() + amount)

    btn_frame = tk.Frame(frame, bg="white")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="+100",
              font=("Segoe UI", 16),
              width=8,
              command=lambda: add_steps(100)).grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="+500",
              font=("Segoe UI", 16),
              width=8,
              command=lambda: add_steps(500)).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="+1000",
              font=("Segoe UI", 16),
              width=8,
              command=lambda: add_steps(1000)).grid(row=0, column=2, padx=10)

    def save_today():
        data = load_steps()
        data.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "steps": steps.get()
        })
        save_steps(data)

        messagebox.showinfo(
            "Saved",
            "Today's steps saved successfully 🚶"
        )

    tk.Button(frame, text="💾 Save Today",
              font=("Segoe UI", 16),
              bg="#1e88e5", fg="white",
              padx=20, pady=5,
              command=save_today).pack(pady=15)

    tk.Button(frame, text="🔙 Back to Main Menu",
              font=("Segoe UI", 14),
              bg="#e0e0e0",
              padx=20, pady=5,
              command=main_menu).pack(pady=10)
