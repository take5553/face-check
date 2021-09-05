import tkinter as tk
from tkinter import ttk
import re
import device_check as dc
import gst_builder
import json_util as ju


class ConfigWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky=(tk.E, tk.W, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        self._settings = ju.load()

        self._create_widgets()
        self._set_combo_dev_values()
        self._set_combo_res_values()
        self._set_combo_rot_values()
        self._set_combo_fli_values()


    def _create_widgets(self):
        
        padx = 15
        pady = 10

        row = 0

        column = 0
        self._label_cap = ttk.Label(self, text="Capture")
        self._label_cap.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._label_dev = ttk.Label(self, text="Device")
        self._label_dev.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._combo_dev = ttk.Combobox(self, state="readonly", width=30)
        self._combo_dev.bind("<<ComboboxSelected>>", self._combo_dev_on_selected)
        self._combo_dev.grid(column=column, row=row, padx=padx, pady=pady)
        row += 1
        
        column = 0
        # blank cell
        column += 1
        self._label_res = ttk.Label(self, text="Resolution")
        self._label_res.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._combo_res = ttk.Combobox(self, state="readonly", width=30)
        self._combo_res.bind("<<ComboboxSelected>>", self._combo_res_on_selected)
        self._combo_res.grid(column=column, row=row, padx=padx, pady=pady)
        row += 1
        
        column = 0
        # blank cell
        column += 1
        self._label_rot = ttk.Label(self, text="Rotation")
        self._label_rot.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._combo_rot = ttk.Combobox(self, state="readonly", width=30)
        self._combo_rot.bind("<<ComboboxSelected>>", self._combo_rot_on_selected)
        self._combo_rot.grid(column=column, row=row, padx=padx, pady=pady)
        row += 1
        
        column = 0
        # blank cell
        column += 1
        self._label_fli = ttk.Label(self, text="Flip")
        self._label_fli.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._combo_fli = ttk.Combobox(self, state="readonly", width=30)
        self._combo_fli.bind("<<ComboboxSelected>>", self._combo_fli_on_selected)
        self._combo_fli.grid(column=column, row=row, padx=padx, pady=pady)
        row += 1
        
        column = 0
        self._label_can = ttk.Label(self, text="Canvas")
        self._label_can.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._label_can_wxh = ttk.Label(self, text="Width x Height")
        self._label_can_wxh.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._frame_can_wxh = ttk.Frame(self)
        self._frame_can_wxh.grid(column=column, row=row, padx=padx, pady=pady, sticky=tk.W)
        # -----------
        self._entry_can_width = ttk.Entry(self._frame_can_wxh, width=6)
        self._entry_can_width.grid(column=0, row=0)
        self._label_can_mul = ttk.Label(self._frame_can_wxh, text=' x ')
        self._label_can_mul.grid(column=1, row=0)
        self._entry_can_height = ttk.Entry(self._frame_can_wxh, width=6)
        self._entry_can_height.grid(column=2, row=0)
        # -----------
        row += 1
        
        column = 0
        # blank cell
        column += 1
        self._label_can_fps = ttk.Label(self, text="Update Interval")
        self._label_can_fps.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._frame_can_fps = ttk.Frame(self)
        self._frame_can_fps.grid(column=column, row=row, padx=padx, pady=pady, sticky=tk.W)
        # ----------
        self._entry_can_fps = ttk.Entry(self._frame_can_fps, width=4)
        self._entry_can_fps.grid(column=0, row=0)
        self._label_can_fpsunit = ttk.Label(self._frame_can_fps, text="ms")
        self._label_can_fpsunit.grid(column=1, row=0)
        # ----------
        row += 1
        
        column = 0
        # blank cell
        column += 1
        # blank cell
        column += 1
        self._frame_sav = ttk.Frame(self)
        self._frame_sav.grid(column=column, row=row, padx=padx, pady=pady, sticky=tk.E)
        # ----------
        self._label_sav = ttk.Label(self._frame_sav)
        self._label_sav.grid(column=0, row=0, padx=20, sticky=tk.E)
        self._button_sav = ttk.Button(self._frame_sav, text="Save", command=self._save)
        self._button_sav.grid(column=1, row=0)
        self._frame_sav.columnconfigure(0, weight=1)
        # ----------
        row += 1
        
        # Bind Variables
        vcmd = (self.register(lambda target: target.isdecimal() or len(target) == 0), '%P')
        self._canvas_width_var = tk.IntVar(value=self._settings['canvas_settings']['canvas_width'])
        self._entry_can_width.configure(textvariable=self._canvas_width_var, validate='key', validatecommand=vcmd)
        self._canvas_height_var = tk.IntVar(value=self._settings['canvas_settings']['canvas_height'])
        self._entry_can_height.configure(textvariable=self._canvas_height_var, validate='key', validatecommand=vcmd)
        self._canvas_fps_var = tk.IntVar(value=self._settings['canvas_settings']['update_interval'])
        self._entry_can_fps.configure(textvariable=self._canvas_fps_var, validate='key', validatecommand=vcmd)

        
    def _set_combo_dev_values(self):
        result = dc.get_device_list()
        if result == '':
            return
        device_list = result.split()
        cameras = []
        for device in device_list:
            _, device_name = device.split(':')
            cameras += [device_name]
        self._combo_dev.configure(values=cameras)
        for i in range(len(cameras)):
            if self._settings['camera_mode'] == cameras[i]:
                self._combo_dev.current(i)
                break
        else:
            self._combo_dev.current(0)


    def _set_combo_res_values(self):
        if self._combo_dev.get() == '':
            return
        values = []
        self._resolutions = []
        device_id = dc.get_device_id(self._combo_dev.get())[0]
        formats = dc.get_formats(device_id)
        for format_ in formats:
            for resolution in format_.resolutions:
                values += ['{} : {}x{} ({} fps)'.format(format_.name, resolution[0], resolution[1], resolution[2])]
                self._resolutions += [(format_.name, resolution[0], resolution[1], resolution[2])]
        self._combo_res.configure(values=values)
        
        setting_str = '{} : {}x{} ({:.3f} fps)'.format(self._settings['cap_settings']['cap_mode'], 
                                                       self._settings['cap_settings']['cap_width'], 
                                                       self._settings['cap_settings']['cap_height'], 
                                                       self._settings['cap_settings']['cap_fps'])
        for i in range(len(values)):
            if setting_str == values[i]:
                self._combo_res.current(i)
                break
        else:
            self._combo_res.current(0)
            self._set_selected_resolution(0)


    def _set_combo_rot_values(self):
        values = ['None', '90 degrees Clock Wise', '180 degrees Rotation', '90 degrees Counter Clock Wise']
        self._combo_rot.configure(values=values)
        
    
    def _set_combo_fli_values(self):
        pass


    def _combo_dev_on_selected(self, e):
        self._settings['camera_mode'] = e.widget.get()
        self._set_combo_res_values()


    def _combo_res_on_selected(self, e):
        self._set_selected_resolution(e.widget.current())
        
    
    def _set_selected_resolution(self, index):
        self._settings['cap_settings'] = {
                'cap_mode' : self._resolutions[index][0],
                'cap_width' : int(self._resolutions[index][1]),
                'cap_height' : int(self._resolutions[index][2]),
                'cap_fps' : float(self._resolutions[index][3])
            }
        
        
    def _combo_rot_on_selected(self, e):
        pass
    
    
    def _combo_fli_on_selected(self, e):
        pass
        
        
    def _save(self):
        self._settings['canvas_settings'] = {
            'canvas_width' : self._canvas_width_var.get(),
            'canvas_height' : self._canvas_height_var.get(),
            'update_interval' : self._canvas_fps_var.get()
        }
        self._settings['gst_str'] = gst_builder.get_gst(self._settings)
        ju.save(self._settings)
        self._label_sav.configure(text="Save OK")
        self.master.after(2000, lambda: self._label_sav.configure(text=""))


if __name__ == "__main__":
    window = tk.Tk()
    app = ConfigWindow(master=window)
    app.mainloop()