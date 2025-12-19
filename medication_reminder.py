import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from storage import load_reminders, save_reminders
from utils import clear_window, is_valid_time

# =====================================================
# MEDICATION REMINDER PAGE 
# =====================================================
def medication_page(root, main_menu_callback):
    clear_window(root)
    root.configure(bg="#f0f4f8")

    class ScheduleApp:
        def __init__(self, frame):
            self.frame = frame
            self.reminders = load_reminders()
            self.setup_ui()
            self.update_list()
            self.update_countdown()

        def setup_ui(self):
            tk.Label(self.frame, text="Schedule Reminder 💊",
                     font=("Arial", 24), bg="#f0f4f8", fg="#0b3d91").pack(pady=(15, 10))

            self.label_next = tk.Label(self.frame, text="Next Schedule ⏰: --:--",
                                       font=("Arial", 18), bg="#f0f4f8", fg="#2c3e50")
            self.label_next.pack(pady=(0, 5))

            self.label_countdown = tk.Label(self.frame, text="Countdown ⏳: --:--:--",
                                            font=("Arial", 18), bg="#f0f4f8", fg="#27ae60")
            self.label_countdown.pack(pady=(0, 15))

            style = ttk.Style()
            style.theme_use("default")
            style.configure("Treeview.Heading", background="#34495e", foreground="white",
                            font=("Arial", 12, "bold"))
            style.configure("Treeview", font=("Arial", 11), rowheight=25,
                            background="white", fieldbackground="white")
            style.map("Treeview",
                      background=[("selected", "#3498db")],
                      foreground=[("selected", "white")])

            columns = ("name", "dosage", "time", "on")
            self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=14)
            self.tree.heading("name", text="Medicine Name")
            self.tree.heading("dosage", text="Dosage")
            self.tree.heading("time", text="Time")
            self.tree.heading("on", text="On/Off")

            self.tree.column("name", width=220)
            self.tree.column("dosage", width=140)
            self.tree.column("time", width=140)
            self.tree.column("on", width=80)

            self.tree.tag_configure("oddrow", background="#ecf0f1")
            self.tree.tag_configure("evenrow", background="white")

            self.tree.pack(expand=True, fill="both", padx=20)

            btn_frame = tk.Frame(self.frame, bg="#f0f4f8")
            btn_frame.pack(pady=20)

            tk.Button(btn_frame, text="➕ Add", font=("Arial", 16),
                      width=10, command=self.open_add_window, bg="#2980b9",
                      fg="white", relief="flat").pack(side="left", padx=10)

            tk.Button(btn_frame, text="✏️ Edit", font=("Arial", 16),
                      width=10, command=self.open_edit_window, bg="#2980b9",
                      fg="white", relief="flat").pack(side="left", padx=10)

            tk.Button(btn_frame, text="🔙 Back", font=("Arial", 16),
                      width=10, command=lambda: main_menu_callback(root), bg="#2980b9",
                      fg="white", relief="flat").pack(side="left", padx=10)

        def update_list(self):
            for row in self.tree.get_children():
                self.tree.delete(row)

            for i, r in enumerate(self.reminders):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end",
                                 values=(r["name"], r["dosage"], r["time"],
                                         "ON" if r["on"] else "OFF"),
                                 tags=(tag,))

        def get_next_reminder(self):
            now = datetime.now()
            soonest = None
            item = None

            for r in self.reminders:
                if not r["on"]:
                    continue
                try:
                    h, m = map(int, r["time"].split(":"))
                except:
                    continue

                t = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if t < now:
                    t += timedelta(days=1)

                if soonest is None or t < soonest:
                    soonest = t
                    item = r
            return soonest, item

        def update_countdown(self):
            next_time, item = self.get_next_reminder()

            if next_time:
                self.label_next.config(text=f"Next Schedule ⏰: {item['time']}")
                diff = next_time - datetime.now()

                if diff.total_seconds() <= 1:
                    messagebox.showinfo("Reminder",
                                        f"Time to take medicine 💉:\n{item['name']} ({item['dosage']})")
                    self.frame.after(1000, self.update_countdown)
                    return

                h = diff.seconds // 3600
                m = (diff.seconds % 3600) // 60
                s = diff.seconds % 60
                self.label_countdown.config(text=f"Countdown ⏳: {h:02}:{m:02}:{s:02}")
            else:
                self.label_next.config(text="Next Schedule ⏰: --:--")
                self.label_countdown.config(text="Countdown ⏳: --:--:--")

            self.frame.after(1000, self.update_countdown)

        def open_add_window(self):
            win = tk.Toplevel(self.frame)
            win.title("➕ Add Reminder")
            win.geometry("420x350")
            win.configure(bg="#f0f4f8")

            tk.Label(win, text="Medicine Name:", font=("Arial", 16), bg="#f0f4f8").pack(pady=10)
            name_entry = tk.Entry(win, font=("Arial", 16))
            name_entry.pack()

            tk.Label(win, text="Dosage (numbers only):", font=("Arial", 16), bg="#f0f4f8").pack(pady=10)
            dose_entry = tk.Entry(win, font=("Arial", 16))
            dose_entry.pack()

            tk.Label(win, text="Time (HH:MM):", font=("Arial", 16), bg="#f0f4f8").pack(pady=10)
            time_entry = tk.Entry(win, font=("Arial", 16))
            time_entry.pack()

            def validate_dosage(dosage):
                """Check if dosage contains only numbers and optional units"""
                dosage = dosage.strip()
                if not dosage:
                    return False
                
                # Split by space to separate numbers from units
                parts = dosage.split()
                if len(parts) == 0:
                    return False
                
                # First part should be a number
                first_part = parts[0]
                if not first_part.replace('.', '', 1).isdigit():
                    return False
                
                return True

            def save_new():
                name = name_entry.get().strip()
                dose = dose_entry.get().strip()
                tim = time_entry.get().strip()

                if not name or not dose or not tim:
                    messagebox.showwarning("Error", "All fields required")
                    return
                
                if not validate_dosage(dose):
                    messagebox.showwarning("Error", 
                                         "Invalid dosage format!\n"
                                         "Please enter numbers only (e.g., '10' or '5 mg')\n"
                                         "Letters and symbols are not allowed in the number part.")
                    dose_entry.focus_set()
                    return
                
                if not is_valid_time(tim):
                    messagebox.showwarning("Error", "Invalid time format (HH:MM)")
                    return

                self.reminders.append({
                    "name": name,
                    "dosage": dose,
                    "time": tim,
                    "on": True
                })

                save_reminders(self.reminders)
                self.update_list()
                win.destroy()

            tk.Button(win, text="💾Save", font=("Arial", 18), command=save_new).pack(pady=20)

        def open_edit_window(self):
            win = tk.Toplevel(self.frame)
            win.title("Edit Reminder")
            win.geometry("420x350")
            win.configure(bg="#f0f4f8")

            names = [r["name"] for r in self.reminders]

            tk.Label(win, text="Select Reminder:", font=("Arial", 16), bg="#f0f4f8").pack(pady=10)
            combo = ttk.Combobox(win, values=names, font=("Arial", 16))
            combo.pack()

            def edit_selected():
                sel = combo.get()
                if not sel:
                    messagebox.showwarning("Error", "Select one")
                    return

                for r in self.reminders:
                    if r["name"] == sel:
                        self.edit_item_window(r)
                        win.destroy()
                        return

            def delete_selected():
                sel = combo.get()
                if messagebox.askyesno("Confirm Delete", f"Delete '{sel}'?"):
                    self.reminders = [r for r in self.reminders if r["name"] != sel]
                    save_reminders(self.reminders)
                    self.update_list()
                    win.destroy()

            tk.Button(win, text="✏️ Edit", font=("Arial", 16), command=edit_selected).pack(pady=10)
            tk.Button(win, text="🗑 Delete", font=("Arial", 16), command=delete_selected).pack(pady=10)

        def edit_item_window(self, item):
            win = tk.Toplevel(self.frame)
            win.title("Edit Item")
            win.geometry("420x360")
            win.configure(bg="#f0f4f8")

            tk.Label(win, text="Medicine Name:", font=("Arial", 16), bg="#f0f4f8").pack(pady=10)
            name_e = tk.Entry(win, font=("Arial", 16))
            name_e.insert(0, item["name"])
            name_e.pack()

            tk.Label(win, text="Dosage (numbers only):", font=("Arial", 16), bg="#f0f4f8").pack(pady=10)
            dose_e = tk.Entry(win, font=("Arial", 16))
            dose_e.insert(0, item["dosage"])
            dose_e.pack()

            tk.Label(win, text="Time (HH:MM):", font=("Arial", 16), bg="#f0f4f8").pack(pady=10)
            time_e = tk.Entry(win, font=("Arial", 16))
            time_e.insert(0, item["time"])
            time_e.pack()

            on_var = tk.BooleanVar(value=item.get("on", True))
            tk.Checkbutton(win, text="Enabled Reminder",
                           variable=on_var, font=("Arial", 14), bg="#f0f4f8").pack(pady=10)

            def validate_dosage(dosage):
                dosage = dosage.strip()
                if not dosage:
                    return False
                
                parts = dosage.split()
                if len(parts) == 0:
                    return False
                
                first_part = parts[0]
                if not first_part.replace('.', '', 1).isdigit():
                    return False
                
                return True

            def save_edit():
                name = name_e.get().strip()
                dose = dose_e.get().strip()
                tim = time_e.get().strip()

                if not name or not dose or not tim:
                    messagebox.showwarning("Error", "All fields required")
                    return
                
                if not validate_dosage(dose):
                    messagebox.showwarning("Error", 
                                         "Invalid dosage format!\n"
                                         "Please enter numbers only (e.g., '10' or '5 mg')\n"
                                         "Letters and symbols are not allowed in the number part.")
                    dose_e.focus_set()
                    return
                
                if not is_valid_time(tim):
                    messagebox.showwarning("Error", "Invalid time")
                    return

                item["name"] = name
                item["dosage"] = dose
                item["time"] = tim
                item["on"] = on_var.get()

                save_reminders(self.reminders)
                self.update_list()
                win.destroy()

            tk.Button(win, text="💾Save Changes", font=("Arial", 18),
                      command=save_edit).pack(pady=20)

    ScheduleApp(root)
   

