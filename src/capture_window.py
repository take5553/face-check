import tkinter as tk
from tkinter import ttk
from jetcam.usb_camera import USBCamera
import cv2
import PIL.Image, PIL.ImageTk

class CaptureWindow(ttk.Frame):
    def __init__(self, master=None, camera=None, cap_device=0, cap_width=352, cap_height=288, delay=10):
        super().__init__(master)
        self.camera = camera
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.title("Capture")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.cap_device = cap_device
        self.cap_width = cap_width
        self.cap_height = cap_height
        self.delay = delay

        self.create_widgets()

        if self.camera == None:
            self.camera = USBCamera(capture_device=self.cap_device, capture_width=self.cap_width, capture_height=self.cap_height, width=self.cap_width, height=self.cap_height)
        self.camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self.closing_window)
        self.running = True
        self.update()

    def create_widgets(self):

        #Canvas
        self.canvas1 = tk.Canvas(self, width = self.cap_width, height = self.cap_height)
        self.canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        # #Button Frame
        # self.frame1 = ttk.Frame(self)
        # self.frame1.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=10, pady=10)

        # #Capture Button

    def closing_window(self):
        self.camera.running = False
        self.master.destroy()

    def update(self):
        frame = self.camera.value
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas1.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.master.after(self.delay, self.update)


if __name__ == "__main__":
    window = tk.Tk()
    app = CaptureWindow(master=window)
    app.mainloop()
    