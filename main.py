import tkinter as tk

from bmi_page import BMI_page
from medication_page import medication_page
from wellness_page import wellness_page
from step_counter_page import step_counter_page


# =====================================================
# MAIN APP WINDOW
# =====================================================
root = tk.Tk()
root.title("Personal Health Management System")
root.geometry("900x600")
root.configure(bg="#f5f7fa")


# =====================================================
# CLEAR WINDOW
# =====================================================
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# =====================================================
# MAIN MENU
# =====================================================
def main_menu():
    clear_window()

    container = tk.Frame(root, bg="#f5f7fa")
    container.pack(expand=True, fill="both")

    tk.Label(container,
             text="Personal Health Management System 🏥",
             font=("Segoe UI", 28, "bold"),
             bg="#f5f7fa").pack(pady=40)

    card = tk.Frame(container, bg="white", padx=50, pady=40)
    card.pack()

    def menu_button(text, command):
        tk.Button(card,
                  text=text,
                  font=("Segoe UI", 18),
                  width=22,
                  pady=10,
                  bg="#4da6ff",
                  fg="white",
                  relief="flat",
                  command=command).pack(pady=12)

    menu_button("BMI Calculator ⚖️",
                lambda: BMI_page(root, main_menu))

    menu_button("Medication Reminder 💊",
                lambda: medication_page(root, main_menu))

    menu_button("Daily Wellness Log 🌱",
                lambda: wellness_page(root, main_menu))

    menu_button("Step Counter 🚶‍♂️",
                lambda: step_counter_page(root, main_menu))

    tk.Button(container,
              text="❌ Exit",
              font=("Segoe UI", 14),
              bg="#e0e0e0",
              padx=20,
              pady=5,
              command=root.quit).pack(pady=30)


# =====================================================
# START APP
# =====================================================
main_menu()
root.mainloop()
