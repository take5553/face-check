import tkinter as tk
from tkinter import ttk
from jetcam.usb_camera import USBCamera
import cv2
import PIL.Image, PIL.ImageTk
import os

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
        
        self.capIm = False
        self.path = "data/one_shot/"
        self.fileprefix = "capture"
        self.fileext = ".jpg"
        self.image_index = 0
        files = os.listdir(self.path)
        files_file = [f for f in files if os.path.isfile(os.path.join(self.path, f))]
        if len(files_file) > 0:
            for f in files_file:
                if (int(f[len(self.fileprefix):len(self.fileprefix) + 4]) > self.image_index):
                    self.image_index = int(f[len(self.fileprefix):len(self.fileprefix) + 4]) + 1
        
        self.capIms = False

        if self.camera == None:
            self.camera = USBCamera(capture_device=self.cap_device, capture_width=self.cap_width, capture_height=self.cap_height, width=self.cap_width, height=self.cap_height)
        self.camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self.closing_window)
        self.running = True
        self.update()

    def create_widgets(self):

        #Canvas
        self.canvas1 = tk.Canvas(self, width = self.cap_width, height = self.cap_height)
        self.canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E), pady=10)

        #Button Frame
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=1, sticky=(tk.W, tk.E))

        #One Image Button
        self.button1 = ttk.Button(self.frame1, text="Take a pic", command=self.OneCapture)
        self.button1.grid(column=0, row=0, padx=60, pady=40, ipady=20, sticky=(tk.W, tk.E))

        #Images Button
        self.button2 = ttk.Button(self.frame1, text="Continous images", command=self.CaptureImages)
        self.button2.grid(column=1, row=0, padx=60, pady=40, ipady=20, sticky=(tk.W, tk.E))

        self.frame1.columnconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.rowconfigure(0, weight=1)
        
    def OneCapture(self):
        self.capIm = True

    def CaptureImages(self):
        self.capIms = True

    def closing_window(self):
        self.camera.running = False
        self.master.destroy()

    def update(self):
        frame = self.camera.value
        if self.capIm == True:
            cv2.imwrite('{}{}{:04}{}'.format(self.path, self.fileprefix, self.image_index, self.fileext), frame)
            self.image_index += 1
            self.capIm = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas1.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.master.after(self.delay, self.update)


if __name__ == "__main__":
    window = tk.Tk()
    app = CaptureWindow(master=window)
    app.mainloop()
    