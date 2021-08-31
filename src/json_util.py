import json
import os
from device_check import get_device_id, get_format
import gst_builder

target_path = os.path.join(os.path.dirname(__file__), 'setting.json')

def save(settings):
    with open(target_path, 'w') as f:
        json.dump(settings, f, indent=4)

def load():
    if os.path.exists(target_path):
        with open(target_path, 'r') as f:
            d = json.load(f)
    else:
        cap_device = get_device_id('usb')[0]
        format_ = get_format(cap_device)
        resolution = format_.resolution()
        d = {
            'camera_mode': 'usb',
            'cap_settings' : {
                'cap_mode' : format_.name,
                'cap_width' : int(resolution[0]),
                'cap_height' : int(resolution[1]),
                'cap_fps' : float(resolution[2])
            },
            'canvas_settings' : {
                'canvas_width' : 600,
                'canvas_height' : 860,
                'update_interval' : 15,
                'portrait' : True
            }
        }
        gst_str = gst_builder.get_gst(d)
        d['gst_str'] = gst_str
        save(d)
    return d