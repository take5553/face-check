import cv2
import os
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import ttk
import json_util as ju


class RegisteredListWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._settings = ju.load()
        s = ttk.Style()
        s.configure('TButton', font=("", 20))
        s.configure('TLabel', font=("", 20))
        self._registered_dir = self._settings['save_settings']['main_dir']
        if self._registered_dir[-1] != '/':
            self._registered_dir += '/'
        self._registered_dir += self._settings['save_settings']['onepic_dir']
        if self._registered_dir[-1] != '/':
            self._registered_dir += '/'
        if self._settings['fullscreen'] == True:
            self.master.attributes('-zoomed', '1')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.title("Registered List")
        
        self._canvas_width = self._settings['canvas_settings']['canvas_width']
        self._canvas_height = self._settings['canvas_settings']['canvas_height']
        self._delay = self._settings['canvas_settings']['update_interval']
        
        self._create_widgets()
        self._set_list()
        
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)


    def _create_widgets(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20
        
        # Canvas
        self._canvas1 = tk.Canvas(self, width = self._canvas_width, height = self._canvas_height)
        self._canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E))
        
        # Others'
        self._frame_others = ttk.Frame(self)
        self._frame_others.grid(column=1, row=0, padx=padx, pady=pady, sticky=(tk.W, tk.E))
        
        # List
        self._frame_list = ttk.Frame(self._frame_others)
        self._frame_list.grid(column=0, row=0, sticky=(tk.W, tk.E))
        self._label_list = ttk.Label(self._frame_list, text='Registered Pics')
        self._label_list.grid(column=0, row=0, columnspan=2, sticky=tk.W)
        self._listbox_list = tk.Listbox(self._frame_list, height=10, font=('', 20))
        self._listbox_list.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self._scrollbar_list = ttk.Scrollbar(self._frame_list, orient=tk.VERTICAL, command=self._listbox_list.yview)
        self._listbox_list['yscrollcommand'] = self._scrollbar_list.set
        self._scrollbar_list.grid(column=1, row=1, sticky=(tk.N, tk.S))

        # Delete Button
        self._button_delete = ttk.Button(self._frame_others, text='Delete Picture', command=self._delete_pic)
        self._button_delete.grid(column=0, row=1, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        # Close Button
        self._button_close = ttk.Button(self, text='Close', command=self._close)
        self._button_close.grid(column=0, row=1, columnspan=2, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self._frame_others.columnconfigure(0, weight=1)
        self._frame_list.columnconfigure(0, weight=1)
        
        self._listbox_list.bind('<<ListboxSelect>>', self._update)
        
        
    def _set_list(self):
        files = sorted(os.listdir(self._registered_dir))
        self._file_list = [os.path.join(self._registered_dir, f) for f in files if os.path.isfile(os.path.join(self._registered_dir, f))]
        names = [f[:-8] for f in files if os.path.isfile(os.path.join(self._registered_dir, f))]
        listitems = tk.StringVar(value=names)
        self._listbox_list.configure(listvariable=listitems)
        
        
    def _delete_pic(self):
        index = self._listbox_list.curselection()
        file_path = os.path.join(self._registered_dir, self._file_list[index[0]])
        ret = tk.messagebox.askyesno('Confirm', 'Delete {} ?'.format(file_path), parent=self.master)
        if ret == True:
            os.remove(file_path)
            self._set_list()
        
        
    def _on_closing(self):
        self.master.destroy()
        
        
    def _close(self):
        self._on_closing()
        
    
    def _update(self, e):
        index = e.widget.curselection()
        frame = cv2.imread(os.path.join(self._registered_dir, self._file_list[index[0]]))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        self._photo = PIL.ImageTk.PhotoImage(image=image)
        self._canvas1.create_image(self._canvas_width / 2, self._canvas_height / 2, image = self._photo, anchor=tk.CENTER)


if __name__ == "__main__":
    window = tk.Tk()
    app = RegisteredListWindow(master=window)
    app.mainloop()