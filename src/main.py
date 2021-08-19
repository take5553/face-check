import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from capture_window import CaptureWindow
from mycamera import MJPGCamera

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.captureWindow = None
        self.create_widgets()

        self.cap_device = 1
        self.cap_width = 1280
        self.cap_height = 720
        self.delay = 30

        self.camera = MJPGCamera(capture_device=self.cap_device, capture_width=self.cap_width, capture_height=self.cap_height, width=self.cap_width, height=self.cap_height)

    def create_widgets(self):

        #Capture Window Button
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        self.button1 = ttk.Button(self.frame1, text="Capture", command=self.ShowCapture)
        self.button1.grid()

    def ShowCapture(self):
        if self.captureWindow == None or not self.captureWindow.winfo_exists():
            self.captureWindow = tk.Toplevel()
            self.capture = CaptureWindow(master=self.captureWindow, camera=self.camera, cap_device=self.cap_device, cap_width=self.cap_width, cap_height=self.cap_height, delay=self.delay)
            
if __name__ == "__main__":
    window = tk.Tk()
    app = Application(master=window)
    app.mainloop()