import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from w_capture_im import ImCaptureWindow
from w_capture_ims import ImsCaptureWindow
from w_config import ConfigWindow
from w_recog import RecogWindow
from w_registered_list import RegisteredListWindow
from w_result import ResultWindow
from w_base import BaseWindow


class Application(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self._capture_window = None
        self._config_window = None
        self._registered_window = None
        self._result_window = None
        self._create_widgets()
        

    def _create_widgets(self):
        
        padx = 0
        pady = 30
        ipadx = 30
        ipady = 50
        
        #Capture Im Window Button
        self._button_im = ttk.Button(self._frame_main, text="Image Capture", command=self._show_capture_im)
        self._button_im.grid(column=0, row=0, sticky=tk.EW, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

        #Capture Ims Window Button
        self._button_ims = ttk.Button(self._frame_main, text="Continuous Capture", command=self._show_capture_ims)
        self._button_ims.grid(column=2, row=0, sticky=tk.EW, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        
        #Registered Pics List Window Button
        self._button_reg = ttk.Button(self._frame_main, text="Registered Pics", command=self._show_registered_list)
        self._button_reg.grid(column=4, row=0, sticky=tk.EW, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        
        #Recognition Window Button
        self._button_rec = ttk.Button(self._frame_main, text="Recognition", command=self._show_recog)
        self._button_rec.grid(column=0, row=1, sticky=tk.EW, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        
        #Result Window Button
        self._button_res = ttk.Button(self._frame_main, text="Result", command=self._show_result)
        self._button_res.grid(column=2, row=1, sticky=tk.EW, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

        #Config Window Button
        self._button_conf = ttk.Button(self._frame_main, text="Config", command=self._show_config)
        self._button_conf.grid(column=4, row=1, sticky=tk.EW, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

        self._frame_main.columnconfigure(0, weight=1)
        self._frame_main.columnconfigure(1, minsize=40)
        self._frame_main.columnconfigure(2, weight=1)
        self._frame_main.columnconfigure(3, minsize=40)
        self._frame_main.columnconfigure(4, weight=1)
        for i in range(2):
            self._frame_main.rowconfigure(i, weight=1)
        
        
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
            
            
    def _show_registered_list(self):
        if self._registered_window == None or not self._registered_window.winfo_exists():
            self._registered_window = tk.Toplevel()
            self._registered_window = RegisteredListWindow(master=self._registered_window)
            
            
    def _show_result(self):
        if self._result_window == None or not self._result_window.winfo_exists():
            self._result_window = tk.Toplevel()
            self._result_window = ResultWindow(master=self._result_window)


if __name__ == "__main__":
    window = tk.Tk()
    app = Application(master=window)
    app.mainloop()