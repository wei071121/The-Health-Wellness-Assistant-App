import tkinter as tk
from menu import main_menu

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Health & Wellness Assistant App")
    root.geometry("820x600")
    root.configure(bg="#c9d6ff")
    
    # Center the window
    window_width = 820
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    main_menu(root)
    root.mainloop()