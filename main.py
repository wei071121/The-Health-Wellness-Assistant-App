"""
Health & Wellness Assistant - Main Application
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import json
import os
from datetime import datetime, timedelta


from bmi_calculator import BMI_page
from medication_reminder import medication_page
from wellness_log import wellness_page
from step_counter import step_counter_page
from storage import (
    load_reminders, save_reminders,
    load_wellness_logs, save_wellness_logs,
    load_step_logs, save_step_logs
)
from utils import is_valid_time


reminder_checking_active = False

def main_menu():
    clear_window()
    root.configure(bg="#c9d6ff")
    

    global reminder_checking_active
    if not reminder_checking_active:
        check_reminders_from_main()
        reminder_checking_active = True
    
    header_frame = tk.Frame(root, bg="#c9d6ff", height=120)
    header_frame.pack(fill="x", padx=40, pady=(20, 0))
    
    tk.Label(header_frame, text="Health & Wellness Assistant", 
             font=("Segoe UI", 36, "bold"),
             fg="#2c3e50",
             bg="#c9d6ff").pack()
    
    tk.Label(header_frame, text="Your Complete Health Management Solution",
             font=("Segoe UI", 14),
             fg="#5a7cff",
             bg="#c9d6ff").pack(pady=(5, 0))
    
    tk.Frame(root, height=2, bg="#6fa8dc", bd=0).pack(fill="x", padx=80, pady=(10, 0))
    
    content_frame = tk.Frame(root, bg="#d8e3ff")
    content_frame.pack(fill="both", expand=True, padx=40, pady=30)
    
    tk.Label(content_frame, text="Health Management Tools",
             font=("Segoe UI", 24, "bold"),
             bg="#d8e3ff",
             fg="#2c3e50").pack(pady=(20, 30))
    
    cards_container = tk.Frame(content_frame, bg="#d8e3ff")
    cards_container.pack(fill="both", expand=True)
    
    features = [
        ("📊", "BMI & Calorie\nCalculator", 
         "Calculate BMI and daily\ncalorie requirements", 
         open_bmi_page, "#6fa8dc"),
        ("⏰", "Medication\nReminder", 
         "Set and manage\nmedication reminders", 
         open_medication_page, "#6fa8dc"),
        ("📝", "Daily Wellness\nLog", 
         "Track your daily wellness\nand mood", 
         open_wellness_page, "#6fa8dc"),
        ("👣", "Step Counter\nLog", 
         "Log and monitor\ndaily steps", 
         open_step_counter_page, "#6fa8dc"),
    ]
    
    for i, (icon, title, description, command, color) in enumerate(features):
        card_frame = tk.Frame(cards_container, bg="#d8e3ff")
        card_frame.pack(side="left", fill="both", expand=True, padx=15)
        
        card = tk.Frame(card_frame, bg="white", width=200, height=250)
        card.pack_propagate(False)
        card.pack()
        
        card.config(highlightbackground="#b8c9ff", highlightthickness=2)
        
        tk.Label(card, text=icon, font=("Segoe UI", 42),
                bg="white", fg=color).pack(pady=(30, 10))
        
        tk.Label(card, text=title, font=("Segoe UI", 16, "bold"),
                bg="white", fg="#2c3e50", wraplength=180).pack(pady=5)
        
        tk.Label(card, text=description, font=("Segoe UI", 11),
                bg="white", fg="#666666", wraplength=180).pack(pady=10, padx=10)
        
        card_btn = tk.Button(card, text="Open Feature →",
                           font=("Segoe UI", 11, "bold"),
                           bg=color,
                           fg="white",
                           relief="flat",
                           padx=20,
                           pady=8,
                           command=command)
        card_btn.pack(pady=20)
        
        def on_enter_card(e, c=card, b=card_btn, col=color):
            c.config(bg="#f8faff")
            c.config(highlightbackground=col)
            b.config(bg="#5a96d9")
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
    
    bottom_frame = tk.Frame(root, bg="#c9d6ff", height=100)
    bottom_frame.pack(side="bottom", fill="x", padx=40, pady=(0, 20))
    
    tk.Frame(bottom_frame, height=2, bg="#6fa8dc", bd=0).pack(fill="x", pady=(0, 20))
    
    btn_frame = tk.Frame(bottom_frame, bg="#c9d6ff")
    btn_frame.pack()
    
    exit_btn = tk.Button(btn_frame, text="⏻ Exit Application",
                        font=("Segoe UI", 14, "bold"),
                        bg="#e74c3c",
                        fg="white",
                        width=20,
                        height=2,
                        relief="flat",
                        bd=0,
                        activebackground="#c0392b",
                        activeforeground="white",
                        cursor="hand2",
                        command=root.destroy)
    exit_btn.pack()
    
    exit_btn.config(highlightbackground="#c0392b", highlightthickness=1)
    
    def on_enter_exit(e):
        exit_btn.config(bg="#c0392b")
        exit_btn.config(cursor="hand2")
    
    def on_leave_exit(e):
        exit_btn.config(bg="#e74c3c")
    
    exit_btn.bind("<Enter>", on_enter_exit)
    exit_btn.bind("<Leave>", on_leave_exit)
    
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
    
    def rotate_tip():
        current = tip_label.cget("text")
        index = health_tips.index(current) if current in health_tips else 0
        next_index = (index + 1) % len(health_tips)
        tip_label.config(text=health_tips[next_index])
        root.after(5000, rotate_tip)
    
    root.after(5000, rotate_tip)

def check_reminders_from_main():
    """Check for reminders from main menu"""
    reminders = load_reminders()
    now = datetime.now()
    
    for reminder in reminders:
        if not reminder.get("on", True):
            continue
        
        try:
            h, m = map(int, reminder["time"].split(":"))
            reminder_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
            
            # Check if it's time for the reminder (within 1 minute)
            time_diff = abs((reminder_time - now).total_seconds())
            if time_diff <= 60:  # Within 1 minute
                messagebox.showinfo(
                    "Medication Reminder 💊",
                    f"Time to take medicine:\n"
                    f"Medicine: {reminder['name']}\n"
                    f"Dosage: {reminder['dosage']}\n"
                    f"Time: {reminder['time']}"
                )
        except:
            pass
    

    root.after(60000, check_reminders_from_main)


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def open_bmi_page():
    BMI_page(root, main_menu)

def open_medication_page():
    medication_page(root, main_menu)

def open_wellness_page():
    wellness_page(root, main_menu)

def open_step_counter_page():
    step_counter_page(root, main_menu)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Health & Wellness Assistant App")
    root.geometry("820x550")
    root.configure(bg="#e6e6e6")
    
    main_menu()
    root.mainloop()
