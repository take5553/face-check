#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

import os
import tkinter as tk
from tkinter import ttk
from w_base import BaseWindow

class ResultCheckWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self._result_file_prefix = 'result'
        self._list_path = self.settings.save_dir.result_save_dir_fullpath
        os.makedirs(self._list_path, exist_ok=True)
        self.master.title("Result Check")
        
        self._create_widgets()
        
    
    def _create_widgets(self):

        fontsize = self.settings.window.fontsize
        
        # self._frame_main is defined in BaseWindow
        
        self._frame_not_checked = ttk.Frame(self._frame_main)
        self._frame_not_checked.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._label_not_checked = ttk.Label(self._frame_not_checked, text='Not Checked:')
        self._label_not_checked.grid(column=0, row=0, sticky=tk.NSEW)
        self._frame_nchecked_list = ttk.Frame(self._frame_not_checked)
        self._frame_nchecked_list.grid(column=0, row=1, sticky=tk.NSEW)
        self._listbox_nchecked = tk.Listbox(self._frame_nchecked_list, font=('', fontsize))
        self._listbox_nchecked.grid(column=0, row=0, sticky=tk.NSEW)
        self._scrollbar_nchecked = ttk.Scrollbar(self._frame_nchecked_list, orient=tk.VERTICAL, command=self._listbox_nchecked.yview)
        self._listbox_nchecked['yscrollcommand'] = self._scrollbar_nchecked.set
        self._scrollbar_nchecked.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        self._frame_not_registered = ttk.Frame(self._frame_main)
        self._frame_not_registered.grid(column=2, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._label_not_registered = ttk.Label(self._frame_not_registered, text='Not Registered:')
        self._label_not_registered.grid(column=0, row=0, sticky=tk.NSEW)
        self._frame_nregistered_list = ttk.Frame(self._frame_not_registered)
        self._frame_nregistered_list.grid(column=0, row=1, sticky=tk.NSEW)
        self._listbox_nregistered = tk.Listbox(self._frame_nregistered_list, font=('', fontsize))
        self._listbox_nregistered.grid(column=0, row=0, sticky=tk.NSEW)
        self._scrollbar_nregistered = ttk.Scrollbar(self._frame_nregistered_list, orient=tk.VERTICAL, command=self._listbox_nregistered.yview)
        self._listbox_nregistered['yscrollcommand'] = self._scrollbar_nregistered.set
        self._scrollbar_nregistered.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        self._frame_main.columnconfigure(0, weight=1)
        self._frame_main.columnconfigure(1, minsize=20)
        self._frame_main.columnconfigure(2, weight=1)
        self._frame_main.rowconfigure(0, weight=1)
        self._frame_not_checked.rowconfigure(0, minsize=30)
        self._frame_not_checked.rowconfigure(1, weight=1)
        self._frame_nchecked_list.rowconfigure(0, weight=1)
        self._frame_nchecked_list.columnconfigure(0, weight=1)
        self._frame_not_registered.rowconfigure(0, minsize=30)
        self._frame_not_registered.rowconfigure(1, weight=1)
        self._frame_nregistered_list.rowconfigure(0, weight=1)
        self._frame_nregistered_list.columnconfigure(0, weight=1)

        

if __name__ == "__main__":
    window = tk.Tk()
    app = ResultCheckWindow(master=window)
    app.mainloop()