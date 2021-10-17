#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

import os
import tkinter as tk
from tkinter import ttk
from w_base import BaseWindow

class ResultWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self._result_file_prefix = 'result'
        self._list_path = self.settings.save_dir.result_save_dir_fullpath
        os.makedirs(self._list_path, exist_ok=True)
        self.master.title("Result")
        
        self._create_widgets()
        
        self._set_filelist()
        
    
    def _create_widgets(self):

        fontsize = self.settings.window.fontsize
        
        # self._frame_main is defined in BaseWindow
        
        self._frame_result = ttk.Frame(self._frame_main)
        self._frame_result.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._text_result = tk.Text(self._frame_result, font=("", fontsize))
        self._text_result.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._scrollbar_result = ttk.Scrollbar(self._frame_result, orient=tk.VERTICAL, command=self._text_result.yview)
        self._text_result['yscrollcommand'] = self._scrollbar_result.set
        self._scrollbar_result.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        self._frame_filelist = ttk.Frame(self._frame_main)
        self._frame_filelist.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._listbox_filelist = tk.Listbox(self._frame_filelist, width=len(self._result_file_prefix)+20, font=('', fontsize))
        self._listbox_filelist.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._scrollbar_filelist = ttk.Scrollbar(self._frame_filelist, orient=tk.VERTICAL, command=self._listbox_filelist.yview)
        self._listbox_filelist['yscrollcommand'] = self._scrollbar_filelist.set
        self._scrollbar_filelist.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        self._frame_main.columnconfigure(0, weight=3)
        self._frame_main.columnconfigure(1, weight=1)
        self._frame_main.rowconfigure(0, weight=1)
        self._frame_result.columnconfigure(0, weight=1)
        self._frame_result.columnconfigure(2, minsize=20)
        self._frame_result.rowconfigure(0, weight=1)
        self._frame_filelist.columnconfigure(0, weight=1)
        self._frame_filelist.rowconfigure(0, weight=1)
        
        self._listbox_filelist.bind('<<ListboxSelect>>', self._update_textbox)
        
        
    def _set_filelist(self):
        file_list = [f for f in sorted(os.listdir(self._list_path), reverse=True) if os.path.isfile(os.path.join(self._list_path, f)) \
                and f[:len(self._result_file_prefix)] == self._result_file_prefix]
        self._file_path_list = [os.path.join(self._list_path, f) for f in file_list]
        listitems = tk.StringVar(value=file_list)
        self._listbox_filelist.configure(listvariable=listitems)
        
        
    def _update_textbox(self, e):
        index = e.widget.curselection()
        with open(self._file_path_list[index[0]]) as f:
            content = f.read()
        self._text_result.delete('1.0', 'end')
        self._text_result.insert('1.0', content)
        

if __name__ == "__main__":
    window = tk.Tk()
    app = ResultWindow(master=window)
    app.mainloop()