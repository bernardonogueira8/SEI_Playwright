import os
import json

CONFIG_FILE = "config_sei.json"


def save_prefs(user, remember):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"user": user if remember else "", "remember": remember}, f)


def load_prefs():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"user": "", "remember": False}
