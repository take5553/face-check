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

        self._create_widgets()
        
        self.capIm = False
        self.abspath = os.path.dirname(os.path.abspath(__file__)) + "/data/"
        self.imdir = "one_shot/"
        self.fileprefix = "capture"
        self.fileext = ".jpg"
        self.image_index = 0
        self._get_index()
        
        self.capIms = False

        if self.camera == None:
            self.camera = USBCamera(capture_device=self.cap_device, capture_width=self.cap_width, capture_height=self.cap_height, width=self.cap_width, height=self.cap_height)
        self.camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._update()

    def _create_widgets(self):

        #Canvas
        self.canvas1 = tk.Canvas(self, width = self.cap_width, height = self.cap_height)
        self.canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E))

        #Button Frame
        self.frame1 = ttk.Frame(self)
        self.frame1.grid(column=0, row=1, sticky=(tk.W, tk.E))

        #One Image Button
        self.button1 = ttk.Button(self.frame1, text="Take a pic", command=self._one_capture)
        self.button1.grid(column=0, row=0, padx=60, pady=40, ipady=20, sticky=(tk.W, tk.E))

        #Images Button
        self.button2 = ttk.Button(self.frame1, text="Continous images", command=self._capture_images)
        self.button2.grid(column=1, row=0, padx=60, pady=40, ipady=20, sticky=(tk.W, tk.E))

        self.frame1.columnconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.rowconfigure(0, weight=1)

    def _get_index(self):
        files = os.listdir(self.abspath + self.imdir)
        files_file = [f for f in files if os.path.isfile(os.path.join(self.abspath + self.imdir, f))]
        if len(files_file) > 0:
            for f in files_file:
                if (int(f[len(self.fileprefix):len(self.fileprefix) + 4]) > self.image_index):
                    self.image_index = int(f[len(self.fileprefix):len(self.fileprefix) + 4]) + 1
        else:
            self.image_index = 0
        
    def _one_capture(self):
        if self.capIms == False:
            self.capIm = True
            self.imdir = 'one_shot/'
            self._get_index()

    def _capture_images(self):
        if self.capIm == True:
            self.capIm = False
        self.capIms = not self.capIms
        if self.capIms == True:
            self.imdir = 'Takeshi/train/'
            self._get_index()

    def _on_closing(self):
        self.camera.running = False
        self.master.destroy()

    def _update(self):
        frame = self.camera.value
        if (self.capIm == True) or (self.capIms == True):
            cv2.imwrite('{}{}{:04}{}'.format(self.abspath + self.imdir, self.fileprefix, self.image_index, self.fileext), frame)
            self.image_index += 1
            if (self.capIm == True):
                self.capIm = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas1.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.master.after(self.delay, self._update)

if __name__ == "__main__":
    window = tk.Tk()
    app = CaptureWindow(master=window)
    app.mainloop()
    