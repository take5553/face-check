import cv2
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import os
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import ttk
import json_util as ju
from mycamera import MyCamera
from facecheck import FaceCheck

class RecogWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._settings = ju.load()
        self._camera = MyCamera(width=self._settings['canvas_settings']['canvas_width'], height=self._settings['canvas_settings']['canvas_height'])
        if self._settings['fullscreen'] == True:
            w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
            self.master.geometry('{}x{}+0+0'.format(w, h))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.title("Recognition")
        
        self._canvas_width = self._settings['canvas_settings']['canvas_width']
        self._canvas_height = self._settings['canvas_settings']['canvas_height']
        self._delay = self._settings['canvas_settings']['update_interval']
        
        self._create_widgets()
        
        dummy = self._camera.read()
        dummy = cv2.cvtColor(dummy, cv2.COLOR_BGR2RGB)
        self._fc = FaceCheck()
        self._fc.setup_network(dummy)
        
        self._detecting = False
        
        self._camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._update()


    def _create_widgets(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20
        
        s = ttk.Style()
        s.configure('Inference.TLabel', font=("", 40, 'bold'), foreground='red')

        # Canvas
        self._canvas1 = tk.Canvas(self, width = self._canvas_width, height = self._canvas_height)
        self._canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E))
        
        # Detection
        self._frame_infer = ttk.Frame(self)
        self._frame_infer.grid(column=0, row=1, padx=padx, pady=pady, sticky=(tk.W, tk.E))
        
        self._label_infer_pre = ttk.Label(self._frame_infer, text='You are :')
        self._label_infer_pre.grid(column=0, row=0)
        self._frame_infer_answer = ttk.Frame(self._frame_infer)
        self._frame_infer_answer.grid(column=1, row=0, sticky=(tk.W, tk.E))
        
        self._label_infer = ttk.Label(self._frame_infer_answer, text='aaaaaa', style='Inference.TLabel')
        self._label_infer.grid(column=0, row=0)
        self._label_infer_prob = ttk.Label(self._frame_infer_answer, text='0.999999')
        self._label_infer_prob.grid(column=0, row=1)
        
        # Start Button
        self._button_start = ttk.Button(self, text='Start', command=self._start_detection)
        self._button_start.grid(column=0, row=2, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        # Close Button
        self._button_close = ttk.Button(self, text='Close', command=self._close)
        self._button_close.grid(column=0, row=3, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, minsize=20)
        self._frame_infer.columnconfigure(1, weight=1)
        self._frame_infer_answer.columnconfigure(0, weight=1)

        
    def _on_closing(self):
        self._camera.running = False
        self._camera.cap.release()
        self.master.destroy()
        
        
    def _close(self):
        self._on_closing()
        
        
    def _start_detection(self):
        self._detecting = not self._detecting
        if self._detecting == True:
            self._button_start.configure(text='Stop')
        else:
            self._button_start.configure(text='Start')
            self._label_infer.configure(text='')
            self._label_infer_prob.configure(text='')
        
    
    def _update(self):
        frame = self._camera.value
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        if self._detecting == True:
            name, prob = self._fc.identify(frame)            
            self._label_infer.configure(text=name)
            percentage = Decimal(str(prob * 100)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
            self._label_infer_prob.configure(text='( {} % )'.format(percentage))
        self._photo = PIL.ImageTk.PhotoImage(image=image)
        self._canvas1.create_image(self._canvas1.winfo_width() / 2, self._canvas1.winfo_height() / 2, image = self._photo, anchor=tk.CENTER)
        self.master.after(self._delay, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = RecogWindow(master=window)
    app.mainloop()