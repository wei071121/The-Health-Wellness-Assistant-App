import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os

# ----------------------------
# LIGHTED TITLE / GLOW EFFECT
# ----------------------------
def create_glowing_title(root, text):
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

# =====================================================
# JSON DATA HANDLING
# =====================================================
def save_data(file, data):
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to save {file}:\n{e}")

def load_data(file):
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # corrupted file: warn user and return empty list
        messagebox.showwarning("Data Warning", f"{file} is corrupted. Starting fresh.")
        return []
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to load {file}:\n{e}")
        return []

# =====================================================
# PAGE CLEAR FUNCTION
# =====================================================
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# =====================================================
# MAIN MENU WINDOW
# =====================================================
def main_menu():
    clear_window()
    root.configure(bg="#c9d6ff")
    create_glowing_title(root, "Health & Wellness Assistant App")
    card = tk.Frame(root, bg="white", padx=40, pady=40)
    card.pack(pady=100, padx=20, fill="both", expand=True)
    card.configure(highlightbackground="#d0d0d0", highlightthickness=1)

    btn_font = ("Segoe UI", 14, "bold")
    btn_options = {"width": 25, "height": 2, "font": btn_font, "relief": "flat", "bd": 0}

    tk.Button(card, text="BMI & Calorie Calculator", bg="#6fa8dc", fg="white",
              command=BMI_page, **btn_options).pack(pady=10)

    tk.Button(card, text="Medication Reminder", bg="#6fa8dc", fg="white",
              command=medication_page, **btn_options).pack(pady=10)

    tk.Button(card, text="Daily Wellness Log", bg="#6fa8dc", fg="white",
              command=wellness_page, **btn_options).pack(pady=10)

    tk.Button(card, text="Step Counter Log", bg="#6fa8dc", fg="white",
              command=step_counter_page, **btn_options).pack(pady=10)

    tk.Button(card, text="Exit App", bg="#e74c3c", fg="white",
              command=root.destroy, **btn_options).pack(pady=20)

