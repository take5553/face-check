import cv2
import os
import PIL.Image, PIL.ImageTk
import random
import tkinter as tk
from tkinter import ttk
import json_util as ju
from mycamera import MyCamera

class CaptureWindow(ttk.Frame):
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
        self._file_prefix = "capture"
        self._file_ext = ".jpg"
        self._datasets_dir = ('train/', 'valid/', 'test/')
        self._image_index = [0, 0, 0]
        self._total_im_count = 0
        self._save_dir_order = []
        self._set_save_dir_order()
        
        self._cap_ims_fl = False

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

        # Images Button
        self._button_images = ttk.Button(self._frame1, text="Continous images", command=self._capture_images)
        self._button_images.grid(column=1, row=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Save Settings
        self._frame_name = ttk.Frame(self._frame1)
        self._frame_name.grid(column=0, row=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        self._label_name = ttk.Label(self._frame_name, text='Data Name')
        self._label_name.grid(column=0, row=0)
        self._entry_name = ttk.Entry(self._frame_name)
        self._entry_name.grid(column=1, row=0, sticky=(tk.W, tk.E))
        self._label_speed = ttk.Label(self._frame_name, text='Save speed')
        self._label_speed.grid(column=0, row=1)
        self._frame_speed = ttk.Frame(self._frame_name)
        self._frame_speed.grid(column=1, row=1)
        self._label_speed_despription = ttk.Label(self._frame_speed, text='1 shoot per ')
        self._label_speed_despription.grid(column=0, row=0)
        self._entry_speed = ttk.Entry(self._frame_speed)
        self._entry_speed.grid(column=1, row=0, sticky=(tk.W, tk.E))
        self._label_speed_despription2 = ttk.Label(self._frame_speed, text='frame(s)')
        self._label_speed_despription2.grid(column=2, row=0)
        
        # Save State
        self._frame_save_state = ttk.Frame(self._frame1)
        self._frame_save_state.grid(column=1, row=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        self._label_save_description = ttk.Label(self._frame_save_state, text='Taken Pics : ')
        self._label_save_description.grid(column=0, row=0)
        self._label_save_count = ttk.Label(self._frame_save_state)
        self._label_save_count.grid(column=1, row=0)
        self._label_sub_count = []
        self._label_train_description = ttk.Label(self._frame_save_state, text='Train : ')
        self._label_train_description.grid(column=0, row=1, pady=2)
        self._label_sub_count += [ttk.Label(self._frame_save_state)]
        self._label_sub_count[0].grid(column=1, row=1, pady=2)
        self._label_valid_description = ttk.Label(self._frame_save_state, text='Valid : ')
        self._label_valid_description.grid(column=0, row=2, pady=2)
        self._label_sub_count += [ttk.Label(self._frame_save_state)]
        self._label_sub_count[1].grid(column=1, row=2, pady=2)
        self._label_test_description = ttk.Label(self._frame_save_state, text='Test : ')
        self._label_test_description.grid(column=0, row=3, pady=2)
        self._label_sub_count += [ttk.Label(self._frame_save_state)]
        self._label_sub_count[2].grid(column=1, row=3, pady=2)

        self._frame1.columnconfigure(0, weight=1)
        self._frame1.columnconfigure(1, weight=1)
        self._frame1.rowconfigure(0, weight=1)
        self._frame_name.columnconfigure(0, weight=1)
        self._frame_name.columnconfigure(1, weight=1)
        
        self._data_name = tk.StringVar()
        self._entry_name.configure(textvariable=self._data_name)
        self._shutter_speed = tk.IntVar(value=1)
        self._entry_speed.configure(textvariable=self._shutter_speed)
        

    def _get_index(self):
        if self._data_name.get() == '':
            self._im_dir = 'Data1/'
        else:
            self._im_dir = self._data_name.get()
        if self._im_dir[-1] != '/':
            self._im_dir += '/'
        for i in range(3):
            os.makedirs(self._abspath + self._im_dir + self._datasets_dir[i], exist_ok=True)
            files = os.listdir(self._abspath + self._im_dir + self._datasets_dir[i])
            files_file = [f for f in files if os.path.isfile(os.path.join(self._abspath + self._im_dir + self._datasets_dir[i], f))]
            if len(files_file) > 0:
                for f in files_file:
                    if (int(f[len(self._file_prefix):len(self._file_prefix) + 4]) > self._image_index[i]):
                        self._image_index[i] = int(f[len(self._file_prefix):len(self._file_prefix) + 4]) + 1
            else:
                self._image_index[i] = 0
        self._total_im_count = sum(self._image_index)
        
        
    def _one_capture(self):
        if self._cap_ims_fl == False:
            self._cap_im_fl = True
            self._timing = 0
            self._shutter_timing = 0
            self._get_index()


    def _capture_images(self):
        if self._cap_im_fl == True:
            self._cap_im_fl = False
        self._cap_ims_fl = not self._cap_ims_fl
        if self._cap_ims_fl == True:
            self._button_images.configure(text="Stop")
            self._button_image.configure(state="disable")
            self._get_index()
            self._timing = 0
            self._shutter_timing = self._shutter_speed.get()
        else:
            self._button_images.configure(text="Continous images")
            self._button_image.configure(state="enable")


    def _on_closing(self):
        self._camera.running = False
        self._camera.cap.release()
        self.master.destroy()
        
        
    def _set_save_dir_order(self):
        r1 = random.randrange(10)
        r2 = random.randrange(10)
        while r1 == r2:
            r2 = random.randrange(10)
        for i in range(10):
            if i == r1:
                self._save_dir_order += [1]
            elif i == r2:
                self._save_dir_order += [2]
            else:
                self._save_dir_order += [0]


    def _update(self):
        frame = self._camera.value
        if self._cap_ims_fl == True:
            self._timing += 1
        if (self._cap_im_fl == True) or ((self._cap_ims_fl == True) and (self._timing == self._shutter_timing)):
            self._timing = 0
            self._total_im_count += 1
            self._label_save_count.configure(text=self._total_im_count)
            index = self._total_im_count % 10
            if index == 0:
                self._save_dir_order = []
                self._set_save_dir_order()
            cv2.imwrite('{}{}{:04}{}'.format(self._abspath + self._im_dir + self._datasets_dir[self._save_dir_order[index]], self._file_prefix, self._image_index[self._save_dir_order[index]], self._file_ext), frame)
            self._image_index[self._save_dir_order[index]] += 1
            self._label_sub_count[self._save_dir_order[index]].configure(text=self._image_index[self._save_dir_order[index]])
            if (self._cap_im_fl == True):
                self._cap_im_fl = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self._photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self._canvas1.create_image(0, 0, image = self._photo, anchor = tk.NW)
        self.master.after(self._delay, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = CaptureWindow(master=window)
    app.mainloop()
    