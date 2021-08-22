import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from capture_window import CaptureWindow
from mycamera import MyCamera

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._capture_window = None
        self._create_widgets()

        self._cap_width = 540
        self._cap_height = 860
        self._delay = 15

        self.camera = MyCamera(camera_mode='csi', capture_width=self._cap_width, capture_height=self._cap_height, width=self._cap_width, height=self._cap_height)

    def _create_widgets(self):

        #Capture Window Button
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=0, sticky=(tk.W, tk.E), padx=10, pady=10)
        self.button1 = ttk.Button(self.frame1, text="Capture", command=self._show_capture)
        self.button1.grid()

    def _show_capture(self):
        if self._capture_window == None or not self._capture_window.winfo_exists():
            self._capture_window = tk.Toplevel()
            self.capture = CaptureWindow(master=self._capture_window, camera=self.camera, cap_width=self._cap_width, cap_height=self._cap_height, delay=self._delay)
            
if __name__ == "__main__":
    window = tk.Tk()
    app = Application(master=window)
    app.mainloop()