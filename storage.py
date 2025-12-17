import json
import os

REMINDERS_FILE = "medication_reminders.json"
WELLNESS_FILE = "wellness_logs.json"
STEPS_FILE = "step_logs.json"

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_reminders(data):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_wellness_logs():
    if os.path.exists(WELLNESS_FILE):
        try:
            with open(WELLNESS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_wellness_logs(data):
    with open(WELLNESS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_step_logs():
    if os.path.exists(STEPS_FILE):
        try:
            with open(STEPS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_step_logs(data):
    with open(STEPS_FILE, "w") as f:
        json.dump(data, f, indent=4)
