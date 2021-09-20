import cv2
import os
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import random
import re
import subprocess
import tkinter as tk
from tkinter import ttk
from facenet_pytorch import MTCNN
import torch
import json_util as ju
from mycamera import MyCamera
from facecheck import FaceCheck

nn_device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(min_face_size=120, device=nn_device)

class ImCaptureWindow(ttk.Frame):
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
        self.master.title("Capture")

        self._canvas_width = self._settings['canvas_settings']['canvas_width']
        self._canvas_height = self._settings['canvas_settings']['canvas_height']
        self._delay = self._settings['canvas_settings']['update_interval']

        self._create_widgets()
        
        self._cap_im_fl = False
        self._abspath = self._settings['save_settings']['main_dir']
        if self._settings['save_settings']['main_dir'][-1] != '/':
            self._abspath += '/'
        self._file_ext = ".jpg"
        self._image_index = 0
        self._fc = FaceCheck()
        dummy = self._camera.read()
        dummy = cv2.cvtColor(dummy, cv2.COLOR_BGR2RGB)
        self._fc.setup_network(dummy_im=dummy, dataset_setup=False)
        self._show_detection = False

        self._camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._update()
        

    def _create_widgets(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20

        # Canvas
        self._canvas1 = tk.Canvas(self, width = self._canvas_width, height = self._canvas_height)
        self._canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E))

        # Button Frame
        self._frame1 = ttk.Frame(self)
        self._frame1.grid(column=0, row=1, sticky=(tk.W, tk.E))
        
        # One Image Button
        self._button_image = ttk.Button(self._frame1, text="Take a pic", command=self._one_capture)
        self._button_image.grid(column=0, row=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        # Save Settings
        self._frame_name = ttk.Frame(self._frame1)
        self._frame_name.grid(column=0, row=1, padx=padx, pady=pady, sticky=(tk.W, tk.E))
        
        self._label_name = ttk.Label(self._frame_name, text='Data Name')
        self._label_name.grid(column=0, row=0)
        self._entry_name = ttk.Entry(self._frame_name, font=("", 20))
        self._entry_name.grid(column=1, row=0, sticky=(tk.W, tk.E))
        self._button_recog_frame = ttk.Button(self._frame_name, text='Detection ON', command=self._toggle_detection)
        self._button_recog_frame.grid(column=2, row=0, padx=padx, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        # Save Info
        self._label_sav_info = ttk.Label(self._frame1, text='Saved as ')
        self._label_sav_info.grid(column=0, row=2, padx=padx, pady=pady, sticky=(tk.W, tk.E))
        
        # Close
        self._button_close = ttk.Button(self._frame1, text="Close", command=self._close)
        self._button_close.grid(column=0, row=3, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._frame1.columnconfigure(0, weight=1)
        self._frame_name.columnconfigure(0, weight=1)
        self._frame_name.columnconfigure(1, weight=1)
        self._frame_name.columnconfigure(2, weight=1)
        
        # Bind
        self._data_name = tk.StringVar()
        self._entry_name.configure(textvariable=self._data_name)
        # self._entry_name.bind("<FocusIn>", self._call_keyboard)
        # self._entry_name.bind("<FocusOut>", self._close_keyboard)
        

    def _get_index(self):
        os.makedirs(self._abspath + self._im_dir, exist_ok=True)
        files = os.listdir(self._abspath + self._im_dir)
        files_file = [f for f in files if os.path.isfile(os.path.join(self._abspath + self._im_dir, f))]
        if len(files_file) > 0:
            for f in files_file:
                match = re.match('(.{{{}}})(\d{{4}})\.jpg'.format(len(self._file_prefix)), f)
                if (match != None) and (match.group(1) == self._file_prefix):
                    if (int(match.group(2)) >= self._image_index):
                        self._image_index = int(match.group(2)) + 1
        else:
            self._image_index = 0
        
        
    def _one_capture(self):
        self._cap_im_fl = True
        self._im_dir = self._settings['save_settings']['onepic_dir']
        if self._settings['save_settings']['onepic_dir'][-1] != '/':
            self._im_dir += '/'
        if self._data_name.get() == '':
            self._file_prefix = 'noname'
        else:
            self._file_prefix = self._data_name.get()
        self._get_index()


    def _on_closing(self):
        self._camera.running = False
        self._camera.cap.release()
        self.master.destroy()
        
        
    def _close(self):
        self._on_closing()
        
        
    # def _call_keyboard(self, event):
    #     subprocess.Popen("onboard")
        
        
    # def _close_keyboard(self, event):
    #     subprocess.Popen(["pkill", "onboard"])


    def _toggle_detection(self):
        self._show_detection = not self._show_detection
        if self._show_detection == True:
            self._button_recog_frame.configure(text='Detection OFF')
        else:
            self._button_recog_frame.configure(text='Detection ON')
    

    def _update(self):
        frame = self._camera.value
        if self._cap_im_fl == True:
            file_path = '{}{}{:04}{}'.format(self._abspath + self._im_dir, self._file_prefix, self._image_index, self._file_ext)
            cv2.imwrite(file_path, frame)
            self._label_sav_info.configure(text='Saved as {}'.format(file_path))
            self._image_index += 1
            self._cap_im_fl = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        if self._show_detection:
            boxes, _ = self._fc.detect(image)
            if not (boxes is None):
                draw = PIL.ImageDraw.Draw(image)
                for box in boxes:
                    draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
        self._photo = PIL.ImageTk.PhotoImage(image=image)
        self._canvas1.create_image(self._canvas1.winfo_width() / 2, self._canvas1.winfo_height() / 2, image = self._photo, anchor=tk.CENTER)
        self.master.after(self._delay, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = ImCaptureWindow(master=window)
    app.mainloop()
    