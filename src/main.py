import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from w_capture_im import ImCaptureWindow
from w_capture_ims import ImsCaptureWindow
from w_config import ConfigWindow
from w_recog import RecogWindow
import json_util as ju


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._settings = ju.load()
        if self._settings['fullscreen'] == True:
            w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            self.master.geometry('{}x{}+0+0'.format(w, h))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._capture_window = None
        self._config_window = None
        self._camera = None
        self._create_widgets()
        self._set_style()
        

    def _create_widgets(self):
        
        padx = 30
        pady = 30
        ipadx = 30
        ipady = 30
        
        row = 0
        
        #Capture Ims Window Button
        self._button0 = ttk.Button(self, text="Image Capture", command=self._show_capture_im)
        self._button0.grid(column=0, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        row += 1

        #Capture Ims Window Button
        self._button1 = ttk.Button(self, text="Continuous Capture", command=self._show_capture_ims)
        self._button1.grid(column=0, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        row += 1

        #Config Window Button
        self._button2 = ttk.Button(self, text="Config", command=self._show_config)
        self._button2.grid(column=0, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        row += 1
        
        #Recognition Window Button
        self._button3 = ttk.Button(self, text="Recognition", command=self._show_recog)
        self._button3.grid(column=0, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        row += 1
        
        #Close Button
        self._button4 = ttk.Button(self, text='Close', command=self._close)
        self._button4.grid(column=0, row=row, sticky=(tk.W, tk.E), padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        row += 1
        
        self.columnconfigure(0, weight=1)
        for i in range(row):
            self.rowconfigure(i, weight=1)
        
        
    def _set_style(self):
        self._style = ttk.Style()
        self._style.configure('TButton', font=("", 20))
        
        
    def _show_capture_im(self):
        if self._capture_window == None or not self._capture_window.winfo_exists():
            self._capture_window = tk.Toplevel()
            self._capture = ImCaptureWindow(master=self._capture_window)


    def _show_capture_ims(self):
        if self._capture_window == None or not self._capture_window.winfo_exists():
            self._capture_window = tk.Toplevel()
            self._capture = ImsCaptureWindow(master=self._capture_window)


    def _show_config(self):
        if self._config_window == None or not self._config_window.winfo_exists():
            self._config_window = tk.Toplevel()
            self._config = ConfigWindow(master=self._config_window)
            
            
    def _show_recog(self):
        if self._capture_window == None or not self._capture_window.winfo_exists():
            self._capture_window = tk.Toplevel()
            self._capture = RecogWindow(master=self._capture_window)
            
            
    def _close(self):
        self.master.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = Application(master=window)
    app.mainloop()