# =====================================================
# BMI PAGE
# =====================================================
def BMI_page():
    clear_window()
    root.configure(bg="#f2f2f2")
    card = tk.Frame(root, bg="white", padx=40, pady=40)
    card.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(card, text="BMI Dashboard", font=("Segoe UI", 26, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0,20))

    tk.Label(card, text="Weight (kg):", font=("Segoe UI", 16), bg="white").grid(row=1, column=0, sticky="e", padx=15, pady=10)
    weight_entry = tk.Entry(card, font=("Segoe UI", 16), width=12, bd=2, relief="groove")
    weight_entry.grid(row=1, column=1, pady=10)

    tk.Label(card, text="Height (cm or m):", font=("Segoe UI", 16), bg="white").grid(row=2, column=0, sticky="e", padx=15, pady=10)
    height_entry = tk.Entry(card, font=("Segoe UI", 16), width=12, bd=2, relief="groove")
    height_entry.grid(row=2, column=1, pady=10)

    gauge_canvas = tk.Canvas(card, width=300, height=180, bg="white", highlightthickness=0)
    gauge_canvas.grid(row=3, column=0, columnspan=2, pady=20)
    result_label = tk.Label(card, text="", font=("Segoe UI", 18), bg="white")
    result_label.grid(row=4, column=0, columnspan=2, pady=10)
    bar_canvas = tk.Canvas(card, width=300, height=25, bg="white", highlightthickness=0)
    bar_canvas.grid(row=5, column=0, columnspan=2, pady=10)
    bar_canvas.create_rectangle(0, 0, 75, 25, fill="#4da6ff")
    bar_canvas.create_rectangle(75, 0, 150, 25, fill="#66cc66")
    bar_canvas.create_rectangle(150, 0, 225, 25, fill="#ffcc00")
    bar_canvas.create_rectangle(225, 0, 300, 25, fill="#ff6666")
    bar_pointer = bar_canvas.create_line(0, 0, 0, 25, width=4, fill="black")

    def calculate():
        # Validate inputs carefully
        w_raw = weight_entry.get().strip()
        h_raw = height_entry.get().strip()
        try:
            weight = float(w_raw)
        except ValueError:
            result_label.config(text="Invalid weight. Enter a number (kg).")
            return
        try:
            height = float(h_raw)
        except ValueError:
            result_label.config(text="Invalid height. Enter a number (cm or m).")
            return
        # If height looks like cm (greater than 3 meters), convert
        if height > 3:
            height = height / 100.0
        if height <= 0 or weight <= 0:
            result_label.config(text="Height and weight must be positive numbers.")
            return
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            cat = "Underweight"; x = 37
        elif bmi < 24.9:
            cat = "Normal"; x = 112
        elif bmi < 29.9:
            cat = "Overweight"; x = 187
        else:
            cat = "Obese"; x = 262
        calories = 22 * weight * 1.4  # simple estimate (you may want Mifflin-St Jeor)
        result_label.config(text=f"BMI: {bmi:.2f} ({cat})\nDaily Calories: {calories:.0f} kcal")
        bar_canvas.coords(bar_pointer, x, 0, x, 25)
        gauge_canvas.delete("all")
        gauge_canvas.create_arc(10,10,290,290,start=180,extent=180,style="arc",width=25,outline="#e6e6e6")
        angle = min(bmi,40)*(180/40)
        color = {"Underweight":"#4da6ff","Normal":"#66cc66","Overweight":"#ffcc00","Obese":"#ff6666"}[cat]
        gauge_canvas.create_arc(10,10,290,290,start=180,extent=angle,style="arc",width=25,outline=color)
        gauge_canvas.create_text(150,120,text=f"{bmi:.1f}",font=("Segoe UI",28,"bold"),fill=color)

    tk.Button(card,text="Calculate",font=("Segoe UI",16),bg="#4da6dc",fg="white",padx=20,pady=5,command=calculate).grid(row=6,column=0,columnspan=2,pady=(15,5))
    tk.Button(card,text="🔙 Back to Main Menu",font=("Segoe UI",14),bg="#e0e0e0",fg="black",padx=20,pady=5,command=main_menu).grid(row=7,column=0,columnspan=2,pady=10)

# =====================================================
# MEDICATION REMINDER PAGE
# =====================================================
def is_valid_time(t):
    t = t.strip()
    if not t:
        return False
    # accept "H:MM" or "HH:MM", 24-hour
    parts = t.split(":")
    if len(parts) != 2:
        return False
    hh, mm = parts
    if not (hh.isdigit() and mm.isdigit()):
        return False
    hh = int(hh); mm = int(mm)
    return 0 <= hh < 24 and 0 <= mm < 60

