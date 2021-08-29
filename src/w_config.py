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
        self._set_combo2_values()
        self._set_combo1_values()


    def _create_widgets(self):
        
        # Device Label
        self._frame4 = ttk.Frame(self)
        self._frame4.grid(column=0, row=0, padx=10, pady=10)
        self._label3 = ttk.Label(self._frame4, text="Device")
        self._label3.grid()
        
        # Device ComboBox
        self._frame5 = ttk.Frame(self)
        self._frame5.grid(column=1, row=0, padx=10, pady=10)
        self._combo2 = ttk.Combobox(self._frame5, state="readonly", width=30)
        self._combo2.bind("<<ComboboxSelected>>", self._combo2_on_selected)
        self._combo2.grid()

        # Resolution Label
        self._frame1 = ttk.Frame(self)
        self._frame1.grid(column=0, row=1, padx=10, pady=10)
        self._label1 = ttk.Label(self._frame1, text="Resolution")
        self._label1.grid()
        
        # Resolution ComboBox
        self._frame2 = ttk.Frame(self)
        self._frame2.grid(column=1, row=1, padx=10, pady=10)
        self._combo1 = ttk.Combobox(self._frame2, state="readonly", width=30)
        self._combo1.bind("<<ComboboxSelected>>", self._combo1_on_selected)
        self._combo1.grid()
        
        # Save Button
        self._frame3 = ttk.Frame(self)
        self._frame3.grid(column=1, row=2, padx=10, pady=10, sticky=tk.E)
        self._button1 = ttk.Button(self._frame3, text="Save", command=self._save)
        self._button1.grid()
        
        
    def _set_combo2_values(self):
        cameras = ['usb', 'csi']
        self._combo2.configure(values=cameras)
        if self._camera_mode == None:
            self._combo2.current(0)
            self._camera_mode = cameras[0]
        else:
            if self._camera_mode == cameras[0]:
                self._combo2.current(0)
            else:
                self._combo2.current(1)


    def _set_combo1_values(self):
        values = []
        self._resolutions = []
        device_id = dc.get_device_id(self._camera_mode)[0]
        formats = dc.get_formats(device_id)
        for format_ in formats:
            for resolution in format_.resolutions:
                values += ['{} : {}x{} ({} fps)'.format(format_.name, resolution[0], resolution[1], resolution[2])]
                self._resolutions += [(format_.name, resolution[0], resolution[1], resolution[2])]
        self._combo1.configure(values=values)


    def _combo1_on_selected(self, e):
        self._selected_resolution = self._resolutions[e.widget.current()]
        print('selected resolution: {}'.format(self._selected_resolution))
        
        
    def _combo2_on_selected(self, e):
        self._camera_mode = e.widget.get()
        self._set_combo1_values()
        
        
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