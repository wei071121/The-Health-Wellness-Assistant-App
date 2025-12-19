import tkinter as tk
import menu

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Health & Wellness Assistant App")
    root.geometry("820x550")
    root.configure(bg="#e6e6e6")

    menu.main_menu(root)
    root.mainloop()

