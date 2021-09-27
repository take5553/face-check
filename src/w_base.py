import tkinter as tk
from tkinter import ttk
from mysettings import MySettings


class BaseWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.settings = MySettings()
        s = ttk.Style()
        s.configure('TButton', font=("", self.settings.window.fontsize))
        s.configure('TLabel', font=("", self.settings.window.fontsize))
        if self.settings.window.fullscreen == True:
            self.master.attributes('-zoomed', '1')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.protocol("WM_DELETE_WINDOW", self._close)
        
        self._create_basic_layout()
        
    
    def _create_basic_layout(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20
        
        self._frame_main = ttk.Frame(self)
        self._frame_main.grid(column=0, row=0, padx=padx, pady=pady, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Close Button
        self._button_close = ttk.Button(self, text='Close', command=self._close)
        self._button_close.grid(column=0, row=1, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        
    def _close(self):
        self.master.destroy()