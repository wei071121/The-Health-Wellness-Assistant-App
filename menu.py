import tkinter as tk
import time
from utils import clear_window, darken_color

def create_glowing_title(root, text):
    """Create glowing title effect"""
    shadow_colors = ["#a0c4ff", "#b0d0ff", "#c0e0ff"]
    for i, color in enumerate(shadow_colors):
        tk.Label(root, text=text,
                 font=("Segoe UI", 28, "bold"),
                 fg=color,
                 bg="#c9d6ff").place(relx=0.5, y=60+i*2, anchor="center")
    
    tk.Label(root, text=text,
             font=("Segoe UI", 28, "bold"),
             fg="black",
             bg="#c9d6ff").place(relx=0.5, y=60, anchor="center")

def main_menu(root):
    clear_window(root)
    root.configure(bg="#c9d6ff")
    
    # Full-width header
    header_frame = tk.Frame(root, bg="#c9d6ff", height=120)
    header_frame.pack(fill="x", padx=40, pady=(20, 0))
    
    # Title that spans width
    tk.Label(header_frame, text="Health & Wellness Assistant", 
             font=("Segoe UI", 36, "bold"),
             fg="#2c3e50",
             bg="#c9d6ff").pack()
    
    tk.Label(header_frame, text="Your Complete Health Management Solution",
             font=("Segoe UI", 14),
             fg="#5a7cff",
             bg="#c9d6ff").pack(pady=(5, 0))
    
    # Decorative line under title
    tk.Frame(root, height=2, bg="#6fa8dc", bd=0).pack(fill="x", padx=80, pady=(10, 0))
    
    # Main content area - takes most of the screen
    content_frame = tk.Frame(root, bg="#d8e3ff")
    content_frame.pack(fill="both", expand=True, padx=40, pady=30)
    
    # Features section title
    tk.Label(content_frame, text="Health Management Tools",
             font=("Segoe UI", 24, "bold"),
             bg="#d8e3ff",
             fg="#2c3e50").pack(pady=(20, 30))
    
    # Container for feature cards
    cards_container = tk.Frame(content_frame, bg="#d8e3ff")
    cards_container.pack(fill="both", expand=True)
    
    # Import page functions
    from bmi_calculator import BMI_page
    from medication_reminder import medication_page
    from wellness_log import wellness_page
    from step_counter import step_counter_page
    
    # Feature cards in a single row
    features = [
        ("📊", "BMI & Calorie\nCalculator", 
         "Calculate BMI and daily\ncalorie requirements", 
         lambda: BMI_page(root), "#6fa8dc"),
        ("⏰", "Medication\nReminder", 
         "Set and manage\nmedication reminders", 
         lambda: medication_page(root), "#6fa8dc"),
        ("📝", "Daily Wellness\nLog", 
         "Track your daily wellness\nand mood", 
         lambda: wellness_page(root), "#6fa8dc"),
        ("👣", "Step Counter\nLog", 
         "Log and monitor\ndaily steps", 
         lambda: step_counter_page(root), "#6fa8dc"),
    ]
    
    # Create cards in a row
    for i, (icon, title, description, command, color) in enumerate(features):
        card_frame = tk.Frame(cards_container, bg="#d8e3ff")
        card_frame.pack(side="left", fill="both", expand=True, padx=15)
        
        # Card with shadow effect
        card = tk.Frame(card_frame, bg="white", width=200, height=250)
        card.pack_propagate(False)
        card.pack()
        
        # Card styling
        card.config(highlightbackground="#b8c9ff", highlightthickness=2)
        
        # Card content
        tk.Label(card, text=icon, font=("Segoe UI", 42),
                bg="white", fg=color).pack(pady=(30, 10))
        
        tk.Label(card, text=title, font=("Segoe UI", 16, "bold"),
                bg="white", fg="#2c3e50", wraplength=180).pack(pady=5)
        
        tk.Label(card, text=description, font=("Segoe UI", 11),
                bg="white", fg="#666666", wraplength=180).pack(pady=10, padx=10)
        
        # Card button
        card_btn = tk.Button(card, text="Open Feature →",
                           font=("Segoe UI", 11, "bold"),
                           bg=color,
                           fg="white",
                           relief="flat",
                           padx=20,
                           pady=8,
                           command=command)
        card_btn.pack(pady=20)
        
        # Hover effects for entire card
        def on_enter_card(e, c=card, b=card_btn, col=color):
            c.config(bg="#f8faff")
            c.config(highlightbackground=col)
            b.config(bg=darken_color(col, 20))
            b.config(cursor="hand2")
            c.config(cursor="hand2")
        
        def on_leave_card(e, c=card, b=card_btn, col=color):
            c.config(bg="white")
            c.config(highlightbackground="#b8c9ff")
            b.config(bg=col)
        
        card.bind("<Enter>", on_enter_card)
        card.bind("<Leave>", on_leave_card)
        card_btn.bind("<Enter>", on_enter_card)
        card_btn.bind("<Leave>", on_leave_card)
        card.bind("<Button-1>", lambda e, cmd=command: cmd())
    
    # Bottom section with exit button
    bottom_frame = tk.Frame(root, bg="#c9d6ff", height=100)
    bottom_frame.pack(side="bottom", fill="x", padx=40, pady=(0, 20))
    
    # Decorative line above exit button
    tk.Frame(bottom_frame, height=2, bg="#6fa8dc", bd=0).pack(fill="x", pady=(0, 20))
    
    # Centered exit button
    btn_frame = tk.Frame(bottom_frame, bg="#c9d6ff")
    btn_frame.pack()
    
    exit_btn = tk.Button(btn_frame, text="🚪 Exit Application",
                        font=("Segoe UI", 14, "bold"),
                        bg="#e74c3c",
                        fg="white",
                        width=25,
                        height=2,
                        relief="flat",
                        bd=0,
                        command=root.destroy)
    exit_btn.pack()
    
    # Hover effect for exit button
    def on_enter_exit(e):
        exit_btn.config(bg="#c0392b")
        exit_btn.config(cursor="hand2")
    
    def on_leave_exit(e):
        exit_btn.config(bg="#e74c3c")
    
    exit_btn.bind("<Enter>", on_enter_exit)
    exit_btn.bind("<Leave>", on_leave_exit)
    
    # Health tip at the bottom
    health_tips = [
        "💡 Tip: Drink 8 glasses of water daily for optimal health",
        "💡 Tip: Aim for 7-9 hours of sleep each night",
        "💡 Tip: Regular exercise boosts both physical and mental health",
        "💡 Tip: Balanced nutrition is key to maintaining good health"
    ]
    
    tip_label = tk.Label(bottom_frame, 
                        text=health_tips[0],
                        font=("Segoe UI", 11, "italic"),
                        bg="#c9d6ff",
                        fg="#5a7cff")
    tip_label.pack(pady=(15, 0))
    
    # Rotate tips
    def rotate_tip():
        current = tip_label.cget("text")
        index = health_tips.index(current) if current in health_tips else 0
        next_index = (index + 1) % len(health_tips)
        tip_label.config(text=health_tips[next_index])
        root.after(5000, rotate_tip)
    
    root.after(5000, rotate_tip)