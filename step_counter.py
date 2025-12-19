import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from storage import load_step_logs, save_step_logs
from utils import clear_window

# =====================================================
# STEP COUNTER LOG PAGE
# =====================================================
def step_counter_page(root, main_menu_callback):
    clear_window(root)
    root.configure(bg="#c9d6ff")

    tk.Label(root, text="Step Counter Log", font=("Segoe UI", 22, "bold"),
             bg="#c9d6ff").pack(pady=20)

    card = tk.Frame(root, bg="white", padx=30, pady=30)
    card.pack(pady=20)
    card.configure(highlightbackground="#d0d0d0", highlightthickness=1)

    frame = tk.Frame(card, bg="white")
    frame.pack(pady=10)

    tk.Label(frame, text="Steps Today:", font=("Segoe UI", 14),
             bg="white").grid(row=0, column=0, padx=10, pady=10)
    
    def validate_numeric_input(char):
        return char.isdigit()
    
    vcmd = (root.register(validate_numeric_input), '%S')
    
    step_entry = tk.Entry(frame, width=20, font=("Segoe UI", 14),
                          bd=2, relief="groove", validate="key",
                          validatecommand=vcmd)
    step_entry.grid(row=0, column=1, pady=10)

    tk.Label(card, text="Step Log Records", font=("Segoe UI", 14, "bold"),
             bg="white").pack(pady=10)

    log_list = tk.Listbox(card, width=50, height=8,
                          font=("Segoe UI", 12), bd=2, relief="ridge")
    log_list.pack(pady=10)

    # Load existing steps
    steps = load_step_logs()
    for step in steps:
        log_list.insert(tk.END, step)

    def add_steps():
        steps = step_entry.get()
        
        if steps == "":
            messagebox.showerror("Error", "Please enter the number of steps.")
            step_entry.focus_set()
            return
        
        try:
            steps_num = int(steps)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            log_text = f"[{timestamp}] Steps: {steps_num:,}"
            log_list.insert(tk.END, log_text)
            
            # Save to file
            steps.append(log_text)
            save_step_logs(steps)
            
            step_entry.delete(0, tk.END)
            
            if steps_num >= 10000:
                messagebox.showinfo("Great Job!", f"🎉 Excellent! {steps_num:,} steps is amazing!")
            
        except ValueError:
            messagebox.showerror("Invalid Input", 
                                "❌ Error: Please enter numbers only!\n"
                                "Example: 5000, 10000, 7500\n"
                                "Letters and symbols are not allowed.")
            step_entry.delete(0, tk.END)
            step_entry.focus_set()

    tk.Button(card, text="Add Steps", font=("Segoe UI", 14),
              bg="#6fa8dc", fg="white", padx=20, pady=5,
              relief="flat", command=add_steps).pack(pady=10)

    tk.Button(root, text="🔙 Back to Main Menu", font=("Segoe UI", 14),
              bg="#444444", fg="white", padx=20, pady=5,
              command=lambda: main_menu_callback(root)).pack(pady=15)
