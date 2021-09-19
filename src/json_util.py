import json
import os
from device_check import get_device_id, get_format, get_device_list
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
        device_str = get_device_list()
        if device_str == '':
            raise RuntimeError('No device detected.')
        _, device = device_str.split()[0].split(':')
        cap_device = get_device_id(device)[0]
        format_ = get_format(cap_device)
        resolution = format_.resolution()
        d = {
            'camera_mode': device,
            'cap_settings' : {
                'cap_mode' : format_.name,
                'cap_width' : int(resolution[0]),
                'cap_height' : int(resolution[1]),
                'cap_fps' : float(resolution[2]),
                'cap_rotation' : 0
            },
            'canvas_settings' : {
                'canvas_width' : 600,
                'canvas_height' : 860,
                'update_interval' : 15
            },
            'save_dir' : os.path.dirname(os.path.abspath(__file__)) + "/data/",
            'save_dir_onepic' : 'onepic/'
        }
        gst_str = gst_builder.get_gst(d)
        d['gst_str'] = gst_str
        save(d)
    return d