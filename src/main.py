import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from w_capture import CaptureWindow
from w_config import ConfigWindow
from mycamera import MyCamera


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._capture_window = None
        self._config_window = None
        self._create_widgets()

        self._camera_mode = 'csi'
        self._cap_width = 600
        self._cap_height = 860
        self._delay = 15

        self._camera = MyCamera(camera_mode=self._camera_mode, capture_width=self._cap_width, capture_height=self._cap_height, width=self._cap_width, height=self._cap_height)

    def _create_widgets(self):

        #Capture Window Button
        self._frame1 = ttk.Frame(self)
        self._frame1.grid(column=0, row=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        self._button1 = ttk.Button(self._frame1, text="Capture", command=self._show_capture)
        self._button1.grid()

        #Config Window Button
        self._frame2 = ttk.Frame(self)
        self._frame2.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=10, pady=10)
        self._button2 = ttk.Button(self._frame2, text="Config", command=self._show_config)
        self._button2.grid()

    def _show_capture(self):
        if self._capture_window == None or not self._capture_window.winfo_exists():
            self._capture_window = tk.Toplevel()
            self._capture = CaptureWindow(master=self._capture_window, camera=self._camera, cap_width=self._cap_width, cap_height=self._cap_height, delay=self._delay)
    
    def _show_config(self):
        if self._config_window == None or not self._config_window.winfo_exists():
            self._config_window = tk.Toplevel()
            self._config = ConfigWindow(master=self._config_window, camera_mode=self._camera_mode)
            
if __name__ == "__main__":
    window = tk.Tk()
    app = Application(master=window)
    app.mainloop()