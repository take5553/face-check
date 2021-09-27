import cv2
import os
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import ttk
from w_base import BaseWindow


class RegisteredListWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Registered List")
        
        self._create_widgets()
        self._set_list()


    def _create_widgets(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20
        fontsize = self.settings.window.fontsize
        
        # self._frame_main is defined in BaseWindow
        
        # Canvas
        self._canvas1 = tk.Canvas(self._frame_main, width = self.settings.canvas.width, height = self.settings.canvas.height)
        self._canvas1.grid(column=0, row=0, sticky=tk.NSEW)
        
        # Others'
        self._frame_others = ttk.Frame(self._frame_main)
        self._frame_others.grid(column=2, row=0, sticky=tk.NSEW)
        
        # List
        self._frame_list = ttk.Frame(self._frame_others)
        self._frame_list.grid(column=0, row=0, sticky=tk.NSEW)
        self._label_list = ttk.Label(self._frame_list, text='Registered Pics')
        self._label_list.grid(column=0, row=0, columnspan=2, sticky=tk.W)
        self._listbox_list = tk.Listbox(self._frame_list, font=('', fontsize))
        self._listbox_list.grid(column=0, row=1, sticky=tk.NSEW)
        self._scrollbar_list = ttk.Scrollbar(self._frame_list, orient=tk.VERTICAL, command=self._listbox_list.yview)
        self._listbox_list['yscrollcommand'] = self._scrollbar_list.set
        self._scrollbar_list.grid(column=1, row=1, sticky=tk.NS)

        # Delete Button
        self._button_delete = ttk.Button(self._frame_others, text='Delete Picture', command=self._delete_pic)
        self._button_delete.grid(column=0, row=1, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))

        self._frame_main.columnconfigure(0, weight=2)
        self._frame_main.columnconfigure(1, minsize=20)
        self._frame_main.columnconfigure(2, weight=1, minsize=200)
        self._frame_main.rowconfigure(0, weight=1)
        self._frame_others.columnconfigure(0, weight=1)
        self._frame_others.rowconfigure(0, weight=1)
        self._frame_list.columnconfigure(0, weight=1)
        self._frame_list.rowconfigure(1, weight=1)
        
        self._listbox_list.bind('<<ListboxSelect>>', self._update)
        
        # # for debug
        # self._canvas1.configure(borderwidth=1, relief='solid')
        # self._frame_others.configure(borderwidth=1, relief='solid')
        # self._frame_list.configure(borderwidth=1, relief='solid')
        
        
    def _set_list(self):
        files = sorted(os.listdir(self.settings.save_dir.onepic_dir_fullpath))
        self._file_list = [os.path.join(self.settings.save_dir.onepic_dir_fullpath, f) for f in files if os.path.isfile(os.path.join(self.settings.save_dir.onepic_dir_fullpath, f))]
        names = [f[:-8] for f in files if os.path.isfile(os.path.join(self.settings.save_dir.onepic_dir_fullpath, f))]
        listitems = tk.StringVar(value=names)
        self._listbox_list.configure(listvariable=listitems)
        
        
    def _delete_pic(self):
        index = self._listbox_list.curselection()
        file_path = os.path.join(self.settings.save_dir.onepic_dir_fullpath, self._file_list[index[0]])
        ret = tk.messagebox.askyesno('Confirm', 'Delete {} ?'.format(file_path), parent=self.master)
        if ret == True:
            os.remove(file_path)
            self._set_list()
        
    
    def _update(self, e):
        index = e.widget.curselection()
        frame = cv2.imread(os.path.join(self.settings.save_dir.onepic_dir_fullpath, self._file_list[index[0]]))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        self._photo = PIL.ImageTk.PhotoImage(image=image)
        self._canvas1.create_image(self._canvas1.winfo_width() / 2, self._canvas1.winfo_height() / 2, image = self._photo, anchor=tk.CENTER)


if __name__ == "__main__":
    window = tk.Tk()
    app = RegisteredListWindow(master=window)
    app.mainloop()