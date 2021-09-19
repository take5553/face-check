import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from w_capture_im import ImCaptureWindow
from w_capture_ims import ImsCaptureWindow
from w_config import ConfigWindow
from w_recog import RecogWindow


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._capture_window = None
        self._config_window = None
        self._camera = None
        self._create_widgets()
        

    def _create_widgets(self):
        
        #Capture Ims Window Button
        self._frame0 = ttk.Frame(self)
        self._frame0.grid(column=0, row=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        self._button0 = ttk.Button(self._frame0, text="Image Capture", command=self._show_capture_im)
        self._button0.grid()

        #Capture Ims Window Button
        self._frame1 = ttk.Frame(self)
        self._frame1.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=10, pady=10)
        self._button1 = ttk.Button(self._frame1, text="Continuous Capture", command=self._show_capture_ims)
        self._button1.grid()

        #Config Window Button
        self._frame2 = ttk.Frame(self)
        self._frame2.grid(column=0, row=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        self._button2 = ttk.Button(self._frame2, text="Config", command=self._show_config)
        self._button2.grid()
        
        #Recognition Window Button
        self._frame3 = ttk.Frame(self)
        self._frame3.grid(column=0, row=3, sticky=(tk.W, tk.E), padx=10, pady=10)
        self._button3 = ttk.Button(self._frame3, text="Recognition", command=self._show_recog)
        self._button3.grid()
        
        
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


if __name__ == "__main__":
    window = tk.Tk()
    app = Application(master=window)
    app.mainloop()