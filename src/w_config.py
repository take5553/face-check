import json
import os
import tkinter as tk
from tkinter import ttk
import re
import device_check as dc


class ConfigWindow(ttk.Frame):
    def __init__(self, master=None, camera_mode=None):
        super().__init__(master)
        self.grid()

        self._camera_mode = camera_mode

        self._create_widgets()
        self._set_combo_dev_values()
        self._set_combo_res_values()


    def _create_widgets(self):
        
        row = 0
        
        # Device
        column = 0
        self._label_dev = ttk.Label(self, text="Device")
        self._label_dev.grid(column=column, row=row, padx=10, pady=10)
        column += 1
        self._combo_dev = ttk.Combobox(self, state="readonly", width=30)
        self._combo_dev.bind("<<ComboboxSelected>>", self._combo_dev_on_selected)
        self._combo_dev.grid(column=column, row=row, padx=10, pady=10)
        row += 1
        
        # Resolution
        column = 0
        self._label_res = ttk.Label(self, text="Resolution")
        self._label_res.grid(column=column, row=row, padx=10, pady=10)
        column += 1
        self._combo_res = ttk.Combobox(self, state="readonly", width=30)
        self._combo_res.bind("<<ComboboxSelected>>", self._combo_res_on_selected)
        self._combo_res.grid(column=column, row=row, padx=10, pady=10)
        row += 1
        
        # Save
        column = 0
        column += 1
        self._button_sav = ttk.Button(self, text="Save", command=self._save)
        self._button_sav.grid(column=column, row=row, padx=10, pady=10, sticky=tk.E)
        row += 1
        
        
    def _set_combo_dev_values(self):
        cameras = ['usb', 'csi']
        self._combo_dev.configure(values=cameras)
        if self._camera_mode == None:
            self._combo_dev.current(0)
            self._camera_mode = cameras[0]
        else:
            if self._camera_mode == cameras[0]:
                self._combo_dev.current(0)
            else:
                self._combo_dev.current(1)


    def _set_combo_res_values(self):
        values = []
        self._resolutions = []
        device_id = dc.get_device_id(self._camera_mode)[0]
        formats = dc.get_formats(device_id)
        for format_ in formats:
            for resolution in format_.resolutions:
                values += ['{} : {}x{} ({} fps)'.format(format_.name, resolution[0], resolution[1], resolution[2])]
                self._resolutions += [(format_.name, resolution[0], resolution[1], resolution[2])]
        self._combo_res.configure(values=values)


    def _combo_res_on_selected(self, e):
        self._selected_resolution = self._resolutions[e.widget.current()]
        print('selected resolution: {}'.format(self._selected_resolution))
        
        
    def _combo_dev_on_selected(self, e):
        self._camera_mode = e.widget.get()
        self._set_combo_res_values()
        
        
    def _save(self):
        settings = {
            'camera_mode': self._camera_mode,
            'cap_settings' : {
                'cap_mode' : self._selected_resolution[0],
                'cap_width' : int(self._selected_resolution[1]),
                'cap_height' : int(self._selected_resolution[2]),
                'cap_fps' : float(self._selected_resolution[3])
            },
            'canvas_settings' : {
                'canvas_width' : 600,
                'canvas_height' : 860,
                'update_interval' : 15,
                'portrait' : True
            }
        }
        target_path = os.path.join(os.path.dirname(__file__), 'setting.json')
        with open(target_path, 'w') as f:
            json.dump(settings, f, indent=4)


if __name__ == "__main__":
    window = tk.Tk()
    app = ConfigWindow(master=window, camera_mode='usb')
    app.mainloop()