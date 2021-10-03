import tkinter as tk
from tkinter import ttk
import re
import device_check as dc
import gst_builder
from w_base import BaseWindow


class ConfigWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Config')
        
        self._create_widgets()
        self._set_combo_dev_values()
        self._set_combo_res_values()
        self._set_combo_rot_values()


    def _create_widgets(self):
        
        padx = 20
        pady = 30
        ipadx = 30
        ipady = 40
        fontfamily = ''
        fontsize = self.settings.window.fontsize
        
        self.option_add("*TCombobox*Listbox.Font", (fontfamily, fontsize))
        s = ttk.Style()
        s.configure('TNotebook.Tab', font=(fontfamily, fontsize))
        
        self._notebook_options = ttk.Notebook(self._frame_main)
        self._notebook_options.grid(column=0, row=0, sticky=tk.NSEW)
        
        
        # Save Button
        
        self._frame_button = ttk.Frame(self._frame_main)
        self._frame_button.grid(column=3, row=0, sticky=tk.NSEW)
        self._button_sav = ttk.Button(self._frame_button, text="Save", command=self._save)
        self._button_sav.grid(column=0, row=0, ipadx=ipadx, ipady=ipady)
        self._label_savestate = ttk.Label(self._frame_button)
        self._label_savestate.grid(column=0, row=1, pady=pady)
        
        
        # Capture Settings
        
        self._frame_capture = tk.Frame(self._notebook_options, borderwidth=1, relief='solid')
        self._notebook_options.add(self._frame_capture, text='Capture', sticky=tk.NSEW)
        self._frame_capture_inner = ttk.Frame(self._frame_capture)
        self._frame_capture_inner.grid(column=0, row=0, sticky=tk.NSEW)

        row = 0
        
        column = 0
        self._label_dev = ttk.Label(self._frame_capture_inner, text="Device")
        self._label_dev.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._combo_dev = ttk.Combobox(self._frame_capture_inner, state="readonly", font=(fontfamily, fontsize))
        self._combo_dev.bind("<<ComboboxSelected>>", self._combo_dev_on_selected)
        self._combo_dev.grid(column=column, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady)
        row += 1
        
        column = 0
        self._label_res = ttk.Label(self._frame_capture_inner, text="Resolution")
        self._label_res.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._combo_res = ttk.Combobox(self._frame_capture_inner, width=30, state="readonly", font=(fontfamily, fontsize))
        self._combo_res.bind("<<ComboboxSelected>>", self._combo_res_on_selected)
        self._combo_res.grid(column=column, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady)
        row += 1
        
        column = 0
        self._label_rot = ttk.Label(self._frame_capture_inner, text="Rotation")
        self._label_rot.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._combo_rot = ttk.Combobox(self._frame_capture_inner, state="readonly", font=(fontfamily, fontsize))
        self._combo_rot.bind("<<ComboboxSelected>>", self._combo_rot_on_selected)
        self._combo_rot.grid(column=column, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady)
        row += 1
        
        # Canvas Settings
        
        self._frame_canvas = ttk.Frame(self._notebook_options, borderwidth=1, relief='solid')
        self._notebook_options.add(self._frame_canvas, text="Canvas", sticky=tk.NSEW)
        self._frame_canvas_inner = ttk.Frame(self._frame_canvas)
        self._frame_canvas_inner.grid(column=0, row=0, sticky=tk.NSEW)
        
        row = 0
        
        column = 0
        self._label_can_wxh = ttk.Label(self._frame_canvas_inner, text="Width x Height")
        self._label_can_wxh.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._frame_can_wxh = ttk.Frame(self._frame_canvas_inner)
        self._frame_can_wxh.grid(column=column, row=row,sticky=tk.W, padx=padx, pady=pady)
        # -----------
        self._entry_can_width = ttk.Entry(self._frame_can_wxh, width=6, font=(fontfamily, fontsize))
        self._entry_can_width.grid(column=0, row=0)
        self._label_can_mul = ttk.Label(self._frame_can_wxh, text=' x ')
        self._label_can_mul.grid(column=1, row=0)
        self._entry_can_height = ttk.Entry(self._frame_can_wxh, width=6, font=(fontfamily, fontsize))
        self._entry_can_height.grid(column=2, row=0)
        # -----------
        row += 1
        
        column = 0
        self._label_can_fps = ttk.Label(self._frame_canvas_inner, text="Update Interval")
        self._label_can_fps.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._frame_can_fps = ttk.Frame(self._frame_canvas_inner)
        self._frame_can_fps.grid(column=column, row=row, sticky=tk.W, padx=padx, pady=pady)
        # ----------
        self._entry_can_fps = ttk.Entry(self._frame_can_fps, width=4, font=(fontfamily, fontsize))
        self._entry_can_fps.grid(column=0, row=0)
        self._label_can_fpsunit = ttk.Label(self._frame_can_fps, text="ms")
        self._label_can_fpsunit.grid(column=1, row=0)
        # ----------
        row += 1
        
        # Save Settings
        
        self._frame_save = ttk.Frame(self._notebook_options, borderwidth=1, relief='solid')
        self._notebook_options.add(self._frame_save, text="Save Settings", sticky=tk.NSEW)
        self._frame_save_inner = ttk.Frame(self._frame_save)
        self._frame_save_inner.grid(column=0, row=0, sticky=tk.NSEW)
        
        row = 0
        
        column = 0
        self._label_sav_dir = ttk.Label(self._frame_save_inner, text="Save\nDirectory")
        self._label_sav_dir.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._entry_sav_dir = ttk.Entry(self._frame_save_inner, font=(fontfamily, fontsize))
        self._entry_sav_dir.grid(column=column, row=row, sticky=tk.EW, padx=padx, pady=pady)
        row += 1
        
        column = 0
        self._label_sav_onedir = ttk.Label(self._frame_save_inner, text="One Pic\nSub Directory")
        self._label_sav_onedir.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._frame_sav_onedir = ttk.Frame(self._frame_save_inner)
        self._frame_sav_onedir.grid(column=column, row=row, sticky=tk.EW, padx=padx, pady=pady)
        # ----------
        self._label_sav_onedir_pre = ttk.Label(self._frame_sav_onedir, text='(Save Directory)/')
        self._label_sav_onedir_pre.grid(column=0, row=0)
        self._entry_sav_onedir = ttk.Entry(self._frame_sav_onedir, font=(fontfamily, fontsize))
        self._entry_sav_onedir.grid(column=1, row=0, sticky=tk.EW)
        # ----------
        row += 1
        
        column = 0
        self._label_sav_result = ttk.Label(self._frame_save_inner, text="Result Save\nDirectory")
        self._label_sav_result.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._entry_sav_result = ttk.Entry(self._frame_save_inner, font=(fontfamily, fontsize))
        self._entry_sav_result.grid(column=column, row=row, sticky=tk.EW, padx=padx, pady=pady)
        row += 1
        
        # Recognition Settings
        
        self._frame_recog = ttk.Frame(self._notebook_options, borderwidth=1, relief='solid')
        self._notebook_options.add(self._frame_recog, text='Recognition', sticky=tk.NSEW)
        self._frame_recog_inner = ttk.Frame(self._frame_recog)
        self._frame_recog_inner.grid(column=0, row=0, sticky=tk.NSEW)
        
        row = 0
        
        column = 0
        self._label_conf_sound = ttk.Label(self._frame_recog_inner, text="Confirmation\nSound")
        self._label_conf_sound.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._frame_sound = ttk.Frame(self._frame_recog_inner)
        self._frame_sound.grid(column=column, row=row, sticky=tk.EW, padx=padx, pady=pady)
        #----------
        self._label_sound_desc = ttk.Label(self._frame_sound, text="(Save Directory)/")
        self._label_sound_desc.grid(column=0, row=0)
        self._entry_conf_sound = ttk.Entry(self._frame_sound, font=(fontfamily, fontsize))
        self._entry_conf_sound.grid(column=1, row=0, sticky=tk.EW)
        #----------
        row += 1
        
        # Window Settings
        
        self._frame_window = ttk.Frame(self._notebook_options, borderwidth=1, relief='solid')
        self._notebook_options.add(self._frame_window, text='Window Settings', sticky=tk.NSEW)
        self._frame_window_inner = ttk.Frame(self._frame_window)
        self._frame_window_inner.grid(column=0, row=0, sticky=tk.NSEW)
        
        row = 0
        
        column = 0
        self._label_win_full = ttk.Label(self._frame_window_inner, text="Fullscreen")
        self._label_win_full.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._checkbutton_win_full = ttk.Checkbutton(self._frame_window_inner)
        self._checkbutton_win_full.grid(column=column, row=row, sticky=tk.W, padx=padx, pady=pady)
        row += 1
        
        column = 0
        self._label_win_fontsize = ttk.Label(self._frame_window_inner, text="Font Size")
        self._label_win_fontsize.grid(column=column, row=row, padx=padx, pady=pady)
        column += 1
        self._entry_win_fontsize = ttk.Entry(self._frame_window_inner, width=4, font=(fontfamily, fontsize))
        self._entry_win_fontsize.grid(column=column, row=row, sticky=tk.W, padx=padx, pady=pady)
        row +=1

        self._frame_main.columnconfigure(0, weight=1)
        self._frame_main.columnconfigure(2, minsize=40)
        self._frame_main.rowconfigure(0, weight=1)
        
        self._frame_capture.columnconfigure(0, weight=1)
        self._frame_capture.rowconfigure(0, weight=1)
        self._frame_capture_inner.columnconfigure(1, weight=1)
        self._frame_save.columnconfigure(0, weight=1)
        self._frame_save.rowconfigure(0, weight=1)
        self._frame_save_inner.columnconfigure(1, weight=1)
        self._frame_sav_onedir.columnconfigure(1, weight=1)
        self._frame_canvas.columnconfigure(0, weight=1)
        self._frame_canvas.rowconfigure(0, weight=1)
        self._frame_canvas_inner.columnconfigure(1, weight=1)
        self._frame_recog.columnconfigure(0, weight=1)
        self._frame_recog.rowconfigure(0, weight=1)
        self._frame_recog_inner.columnconfigure(1, weight=1)
        self._frame_sound.columnconfigure(1, weight=1)
        self._frame_window.columnconfigure(0, weight=1)
        self._frame_window.rowconfigure(0, weight=1)
        self._frame_window_inner.columnconfigure(1, weight=1)
        
        # Bind Variables
        vcmd = (self.register(lambda target: target.isdecimal() or len(target) == 0), '%P')
        self._canvas_width_var = tk.IntVar(value=self.settings.canvas.width)
        self._entry_can_width.configure(textvariable=self._canvas_width_var, validate='key', validatecommand=vcmd)
        self._canvas_height_var = tk.IntVar(value=self.settings.canvas.height)
        self._entry_can_height.configure(textvariable=self._canvas_height_var, validate='key', validatecommand=vcmd)
        self._canvas_fps_var = tk.IntVar(value=self.settings.canvas.update_interval)
        self._entry_can_fps.configure(textvariable=self._canvas_fps_var, validate='key', validatecommand=vcmd)
        self._sav_dir = tk.StringVar(value=self.settings.save_dir.main_dir)
        self._entry_sav_dir.configure(textvariable=self._sav_dir)
        self._sav_onedir = tk.StringVar(value=self.settings.save_dir.onepic_dir)
        self._entry_sav_onedir.configure(textvariable=self._sav_onedir)
        self._sav_result = tk.StringVar(value=self.settings.save_dir.result_save_dir)
        self._entry_sav_result.configure(textvariable=self._sav_result)
        self._win_full = tk.BooleanVar(value=self.settings.window.fullscreen)
        self._checkbutton_win_full.configure(variable=self._win_full)
        self._conf_sound = tk.StringVar(value=self.settings.recognition.confirmation_sound)
        self._entry_conf_sound.configure(textvariable=self._conf_sound)
        self._win_fontsize = tk.IntVar(value=self.settings.window.fontsize)
        self._entry_win_fontsize.configure(textvariable=self._win_fontsize, validate='key', validatecommand=vcmd)

        
    def _set_combo_dev_values(self):
        result = dc.get_device_list()
        if result == '':
            return
        device_list = result.split()
        self._combo_dev.configure(values=device_list)
        for i in range(len(device_list)):
            device_id, connection_method = device_list[i].split(':')
            if self.settings.camera.device_id == device_id and self.settings.camera.connection_method == connection_method:
                self._combo_dev.current(i)
                break
        else:
            self._combo_dev.current(0)


    def _set_combo_res_values(self):
        if self._combo_dev.get() == '':
            return
        values = []
        self._resolutions = []
        device_id = self._combo_dev.get().split(':')[0]
        formats = dc.get_formats(device_id)
        for format_ in formats:
            for resolution in format_.resolutions:
                values += ['{} : {}x{} ({} fps)'.format(format_.name, resolution[0], resolution[1], resolution[2])]
                self._resolutions += [(format_.name, resolution[0], resolution[1], resolution[2])]
        self._combo_res.configure(values=values)
        
        setting_str = '{} : {}x{} ({:.3f} fps)'.format(self.settings.capture.mode, 
                                                       self.settings.capture.width, 
                                                       self.settings.capture.height, 
                                                       self.settings.capture.fps)
        for i in range(len(values)):
            if setting_str == values[i]:
                self._combo_res.current(i)
                break
        else:
            self._combo_res.current(0)
            self._set_selected_resolution(0)


    def _set_combo_rot_values(self):
        values = ['None', '90 degrees counter clock wise', '180 degrees rotation', '90 degrees clock wise', 'Horizontal flip', 'Upper right diagonal flip', 'Vertical flip', 'Upper left diagonal flip']
        self._combo_rot.configure(values=values)
        self._combo_rot.current(self.settings.capture.rotation)

    def _combo_dev_on_selected(self, e):
        device_id, connection_method = e.widget.get().split(':')
        self.settings.camera.device_id = device_id
        self.settings.camera.connection_method = connection_method
        self._set_combo_res_values()


    def _combo_res_on_selected(self, e):
        self._set_selected_resolution(e.widget.current())
        
    
    def _set_selected_resolution(self, index):
        self.settings.capture.mode = self._resolutions[index][0]
        self.settings.capture.width = int(self._resolutions[index][1])
        self.settings.capture.height = int(self._resolutions[index][2])
        self.settings.capture.fps = float(self._resolutions[index][3])
        
        
    def _combo_rot_on_selected(self, e):
        self.settings.capture.rotation = e.widget.current()
        
        
    def _save(self):
        self.settings.canvas.width = self._canvas_width_var.get()
        self.settings.canvas.height = self._canvas_height_var.get()
        self.settings.canvas.update_interval = self._canvas_fps_var.get()
        self.settings.save_dir.main_dir = self._sav_dir.get()
        self.settings.save_dir.onepic_dir = self._sav_onedir.get()
        self.settings.save_dir.result_save_dir = self._sav_result.get()
        self.settings.recognition.confirmation_sound = self._conf_sound.get()
        self.settings.window.fullscreen = self._win_full.get()
        self.settings.window.fontsize = self._win_fontsize.get()
        
        self.settings.save()
        self._label_savestate.configure(text="Save OK")
        self.master.after(2000, lambda: self._label_savestate.configure(text=""))


if __name__ == "__main__":
    window = tk.Tk()
    app = ConfigWindow(master=window)
    app.mainloop()