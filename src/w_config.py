import tkinter as tk
from tkinter import ttk
import device_check as dc
import re


class ConfigWindow(ttk.Frame):
    def __init__(self, master=None, camera_mode=None):
        super().__init__(master)
        self.grid()

        self._camera_mode = camera_mode

        self._create_widgets()
        self._set_combo_values()


    def _create_widgets(self):

        # Resolution Label
        self._frame1 = ttk.Frame(self)
        self._frame1.grid(column=0, row=0, padx=10, pady=10)
        self._label1 = ttk.Label(self._frame1, text="Resolution")
        self._label1.grid()
        
        # Resolution ComboBox
        self._frame2 = ttk.Frame(self)
        self._frame2.grid(column=1, row=0, padx=10, pady=10)
        self._combo1 = ttk.Combobox(self._frame2, state="readonly", width=30)
        self._combo1.bind("<<ComboboxSelected>>", self._combo1_on_selected)
        self._combo1.grid()


    def _set_combo_values(self):
        if self._camera_mode == None:
            return
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
        resolution = self._resolutions[e.widget.current()]
        # TODO: output selected resolution into a file (or something)
        print(resolution)


if __name__ == "__main__":
    window = tk.Tk()
    app = ConfigWindow(master=window, device_id=1)
    app.mainloop()