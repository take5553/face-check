import json
import os

target_path = os.path.join(os.path.dirname(__file__), 'setting.json')

def save(settings):
    with open(target_path, 'w') as f:
        json.dump(settings, f, indent=4)

def load():
    with open(target_path, 'r') as f:
        d = json.load(f)
    return d