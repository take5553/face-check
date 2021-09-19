import cv2
import os
import PIL.Image, PIL.ImageTk
import random
import tkinter as tk
from tkinter import ttk
import json_util as ju
from mycamera import MyCamera

class ImCaptureWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._settings = ju.load()
        self._camera = MyCamera(width=self._settings['canvas_settings']['canvas_width'], height=self._settings['canvas_settings']['canvas_height'])
        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.title("Capture")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self._canvas_width = self._settings['canvas_settings']['canvas_width']
        self._canvas_height = self._settings['canvas_settings']['canvas_height']
        self._delay = self._settings['canvas_settings']['update_interval']

        self._create_widgets()
        
        self._cap_im_fl = False
        self._abspath = self._settings['save_dir']
        if self._settings['save_dir'][-1] != '/':
            self._abspath += '/'
        self._file_ext = ".jpg"
        self._image_index = 0

        self._camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._update()
        

    def _create_widgets(self):

        # Canvas
        self._canvas1 = tk.Canvas(self, width = self._canvas_width, height = self._canvas_height)
        self._canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E))

        # Button Frame
        self._frame1 = ttk.Frame(self)
        self._frame1.grid(column=0, row=1, sticky=(tk.W, tk.E))

        # One Image Button
        self._button_image = ttk.Button(self._frame1, text="Take a pic", command=self._one_capture)
        self._button_image.grid(column=0, row=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Save Settings
        self._frame_name = ttk.Frame(self._frame1)
        self._frame_name.grid(column=0, row=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        self._label_name = ttk.Label(self._frame_name, text='Data Name')
        self._label_name.grid(column=0, row=0)
        self._entry_name = ttk.Entry(self._frame_name)
        self._entry_name.grid(column=1, row=0, sticky=(tk.W, tk.E))

        self._frame1.columnconfigure(0, weight=1)
        self._frame1.rowconfigure(0, weight=1)
        self._frame_name.columnconfigure(0, weight=1)
        self._frame_name.columnconfigure(1, weight=1)
        
        self._data_name = tk.StringVar()
        self._entry_name.configure(textvariable=self._data_name)
        

    def _get_index(self):
        os.makedirs(self._abspath + self._im_dir, exist_ok=True)
        files = os.listdir(self._abspath + self._im_dir)
        files_file = [f for f in files if os.path.isfile(os.path.join(self._abspath + self._im_dir, f))]
        if len(files_file) > 0:
            for f in files_file:
                if (int(f[len(self._file_prefix):len(self._file_prefix) + 4]) > self._image_index):
                    self._image_index = int(f[len(self._file_prefix):len(self._file_prefix) + 4]) + 1
        else:
            self._image_index = 0
        
        
    def _one_capture(self):
        self._cap_im_fl = True
        self._im_dir = self._settings['save_dir_onepic']
        if self._settings['save_dir_onepic'][-1] != '/':
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


    def _update(self):
        frame = self._camera.value
        if self._cap_im_fl == True:
            cv2.imwrite('{}{}{:04}{}'.format(self._abspath + self._im_dir, self._file_prefix, self._image_index, self._file_ext), frame)
            self._image_index += 1
            self._cap_im_fl = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self._photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self._canvas1.create_image(self._canvas_width / 2, self._canvas_height / 2, image = self._photo, anchor=tk.CENTER)
        self.master.after(self._delay, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = ImCaptureWindow(master=window)
    app.mainloop()
    