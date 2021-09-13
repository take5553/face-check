import cv2
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import tkinter as tk
from tkinter import ttk
import json_util as ju
from mycamera import MyCamera

from facenet_pytorch import MTCNN
import torch

class RecogWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._settings = ju.load()
        self._camera = MyCamera(width=self._settings['canvas_settings']['canvas_width'], height=self._settings['canvas_settings']['canvas_height'])
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.title("Recognition")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self._canvas_width = self._settings['canvas_settings']['canvas_width']
        self._canvas_height = self._settings['canvas_settings']['canvas_height']
        self._delay = self._settings['canvas_settings']['update_interval']
        
        self._create_widgets()
        self._setup_nn_engine()
        
        self._detecting = False
        
        self._camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._update()


    def _create_widgets(self):

        # Canvas
        self._canvas1 = tk.Canvas(self, width = self._canvas_width, height = self._canvas_height)
        self._canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E))
        
        # Button
        self._button_start = ttk.Button(self, text='Start', command=self._start_detection)
        self._button_start.grid(column=0, row=1, sticky=(tk.W, tk.E))
        
    
    def _setup_nn_engine(self):
        print('Initializing start')
        self._nn_device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        print('Running on device: {}'.format(self._nn_device))
        self._mtcnn = MTCNN(keep_all=True, device=self._nn_device)
        print('MTCNN initialized')
        dummy = self._camera.read()
        print('Dummy data captured')
        dummy = cv2.cvtColor(dummy, cv2.COLOR_BGR2RGB)
        self._mtcnn.detect(dummy)
        print('Pre-detection complete')
        
        
    def _on_closing(self):
        self._camera.running = False
        self._camera.cap.release()
        self.master.destroy()
        
        
    def _start_detection(self):
        self._detecting = not self._detecting
        
    
    def _update(self):
        frame = self._camera.value
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        if self._detecting == True:
            boxes, _ = self._mtcnn.detect(image)
            draw = PIL.ImageDraw.Draw(image)
            for box in boxes:
                draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
        self._photo = PIL.ImageTk.PhotoImage(image=image)
        self._canvas1.create_image(0, 0, image = self._photo, anchor = tk.NW)
        self.master.after(self._delay, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = RecogWindow(master=window)
    app.mainloop()