def medication_page():
    clear_window()
    class ScheduleApp:
        def __init__(self, frame):
            self.frame = frame
            self.frame.configure(bg="#f0f4f8")
            # separate files for reminders and log
            self.reminders_file = "medication_reminders.json"
            self.log_file = "medication_log.json"
            self.reminders = load_data(self.reminders_file)
            self.last_triggered_minute = None  # prevent repeated alerts same minute
            self.setup_ui()
            self.update_list()
            self.update_countdown()

        def setup_ui(self):
            tk.Label(self.frame,text="Schedule Reminder 💊",font=("Arial",24),bg="#f0f4f8",fg="#0b3d91").pack(pady=(15,10))
            self.label_next = tk.Label(self.frame,text="Next Schedule ⏰: --:--",font=("Arial",18),bg="#f0f4f8",fg="#2c3e50")
            self.label_next.pack(pady=(0,5))
            self.label_countdown = tk.Label(self.frame,text="Countdown ⏳: --:--:--",font=("Arial",18),bg="#f0f4f8",fg="#27ae60")
            self.label_countdown.pack(pady=(0,15))

            style = ttk.Style()
            try:
                style.theme_use("default")
            except:
                pass
            style.configure("Treeview.Heading", background="#34495e", foreground="white", font=("Arial", 12, "bold"))
            style.configure("Treeview", font=("Arial",11), rowheight=25, background="white", fieldbackground="white")
            style.map("Treeview", background=[("selected","#3498db")], foreground=[("selected","white")])

            columns = ("name","dosage","time","on")
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
            self.tree.pack(expand=True,fill="both",padx=20)

            btn_frame = tk.Frame(self.frame, bg="#f0f4f8")
            btn_frame.pack(pady=20)

            tk.Button(btn_frame,text="➕ Add",font=("Arial",16),width=10,command=self.open_add_window,bg="#2980b9",fg="white",relief="flat").pack(side="left", padx=10)
            tk.Button(btn_frame,text="✏️ Edit",font=("Arial",16),width=10,command=self.open_edit_window,bg="#2980b9",fg="white",relief="flat").pack(side="left", padx=10)
            tk.Button(btn_frame,text="📜 View History",font=("Arial",16),width=10,command=self.view_history,bg="#2980b9",fg="white",relief="flat").pack(side="left", padx=10)
            tk.Button(btn_frame,text="⬅ Back",font=("Arial",16),width=10,command=main_menu,bg="#2980b9",fg="white",relief="flat").pack(side="left", padx=10)

        def update_list(self):
            for row in self.tree.get_children(): self.tree.delete(row)
            for i,r in enumerate(self.reminders):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=(r.get("name",""),r.get("dosage",""),r.get("time",""),"ON" if r.get("on",True) else "OFF"), tags=(tag,))

        def get_next_reminder(self):
            now=datetime.now(); soonest=None; item=None
            for r in self.reminders:
                if not r.get("on", True): continue
                tim = r.get("time", "").strip()
                if not is_valid_time(tim): continue
                try:
                    h,m = map(int, tim.split(":"))
                except:
                    continue
                t = now.replace(hour=h,minute=m,second=0,microsecond=0)
                if t < now:
                    t += timedelta(days=1)
                if soonest is None or t < soonest:
                    soonest = t
                    item = r
            return soonest,item

        def update_countdown(self):
            next_time,item=self.get_next_reminder()
            if next_time:
                self.label_next.config(text=f"Next Schedule ⏰: {item['time']}")
                diff = next_time - datetime.now()
                total_sec = int(diff.total_seconds())
                if total_sec <= 0:
                    # trigger
                    curr_min = datetime.now().strftime("%Y-%m-%d %H:%M")
                    if curr_min != self.last_triggered_minute:
                        messagebox.showinfo("Reminder",f"Time to take medicine 💊:\n{item['name']} ({item['dosage']})")
                        # log into medication log
                        log = load_data(self.log_file)
                        log_entry = {"datetime": datetime.now().strftime("%Y-%m-%d %I:%M %p"), "name": item["name"], "dosage": item["dosage"], "time": item["time"]}
                        log.append(log_entry)
                        save_data(self.log_file, log)
                        self.last_triggered_minute = curr_min
                    # schedule next check quickly
                    self.frame.after(1000, self.update_countdown)
                    return
                h = total_sec // 3600
                m = (total_sec % 3600) // 60
                s = total_sec % 60
                self.label_countdown.config(text=f"Countdown ⏳: {h:02}:{m:02}:{s:02}")
            else:
                self.label_next.config(text="Next Schedule ⏰: --:--")
                self.label_countdown.config(text="Countdown ⏳: --:--:--")
            self.frame.after(1000, self.update_countdown)

        def open_add_window(self):
            win=tk.Toplevel(self.frame)
            win.title("➕ Add Reminder"); win.geometry("420x350")
            tk.Label(win,text="Medicine Name:",font=("Arial",16)).pack(pady=10)
            name_entry=tk.Entry(win,font=("Arial",16)); name_entry.pack()
            tk.Label(win,text="Dosage:",font=("Arial",16)).pack(pady=10)
            dose_entry=tk.Entry(win,font=("Arial",16)); dose_entry.pack()
            tk.Label(win,text="Time (HH:MM, 24h):",font=("Arial",16)).pack(pady=10)
            time_entry=tk.Entry(win,font=("Arial",16)); time_entry.pack()
            on_var = tk.BooleanVar(value=True)
            tk.Checkbutton(win, text="Enable Reminder", variable=on_var, font=("Arial", 14)).pack(pady=10)
            def save_new():
                name=name_entry.get().strip(); dose=dose_entry.get().strip(); tim=time_entry.get().strip()
                if not name or not dose or not tim:
                    messagebox.showwarning("Error","All fields required"); return
                if not is_valid_time(tim):
                    messagebox.showwarning("Error","Invalid time format (HH:MM)"); return
                self.reminders.append({"name":name,"dosage":dose,"time":tim,"on":on_var.get()})
                save_data(self.reminders_file, self.reminders)
                self.update_list()
                win.destroy()
            tk.Button(win,text="💾Save",font=("Arial",18),command=save_new).pack(pady=20)

        def open_edit_window(self):
            win=tk.Toplevel(self.frame)
            win.title("Edit Reminder"); win.geometry("420x350")
            names=[r.get("name","") for r in self.reminders]
            tk.Label(win,text="Select Reminder:",font=("Arial",16)).pack(pady=10)
            combo=ttk.Combobox(win, values=names, font=("Arial",16)); combo.pack()
            def edit_selected():
                sel=combo.get()
                if not sel:
                    messagebox.showwarning("Error","Select one"); return
                for r in self.reminders:
                    if r.get("name","")==sel:
                        self.edit_item_window(r)
                        win.destroy()
                        return
            def delete_selected():
                sel=combo.get()
                if not sel: messagebox.showwarning("Error","Select one"); return
                if messagebox.askyesno("Confirm Delete",f"Delete '{sel}'?"):
                    self.reminders=[r for r in self.reminders if r.get("name","")!=sel]
                    save_data(self.reminders_file,self.reminders)
                    self.update_list(); win.destroy()
            tk.Button(win,text="✏️ Edit",font=("Arial",16),command=edit_selected).pack(pady=10)
            tk.Button(win,text="🗑 Delete",font=("Arial",16),command=delete_selected).pack(pady=10)

        def edit_item_window(self,item):
            win=tk.Toplevel(self.frame); win.title("Edit Item"); win.geometry("420x360")
            tk.Label(win,text="Medicine Name:",font=("Arial",16)).pack(pady=10)
            name_e=tk.Entry(win,font=("Arial",16)); name_e.insert(0,item.get("name","")); name_e.pack()
            tk.Label(win,text="Dosage:",font=("Arial",16)).pack(pady=10)
            dose_e=tk.Entry(win,font=("Arial",16)); dose_e.insert(0,item.get("dosage","")); dose_e.pack()
            tk.Label(win,text="Time (HH:MM):",font=("Arial",16)).pack(pady=10)
            time_e=tk.Entry(win,font=("Arial",16)); time_e.insert(0,item.get("time","")); time_e.pack()
            on_var=tk.BooleanVar(value=item.get("on",True))
            tk.Checkbutton(win,text="Enabled Reminder",variable=on_var,font=("Arial",14)).pack(pady=10)
            def save_edit():
                name=name_e.get().strip(); dose=dose_e.get().strip(); tim=time_e.get().strip()
                if not name or not dose or not tim:
                    messagebox.showwarning("Error","All fields required"); return
                if not is_valid_time(tim):
                    messagebox.showwarning("Error","Invalid time"); return
                item["name"]=name; item["dosage"]=dose; item["time"]=tim; item["on"]=on_var.get()
                save_data(self.reminders_file,self.reminders)
                self.update_list(); win.destroy()
            tk.Button(win,text="💾Save Changes",font=("Arial",18),command=save_edit).pack(pady=20)

        def view_history(self):
            win=tk.Toplevel(self.frame)
            win.title("Medication History"); win.geometry("500x400")
            tk.Label(win,text="Medication History 💊",font=("Arial",16,"bold")).pack(pady=10)
            listbox=tk.Listbox(win,width=70,height=20); listbox.pack(padx=10,pady=10,fill="both",expand=True)
            log = load_data(self.log_file)
            for r in log:
                listbox.insert(tk.END, f"{r.get('datetime','')} | {r.get('name','')} | {r.get('dosage','')} | {r.get('time','')}")

    ScheduleApp(root)

