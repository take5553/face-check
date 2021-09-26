import tkinter as tk
from tkinter import ttk
import json_util as ju

class ResultWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._settings = ju.load()
        s = ttk.Style()
        s.configure('TButton', font=("", 20))
        s.configure('TLabel', font=("", 20))
        if self._settings['fullscreen'] == True:
            self.master.attributes('-zoomed', '1')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.title("Result")
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self._create_widgets()
        
    
    def _create_widgets(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20
        
        self._frame_main = ttk.Frame(self)
        self._frame_main.grid(column=0, row=0, padx=padx, pady=pady, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self._frame_result = ttk.Frame(self._frame_main)
        self._frame_result.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._text_result = tk.Text(self._frame_result)
        self._text_result.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._scrollbar_result = ttk.Scrollbar(self._frame_result, orient=tk.VERTICAL, command=self._text_result.yview)
        self._text_result['yscrollcommand'] = self._scrollbar_result.set
        self._scrollbar_result.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        self._frame_filelist = ttk.Frame(self._frame_main)
        self._frame_filelist.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._listbox_filelist = tk.Listbox(self._frame_filelist, font=('', 20))
        self._listbox_filelist.grid(colmun=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._scrollbar_filelist = ttk.Scrollbar(self._frame_filelist, orient=tk.VERTICAL, command=self._listbox_filelist.yview)
        self._listbox_filelist['yscrollcommand'] = self._scrollbar_filelist.set
        self._scrollbar_filelist.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        # Close Button
        self._button_close = ttk.Button(self, text='Close', command=self._close)
        self._button_close.grid(column=0, row=1, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._frame_main.columnconfigure(0, weight=3)
        self._frame_main.columnconfigure(1, weight=1)
        self._frame_main.rowconfigure(0, weight=1)
        self._frame_result.columnconfigure(0, weight=1)
        self._frame_result.columnconfigure(1, minsize=20)
        self._frame_result.rowconfigure(0, weight=1)
        self._frame_filelist.columnconfigure(0, weight=1)
        self._frame_filelist.rowconfigure(0, weight=1)
        
        
    def _on_closing(self):
        self.master.destroy()
        
        
    def _close(self):
        self._on_closing()