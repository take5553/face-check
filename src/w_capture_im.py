#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

import cv2
import os
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import random
import re
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from facenet_pytorch import MTCNN
import torch
from mycamera import MyCamera
from facecheck import FaceCheck
from w_base import BaseWindow

class ImCaptureWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)
        self._camera = MyCamera(width=self.settings.canvas.width, height=self.settings.canvas.height)
        self.master.title("Capture")

        self._create_widgets()
        
        self._cap_im_fl = False
        self._abspath = self.settings.save_dir.main_dir
        self._file_ext = ".jpg"
        self._checklist_filename = 'checklist.txt'
        self._image_index = 0
        self._fc = FaceCheck()
        dummy = self._camera.read()
        dummy = cv2.cvtColor(dummy, cv2.COLOR_BGR2RGB)
        self._fc.setup_network(dummy_im=dummy, dataset_setup=False)
        self._show_detection = False
        self._added_fl = False

        self._camera.running = True
        self._update()
        

    def _create_widgets(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20
        fontsize = self.settings.window.fontsize

        # Canvas
        self._canvas1 = tk.Canvas(self._frame_main, width = self.settings.canvas.width, height = self.settings.canvas.height)
        self._canvas1.grid(column=0, row=0, sticky=tk.NSEW)

        # Button Frame
        self._frame1 = ttk.Frame(self._frame_main)
        self._frame1.grid(column=2, row=0, sticky=tk.NSEW)
        
        # One Image Button
        self._button_image = ttk.Button(self._frame1, text="Take a pic", command=self._one_capture)
        self._button_image.grid(column=0, row=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=tk.EW)
        self._button_recog_frame = ttk.Button(self._frame1, text='Detection ON', command=self._toggle_detection)
        self._button_recog_frame.grid(column=2, row=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=tk.EW)
        
        # Save Settings
        self._frame_name = ttk.Frame(self._frame1)
        self._frame_name.grid(column=0, row=1, columnspan=3, padx=padx, pady=pady, sticky=tk.EW)
        self._label_name = ttk.Label(self._frame_name, text='Data\nName')
        self._label_name.grid(column=0, row=0)
        self._entry_name = ttk.Entry(self._frame_name, font=("", fontsize))
        self._entry_name.grid(column=1, row=0, padx=padx, sticky=tk.EW)
        
        # Save Info
        self._frame_info = ttk.Frame(self._frame1)
        self._frame_info.grid(column=0, row=2, columnspan=3, padx=padx, pady=pady, sticky=tk.NSEW)
        self._label_sav_info = ttk.Label(self._frame_info, text='Saved as')
        self._label_sav_info.grid(column=0, row=0, sticky=tk.W)
        self._label_sav_path = ttk.Label(self._frame_info)
        self._label_sav_path.grid(column=0, row=1, sticky=tk.EW)

        self._frame_main.columnconfigure(1, minsize=30)
        self._frame_main.columnconfigure(2, weight=1)
        self._frame_main.rowconfigure(0, weight=1)
        self._frame1.columnconfigure(0, weight=1)
        self._frame1.columnconfigure(1, minsize=20)
        self._frame1.columnconfigure(2, weight=1)
        for i in range(3):
            self._frame1.rowconfigure(i, weight=1)
        self._frame_name.columnconfigure(1, weight=1)
        self._frame_info.columnconfigure(0, weight=1)
        
        # Bind
        self._data_name = tk.StringVar()
        self._entry_name.configure(textvariable=self._data_name)
        

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
        self._im_dir = self.settings.save_dir.onepic_dir
        if self._data_name.get() == '':
            self._file_prefix = 'noname'
        else:
            self._file_prefix = self._data_name.get()
        self._image_index = 0
        self._get_index()


    def _close(self):
        if os.path.exists(os.path.join(self.settings.save_dir.main_dir, self._checklist_filename)) and self._added_fl:
            ret = tk.messagebox.askyesno('Confirm', 'Do you want to delete "{}" to update the list?'.format(self._checklist_filename), parent=self.master)
            if ret == True:
                os.remove(os.path.join(self.settings.save_dir.main_dir, self._checklist_filename))
        self._camera.running = False
        self._camera.cap.release()
        self.master.destroy()


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
            self._added_fl = True
            self._label_sav_path.configure(text=file_path)
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
        self.master.after(self.settings.canvas.update_interval, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = ImCaptureWindow(master=window)
    app.mainloop()
    