# =====================================================
# DAILY WELLNESS LOG PAGE
# =====================================================
def wellness_page():
    clear_window()
    root.configure(bg="#c9d6ff")
    tk.Label(root, text="Daily Wellness Log", font=("Arial",22,"bold"), bg="#c9d6ff", fg="#2d2d2d").pack(pady=20)
    card = tk.Frame(root, bg="white", bd=0, relief="ridge")
    card.pack(pady=20, padx=20, fill="both", expand=True)
    card.configure(highlightbackground="#d0d0d0", highlightthickness=1)
    card.pack_propagate(False)

    input_frame = tk.Frame(card, bg="white")
    input_frame.pack(pady=20)

    tk.Label(input_frame, text="Mood Today:", bg="white", font=("Arial",12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    mood_entry = tk.Entry(input_frame, width=35, font=("Arial",11), relief="groove", bd=2)
    mood_entry.grid(row=0, column=1, pady=10)
    tk.Label(input_frame, text="Hours of Sleep:", bg="white", font=("Arial",12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    sleep_entry = tk.Entry(input_frame, width=35, font=("Arial",11), relief="groove", bd=2)
    sleep_entry.grid(row=1, column=1, pady=10)
    tk.Label(input_frame, text="Meals Summary:", bg="white", font=("Arial",12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    meal_entry = tk.Entry(input_frame, width=35, font=("Arial",11), relief="groove", bd=2)
    meal_entry.grid(row=2, column=1, pady=10)

    tk.Label(card, text="Daily Logs", font=("Arial",14,"bold"), bg="white").pack(pady=10)
    log_list = tk.Listbox(card, width=70, height=10, font=("Arial",11), bd=2, relief="ridge")
    log_list.pack(pady=10)

    logs_file = "wellness_history.json"
    logs = load_data(logs_file)

    # preload listbox
    for l in logs:
        log_list.insert(tk.END, f"{l.get('datetime','')} | Mood: {l.get('mood','')} | Sleep: {l.get('sleep','')} hrs | Meals: {l.get('meals','')}")

    def add_log():
        mood = mood_entry.get().strip(); sleep = sleep_entry.get().strip(); meal = meal_entry.get().strip()
        if mood=="" or sleep=="" or meal=="":
            messagebox.showerror("Error","Please fill in all fields."); return
        # validate sleep numeric-ish
        try:
            _ = float(sleep)
        except ValueError:
            messagebox.showerror("Error","Hours of sleep must be a number (e.g., 7.5)."); return
        now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        entry = {"datetime": now_str, "mood": mood, "sleep": sleep, "meals": meal}
        logs.append(entry)
        save_data(logs_file, logs)
        log_list.insert(tk.END, f"{now_str} | Mood: {mood} | Sleep: {sleep} hrs | Meals: {meal}")
        mood_entry.delete(0, tk.END); sleep_entry.delete(0, tk.END); meal_entry.delete(0, tk.END)

    tk.Button(card, text="Add Log", width=15, height=1, bg="#6fa8dc", fg="white", font=("Arial",12,"bold"), relief="flat", command=add_log).pack(pady=10)

    def view_history():
        win=tk.Toplevel(); win.title("Wellness History"); win.geometry("600x400")
        tk.Label(win,text="Wellness History",font=("Arial",14,"bold")).pack(pady=10)
        listbox=tk.Listbox(win,width=80,height=20); listbox.pack(padx=10,pady=10,fill="both",expand=True)
        for l in logs:
            listbox.insert(tk.END, f"{l.get('datetime','')} | Mood: {l.get('mood','')} | Sleep: {l.get('sleep','')} hrs | Meals: {l.get('meals','')}")
    tk.Button(card, text="📜 View History", width=15, height=1, bg="#6fa8dc", fg="white", font=("Arial",12,"bold"), relief="flat", command=view_history).pack(pady=5)
    tk.Button(root, text="🔙 Back to Main Menu", width=25, bg="#444444", fg="white", font=("Arial",12), command=main_menu).pack(pady=15)

# =====================================================
# STEP COUNTER LOG PAGE
# =====================================================
def step_counter_page():
    clear_window()
    root.configure(bg="#c9d6ff")
    tk.Label(root,text="Step Counter Log",font=("Segoe UI",22,"bold"),bg="#c9d6ff").pack(pady=20)
    card=tk.Frame(root,bg="white",padx=30,pady=30)
    card.pack(pady=20)
    card.configure(highlightbackground="#d0d0d0",highlightthickness=1)
    frame=tk.Frame(card,bg="white"); frame.pack(pady=10)
    tk.Label(frame,text="Steps Today:",font=("Segoe UI",14),bg="white").grid(row=0,column=0,padx=10,pady=10)
    step_entry=tk.Entry(frame,width=20,font=("Segoe UI",14),bd=2,relief="groove"); step_entry.grid(row=0,column=1,pady=10)
    tk.Label(card,text="Step Log Records",font=("Segoe UI",14,"bold"),bg="white").pack(pady=10)
    log_list=tk.Listbox(card,width=50,height=8,font=("Segoe UI",12),bd=2,relief="ridge"); log_list.pack(pady=10)

    logs_file = "steps_history.json"
    logs = load_data(logs_file)
    for l in logs:
        log_list.insert(tk.END, f"{l.get('datetime','')} | Steps: {l.get('steps','')}")

    def add_steps():
        steps_raw = step_entry.get().strip()
        if steps_raw=="":
            messagebox.showerror("Error","Please enter the number of steps."); return
        try:
            steps = int(float(steps_raw))
            if steps < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error","Please enter a valid non-negative integer for steps."); return
        now_str=datetime.now().strftime("%Y-%m-%d %I:%M %p")
        entry = {"datetime": now_str, "steps": steps}
        logs.append(entry)
        save_data(logs_file, logs)
        log_list.insert(tk.END, f"{now_str} | Steps: {steps}")
        step_entry.delete(0, tk.END)

    tk.Button(card,text="Add Steps",font=("Segoe UI",14),bg="#6fa8dc",fg="white",padx=20,pady=5,relief="flat",command=add_steps).pack(pady=10)

    def view_history():
        win=tk.Toplevel(); win.title("Step History"); win.geometry("500x400")
        tk.Label(win,text="Step History",font=("Segoe UI",14,"bold")).pack(pady=10)
        listbox=tk.Listbox(win,width=60,height=20); listbox.pack(padx=10,pady=10,fill="both",expand=True)
        for l in logs: listbox.insert(tk.END, f"{l.get('datetime','')} | Steps: {l.get('steps','')}")
    tk.Button(card,text="📜 View History",font=("Segoe UI",14),bg="#6fa8dc",fg="white",padx=20,pady=5,relief="flat",command=view_history).pack(pady=5)
    tk.Button(root,text="🔙 Back to Main Menu",font=("Segoe UI",14),bg="#444444",fg="white",padx=20,pady=5,command=main_menu).pack(pady=15)


# =====================================================
# START APPLICATION
# =====================================================
root=tk.Tk()
root.title("Health & Wellness Assistant App")
root.geometry("820x550")
root.configure(bg="#e6e6e6")
main_menu()
root.mainloop()
