#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

import glob
import os
import tkinter as tk
from tkinter import ttk
from w_base import BaseWindow

class ResultCheckWindow(BaseWindow):
    def __init__(self, master=None, file_path=''):
        super().__init__(master)
        self.master.title("Result Check")
        self._file_path = file_path
        if self._file_path == '':
            self._list_path = self.settings.save_dir.result_save_dir_fullpath
            os.makedirs(self._list_path, exist_ok=True)
            self._file_path = self._get_file_path(result_dir=self._list_path)
        
        self._create_widgets()
        self._not_checked = ''
        self._not_registered = ''
        
        if self._file_path != '':
            with open(self._file_path) as f:
                contents = f.read()
            self._not_checked, self._not_registered = self._get_not_checked_and_not_registered_list(contents=contents)
        
        self._text_nchecked.insert('1.0', self._not_checked)
        self._text_nregistered.insert('1.0', self._not_registered)
    
    def _create_widgets(self):

        fontsize = self.settings.window.fontsize
        
        # self._frame_main is defined in BaseWindow
        
        self._label_file_path = ttk.Label(self._frame_main, text=self._file_path)
        self._label_file_path.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        
        self._frame_not_checked = ttk.Frame(self._frame_main)
        self._frame_not_checked.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._label_not_checked = ttk.Label(self._frame_not_checked, text='Not Checked:')
        self._label_not_checked.grid(column=0, row=0, sticky=tk.NSEW)
        self._frame_nchecked_list = ttk.Frame(self._frame_not_checked)
        self._frame_nchecked_list.grid(column=0, row=1, sticky=tk.NSEW)
        self._text_nchecked = tk.Text(self._frame_nchecked_list, font=('', fontsize))
        self._text_nchecked.grid(column=0, row=0, sticky=tk.NSEW)
        self._scrollbar_nchecked = ttk.Scrollbar(self._frame_nchecked_list, orient=tk.VERTICAL, command=self._text_nchecked.yview)
        self._text_nchecked['yscrollcommand'] = self._scrollbar_nchecked.set
        self._scrollbar_nchecked.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        self._frame_not_registered = ttk.Frame(self._frame_main)
        self._frame_not_registered.grid(column=2, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._label_not_registered = ttk.Label(self._frame_not_registered, text='Not Registered:')
        self._label_not_registered.grid(column=0, row=0, sticky=tk.NSEW)
        self._frame_nregistered_list = ttk.Frame(self._frame_not_registered)
        self._frame_nregistered_list.grid(column=0, row=1, sticky=tk.NSEW)
        self._text_nregistered = tk.Text(self._frame_nregistered_list, font=('', fontsize))
        self._text_nregistered.grid(column=0, row=0, sticky=tk.NSEW)
        self._scrollbar_nregistered = ttk.Scrollbar(self._frame_nregistered_list, orient=tk.VERTICAL, command=self._text_nregistered.yview)
        self._text_nregistered['yscrollcommand'] = self._scrollbar_nregistered.set
        self._scrollbar_nregistered.grid(column=1, row=0, sticky=(tk.N, tk.S))
        
        self._frame_main.columnconfigure(0, weight=1)
        self._frame_main.columnconfigure(1, minsize=20)
        self._frame_main.columnconfigure(2, weight=1)
        self._frame_main.rowconfigure(0, minsize=30)
        self._frame_main.rowconfigure(1, weight=1)
        self._frame_not_checked.rowconfigure(0, minsize=30)
        self._frame_not_checked.rowconfigure(1, weight=1)
        self._frame_nchecked_list.rowconfigure(0, weight=1)
        self._frame_nchecked_list.columnconfigure(0, weight=1)
        self._frame_not_registered.rowconfigure(0, minsize=30)
        self._frame_not_registered.rowconfigure(1, weight=1)
        self._frame_nregistered_list.rowconfigure(0, weight=1)
        self._frame_nregistered_list.columnconfigure(0, weight=1)
        
        
    def _get_file_path(self, result_dir=''):
        if result_dir == '':
            return ''
        file_path = glob.glob(result_dir + 'result*.txt')
        if len(file_path) == 0:
            return ''
        file_path.sort()
        return file_path[-1]
    
    
    def _get_not_checked_and_not_registered_list(self, contents=''):
        if contents == '':
            return '', ''
        get_not_checked_fl = False
        not_checked_list = []
        get_not_registered_fl = False
        not_registered_list = []
        lines = contents.splitlines()
        for line in lines:
            if line == '-----not checked-----':
                get_not_checked_fl = True
            elif line == '-----not registered-----':
                get_not_registered_fl = True
            elif len(line) > 0:
                if get_not_registered_fl:
                    not_registered_list.append(line)
                elif get_not_checked_fl:
                    not_checked_list.append(line)
        return '\n'.join(not_checked_list), '\n'.join(not_registered_list)
        

if __name__ == "__main__":
    window = tk.Tk()
    app = ResultCheckWindow(master=window)
    app.mainloop()