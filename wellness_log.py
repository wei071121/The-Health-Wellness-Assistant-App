import tkinter as tk
from tkinter import messagebox
from utils import clear_window
from menu import main_menu

def wellness_page(root):
    clear_window(root)

    # --- Beautiful Gradient Background ---
    root.configure(bg="#c9d6ff")

    # --- Title ---
    tk.Label(root, text="Daily Wellness Log", font=("Arial", 22, "bold"),
             bg="#c9d6ff", fg="#2d2d2d").pack(pady=20)

    # --- Modern Center Card ---
    card = tk.Frame(root, bg="white", bd=0, relief="ridge")
    card.pack(pady=20, padx=20, fill="both", expand=True)

    card.configure(highlightbackground="#d0d0d0", highlightthickness=1)
    card.pack_propagate(False)

    # --- Inputs inside card ---
    input_frame = tk.Frame(card, bg="white")
    input_frame.pack(pady=20)

    # Mood
    tk.Label(input_frame, text="Mood Today:", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    mood_entry = tk.Entry(input_frame, width=35, font=("Arial", 11), relief="groove", bd=2)
    mood_entry.grid(row=0, column=1, pady=10)

    # Sleep
    tk.Label(input_frame, text="Hours of Sleep:", bg="white", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    sleep_entry = tk.Entry(input_frame, width=35, font=("Arial", 11), relief="groove", bd=2)
    sleep_entry.grid(row=1, column=1, pady=10)

    # Meals
    tk.Label(input_frame, text="Meals Summary:", bg="white", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    meal_entry = tk.Entry(input_frame, width=35, font=("Arial", 11), relief="groove", bd=2)
    meal_entry.grid(row=2, column=1, pady=10)

    # --- Log Display ---
    tk.Label(card, text="Daily Logs", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    log_list = tk.Listbox(card, width=70, height=10, font=("Arial", 11), bd=2, relief="ridge")
    log_list.pack(pady=10)

    # --- Add Log Function ---
    def add_log():
        mood = mood_entry.get()
        sleep = sleep_entry.get()
        meal = meal_entry.get()

        if mood == "" or sleep == "" or meal == "":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        log_list.insert(tk.END, f"Mood: {mood} | Sleep: {sleep} hrs | Meals: {meal}")

        mood_entry.delete(0, tk.END)
        sleep_entry.delete(0, tk.END)
        meal_entry.delete(0, tk.END)

    # --- Add Log Button ---
    tk.Button(card, text="Add Log", width=15, height=1,
              bg="#6fa8dc", fg="white", font=("Arial", 12, "bold"),
              relief="flat", command=add_log).pack(pady=10)

    # --- Back Button ---
    tk.Button(root, text="🔙 Back to Main Menu", width=25,
              bg="#444444", fg="white", font=("Arial", 12),
              command=lambda: main_menu(root)).pack(pady=15)