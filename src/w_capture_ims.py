import cv2
import os
import PIL.Image, PIL.ImageTk
import random
import tkinter as tk
from tkinter import ttk
from mycamera import MyCamera
from w_base import BaseWindow

class ImsCaptureWindow(BaseWindow):
    def __init__(self, master=None):
        super().__init__(master)        
        self._camera = MyCamera(width=self.settings.canvas.width, height=self.settings.canvas.height)
        self.master.title("Capture")

        self._create_widgets()
        
        self._abspath = self.settings.save_dir.main_dir
        self._file_ext = ".jpg"
        self._image_index = [0, 0, 0]
        self._total_im_count = 0
        self._save_dir_order = []
        
        self._cap_ims_fl = False

        self._camera.running = True
        self._update()
        

    def _create_widgets(self):
        
        padx = 20
        pady = 10
        ipadx = 30
        ipady = 20

        # Canvas
        self._canvas1 = tk.Canvas(self._frame_main, width = self.settings.canvas.width, height = self.settings.canvas.height)
        self._canvas1.grid(column=0, row=0, sticky=tk.NSEW)

        # Others Frame
        self._frame1 = ttk.Frame(self._frame_main)
        self._frame1.grid(column=1, row=0, sticky=tk.NSEW)

        # Images Button
        self._button_images = ttk.Button(self._frame1, text="Take Continous images", command=self._switch_capture_fl)
        self._button_images.grid(column=0, row=0, columnspan=2, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=(tk.W, tk.E))
        
        # Save Settings
        self._frame_name = ttk.Frame(self._frame1)
        self._frame_name.grid(column=0, row=1, pady=pady, sticky=tk.NSEW)
        self._label_name = ttk.Label(self._frame_name, text='Data Name')
        self._label_name.grid(column=0, row=0, padx=10, pady=10)
        self._entry_name = ttk.Entry(self._frame_name, width=1, font=("", 20))
        self._entry_name.grid(column=1, row=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        self._label_speed = ttk.Label(self._frame_name, text='Save Speed')
        self._label_speed.grid(column=0, row=1, padx=10)
        self._frame_speed = ttk.Frame(self._frame_name)
        self._frame_speed.grid(column=1, row=1, padx=10, pady=15, sticky=tk.W)
        self._label_speed_despription = ttk.Label(self._frame_speed, text='1 save per ')
        self._label_speed_despription.grid(column=0, row=0, columnspan=2, sticky=tk.W)
        self._entry_speed = ttk.Entry(self._frame_speed, width=5, font=("", 20))
        self._entry_speed.grid(column=0, row=1)
        self._label_speed_despription2 = ttk.Label(self._frame_speed, text='frame(s)')
        self._label_speed_despription2.grid(column=1, row=1)
        self._label_pic_count = ttk.Label(self._frame_name, text='Capture Limit')
        self._label_pic_count.grid(column=0, row=2, padx=10)
        self._frame_pic_count = ttk.Frame(self._frame_name)
        self._frame_pic_count.grid(column=1, row=2, padx=10, pady=15, sticky=tk.W)
        self._label_pic_count_pre = ttk.Label(self._frame_pic_count, text='Up to')
        self._label_pic_count_pre.grid(column=0, row=0, columnspan=2, sticky=tk.W)
        self._entry_pic_count = ttk.Entry(self._frame_pic_count, width=5, font=("", 20))
        self._entry_pic_count.grid(column=0, row=1)
        self._label_pic_count_sur = ttk.Label(self._frame_pic_count, text='pics')
        self._label_pic_count_sur.grid(column=1, row=1)
        
        # Save State
        self._frame_save_state = ttk.Frame(self._frame1, borderwidth=1, relief='solid')
        self._frame_save_state.grid(column=1, row=1, padx=padx, pady=pady, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._label_save_state = ttk.Label(self._frame_save_state, text='Save Info', anchor='center')
        self._label_save_state.grid(column=0, row=0, columnspan=2, padx=padx, sticky=(tk.W, tk.E))
        self._label_save_description = ttk.Label(self._frame_save_state, text='Total : ')
        self._label_save_description.grid(column=0, row=1, padx=10)
        self._label_save_count = ttk.Label(self._frame_save_state)
        self._label_save_count.grid(column=1, row=1, sticky=tk.W)
        self._label_sub_count = []
        self._label_train_description = ttk.Label(self._frame_save_state, text='Train : ')
        self._label_train_description.grid(column=0, row=2, padx=10)
        self._label_sub_count += [ttk.Label(self._frame_save_state)]
        self._label_sub_count[0].grid(column=1, row=2, sticky=tk.W)
        self._label_valid_description = ttk.Label(self._frame_save_state, text='Valid : ')
        self._label_valid_description.grid(column=0, row=3, padx=10)
        self._label_sub_count += [ttk.Label(self._frame_save_state)]
        self._label_sub_count[1].grid(column=1, row=3, sticky=tk.W)
        self._label_test_description = ttk.Label(self._frame_save_state, text='Test : ')
        self._label_test_description.grid(column=0, row=4, padx=10)
        self._label_sub_count += [ttk.Label(self._frame_save_state)]
        self._label_sub_count[2].grid(column=1, row=4, sticky=tk.W)

        self._frame_main.columnconfigure(1, weight=1)
        self._frame_main.rowconfigure(0, weight=1)
        self._frame1.columnconfigure(1, weight=1)
        self._frame1.rowconfigure(1, weight=1)
        self._frame_save_state.columnconfigure(1, weight=1)
        for i in range(3):
            self._frame_name.rowconfigure(i, weight=1)
        for i in range(5):
            self._frame_save_state.rowconfigure(i, weight=1)
        
        self._data_name = tk.StringVar()
        self._entry_name.configure(textvariable=self._data_name)
        self._shutter_speed = tk.IntVar(value=1)
        self._entry_speed.configure(textvariable=self._shutter_speed)
        self._pic_count = tk.IntVar()
        self._entry_pic_count.configure(textvariable=self._pic_count)
        

    def _get_index(self):
        for i in range(3):
            os.makedirs(self._abspath + self._im_dir + self._datasets_dir[i], exist_ok=True)
            files = os.listdir(self._abspath + self._im_dir + self._datasets_dir[i])
            files_file = [f for f in files if os.path.isfile(os.path.join(self._abspath + self._im_dir + self._datasets_dir[i], f))]
            if len(files_file) > 0:
                for f in files_file:
                    if (int(f[len(self._file_prefix[i]):len(self._file_prefix[i]) + 4]) > self._image_index[i]):
                        self._image_index[i] = int(f[len(self._file_prefix[i]):len(self._file_prefix[i]) + 4]) + 1
            else:
                self._image_index[i] = 0
        self._total_im_count = sum(self._image_index)


    def _switch_capture_fl(self):
        self._cap_ims_fl = not self._cap_ims_fl
        if self._cap_ims_fl == True:
            self._button_images.configure(text="Stop")
            self._file_prefix = ('train', 'valid', 'test')
            self._datasets_dir = ('train/', 'valid/', 'test/')
            if self._data_name.get() == '':
                self._im_dir = 'Data1/'
            else:
                self._im_dir = self._data_name.get()
            if self._im_dir[-1] != '/':
                self._im_dir += '/'
            self._set_save_dir_order()
            self._get_index()
            self._timing = 0
            self._shutter_timing = self._shutter_speed.get()
            self._current_im_count = 0
            self._current_im_count_lim = self._pic_count.get()
            for i in range(3):
                self._label_sub_count[i].configure(text=self._image_index[i])
            self._label_save_count.configure(text=self._total_im_count)
        else:
            self._button_images.configure(text="Continous images")


    def _close(self):
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
        if (self._cap_ims_fl == True) and (self._timing == self._shutter_timing):
            self._timing = 0
            self._total_im_count += 1
            self._current_im_count += 1
            self._label_save_count.configure(text=self._total_im_count)
            index = self._total_im_count % 10
            if index == 0:
                self._save_dir_order = []
                self._set_save_dir_order()
            cv2.imwrite('{}{}{:04}{}'.format(self._abspath + self._im_dir + self._datasets_dir[self._save_dir_order[index]], self._file_prefix[self._save_dir_order[index]], self._image_index[self._save_dir_order[index]], self._file_ext), frame)
            self._image_index[self._save_dir_order[index]] += 1
            self._label_sub_count[self._save_dir_order[index]].configure(text=self._image_index[self._save_dir_order[index]])
            if self._current_im_count == self._current_im_count_lim:
                self._switch_capture_fl()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self._photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self._canvas1.create_image(self._canvas1.winfo_width() / 2, self._canvas1.winfo_height() / 2, image = self._photo, anchor=tk.CENTER)
        self.master.after(self.settings.canvas.update_interval, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = ImsCaptureWindow(master=window)
    app.mainloop()
    