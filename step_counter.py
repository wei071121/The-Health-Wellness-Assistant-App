import tkinter as tk
from tkinter import messagebox
from utils import clear_window
from menu import main_menu

def step_counter_page(root):
    clear_window(root)

    # Background upgrade
    root.configure(bg="#c9d6ff")

    # Title
    tk.Label(root, text="Step Counter Log", font=("Segoe UI", 22, "bold"),
             bg="#c9d6ff").pack(pady=20)

    # Modern card
    card = tk.Frame(root, bg="white", padx=30, pady=30)
    card.pack(pady=20)
    card.configure(highlightbackground="#d0d0d0", highlightthickness=1)

    # Input frame
    frame = tk.Frame(card, bg="white")
    frame.pack(pady=10)

    tk.Label(frame, text="Steps Today:", font=("Segoe UI", 14),
             bg="white").grid(row=0, column=0, padx=10, pady=10)
    
    step_entry = tk.Entry(frame, width=20, font=("Segoe UI", 14),
                          bd=2, relief="groove")
    step_entry.grid(row=0, column=1, pady=10)

    # Log title
    tk.Label(card, text="Step Log Records", font=("Segoe UI", 14, "bold"),
             bg="white").pack(pady=10)

    # Listbox
    log_list = tk.Listbox(card, width=50, height=8,
                          font=("Segoe UI", 12), bd=2, relief="ridge")
    log_list.pack(pady=10)

    # Add Step Function
    def add_steps():
        steps = step_entry.get()

        if steps == "":
            messagebox.showerror("Error", "Please enter the number of steps.")
            return

        log_list.insert(tk.END, f"Steps: {steps}")
        step_entry.delete(0, tk.END)

    # Add Steps button
    tk.Button(card, text="Add Steps", font=("Segoe UI", 14),
              bg="#6fa8dc", fg="white", padx=20, pady=5,
              relief="flat", command=add_steps).pack(pady=10)

    # Back button - FIXED: Added value for padx and closed parentheses
    tk.Button(root, text="🔙 Back to Main Menu", font=("Segoe UI", 14),
              bg="#444444", fg="white", padx=20, pady=5,
              command=lambda: main_menu(root)).pack(pady=15)