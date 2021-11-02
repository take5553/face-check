#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

from collections import deque, Counter
import cv2
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import os
import PIL.Image, PIL.ImageTk
from playsound import playsound
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from checklist import CheckList
from mycamera import MyCamera
from facecheck import FaceCheck
from w_base import BaseWindow

class RecogWindow(BaseWindow):
    def __init__(self, master=None, auto_start=False):
        super().__init__(master)
        self._camera = MyCamera(width=self.settings.canvas.width, height=self.settings.canvas.height)
        self.master.title("Recognition")
        
        self._create_widgets()
        
        files = sorted(os.listdir(self.settings.save_dir.onepic_dir_fullpath))
        for f in files:
            if os.path.isfile(os.path.join(self.settings.save_dir.onepic_dir_fullpath, f)):
                dummy = cv2.imread(os.path.join(self.settings.save_dir.onepic_dir_fullpath, f))
                break
        else:
            print('using camera picture for pre-recognition')
            dummy = self._camera.read()
        dummy = cv2.cvtColor(dummy, cv2.COLOR_BGR2RGB)
        dummy = PIL.Image.fromarray(dummy)
        self._fc = FaceCheck()
        self._fc.setup_network(dummy_im=dummy, pre_recog=dummy)
        self._cl = CheckList()
        self._queue = deque([], 10)
        self._identified_pause_fl = False
        self._detecting = 0
        if len(self._cl.get_checked_list()) > 0:
            for item in self._cl.get_checked_list():
                self._listbox_checked.insert(tk.END, item)
            self._detecting = 2
        self._switch_detection_state()
        if self.settings.recognition.confirmation_sound != '':
            self._sound_thread = threading.Thread(target=self._play_sound)
        else:
            self._sound_thread = None
        
        self._camera.running = True
        self._update()
        if auto_start:
            self.master.after(500, self._start_detection)


    def _create_widgets(self):
        
        padx = 30
        pady = 20
        ipadx = 30
        ipady = 20
        fontsize = self.settings.window.fontsize
        
        s = ttk.Style()
        s.configure('Inference.TLabel', font=("", 36, 'bold'), foreground='red')
        s.configure('Failed.TLabel', font=("", 36, 'bold'), foreground='blue')
        s.configure('Already.TLabel', font=("", 36, 'bold'), foreground='green')

        # Canvas
        self._canvas1 = tk.Canvas(self._frame_main, width=self.settings.canvas.width, height=self.settings.canvas.height)
        self._canvas1.grid(column=0, row=0, sticky=tk.NSEW)
        
        # Others
        self._frame_others = ttk.Frame(self._frame_main)
        self._frame_others.grid(column=2, row=0, sticky=tk.NSEW)
        
        # Detection
        self._frame_infer = ttk.Frame(self._frame_others)
        self._frame_infer.grid(column=0, row=1, pady=pady, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self._frame_infer_once = ttk.Frame(self._frame_infer)
        self._frame_infer_once.grid(column=0, row=0, sticky=(tk.W, tk.E))
        
        self._label_infer_pre = ttk.Label(self._frame_infer_once, text='You are :')
        self._label_infer_pre.grid(column=0, row=0, sticky=tk.W)
        self._frame_infer_answer = ttk.Frame(self._frame_infer_once)
        self._frame_infer_answer.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self._label_infer = ttk.Label(self._frame_infer_answer, text='', style='Inference.TLabel')
        self._label_infer.grid(column=0, row=0)
        self._label_infer_prob = ttk.Label(self._frame_infer_answer, text='')
        self._label_infer_prob.grid(column=0, row=1)
        
        self._frame_infer_conf = ttk.Frame(self._frame_infer)
        self._frame_infer_conf.grid(column=0, row=2, sticky=(tk.W, tk.E))
        self._label_id = ttk.Label(self._frame_infer_conf, text='', style='Inference.TLabel')
        self._label_id.grid(column=0, row=0)
        self._label_id_name = ttk.Label(self._frame_infer_conf, text='', style='Inference.TLabel')
        self._label_id_name.grid(column=0, row=1)
        
        # Checked List
        self._frame_checked = ttk.Frame(self._frame_others)
        self._frame_checked.grid(column=1, row=1, padx=padx, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self._frame_checked_inner = ttk.Frame(self._frame_checked)
        self._frame_checked_inner.grid(column=0, row=0, sticky=tk.NSEW)
        self._listbox_checked = tk.Listbox(self._frame_checked_inner, width=12, font=('', fontsize))
        self._listbox_checked.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self._scrollbar_checked = ttk.Scrollbar(self._frame_checked_inner, orient=tk.VERTICAL, command=self._listbox_checked.yview)
        self._listbox_checked['yscrollcommand'] = self._scrollbar_checked.set
        self._scrollbar_checked.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self._button_delete = ttk.Button(self._frame_checked, text='Delete', command=self._delete_confirmation)
        self._button_delete.grid(column=0, row=2, ipadx=ipadx, ipady=5, sticky=tk.EW)
        
        # Button frame
        self._frame_buttons = ttk.Frame(self._frame_others)
        self._frame_buttons.grid(column=0, row=2, columnspan=2, sticky=tk.EW)
        self._button_start = ttk.Button(self._frame_buttons, command=self._start_detection)
        self._button_start.grid(column=0, row=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=tk.EW)
        self._button_finish = ttk.Button(self._frame_buttons, text='Finish Check', command=self._finish_checking)
        self._button_finish.grid(column=1, row=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=tk.EW)
        
        self._frame_main.columnconfigure(1, minsize=30)
        self._frame_main.columnconfigure(2, weight=1, minsize=400)
        self._frame_main.rowconfigure(0, weight=1)
        self._frame_others.columnconfigure(0, weight=1, minsize=250)
        self._frame_others.rowconfigure(0, minsize=50)
        self._frame_others.rowconfigure(1, weight=1)
        self._frame_infer.columnconfigure(0, weight=1)
        self._frame_infer.rowconfigure(0, weight=1)
        self._frame_infer.rowconfigure(1, minsize=50)
        self._frame_infer.rowconfigure(2, weight=1)
        self._frame_infer_once.columnconfigure(0, weight=1)
        self._frame_infer_conf.columnconfigure(0, weight=1)
        self._frame_infer_answer.columnconfigure(0, weight=1)
        self._frame_checked.columnconfigure(0, weight=1)
        self._frame_checked.rowconfigure(0, weight=1)
        self._frame_checked_inner.columnconfigure(0, weight=1)
        self._frame_checked_inner.rowconfigure(0, weight=1)
        self._frame_checked_inner.rowconfigure(1, minsize=20)
        self._frame_buttons.columnconfigure(0, weight=1)
        self._frame_buttons.columnconfigure(1, weight=1)

        
    def _close(self):
        self._camera.running = False
        self._camera.cap.release()
        self._sound_thread = None
        self.master.destroy()
        
        
    def _switch_detection_state(self):
        # 0: not started  1: detecting  2: paused
        if self._detecting == 0:
            self._button_start.configure(text='Start')
            self._button_finish.configure(state=tk.DISABLED)
            self._label_infer.configure(text='')
            self._label_infer_prob.configure(text='')
        elif self._detecting == 1:
            self._button_start.configure(text='Pause')
            self._button_finish.configure(state=tk.NORMAL)
        elif self._detecting == 2:
            self._button_start.configure(text='Restart')
            self._button_finish.configure(state=tk.NORMAL)
            self._label_infer.configure(text='')
            self._label_infer_prob.configure(text='')
            
        
    def _start_detection(self):
        if self._detecting == 0 or self._detecting == 2:
            self._detecting = 1
        elif self._detecting == 1:
            self._detecting = 2
            if self._identified_pause_fl == False:
                self._label_id.configure(text='')
                self._label_id_name.configure(text='')
        self._switch_detection_state()
            
            
    def _finish_checking(self):
        self._detecting = 0
        self._switch_detection_state()
        self._label_id.configure(text='')
        self._label_id_name.configure(text='')
        file_path = self._cl.finish_checking()
        tk.messagebox.showinfo('Finish Checking', 'Result Saved : {}'.format(file_path), parent=self.master)
        self._listbox_checked.delete(0, tk.END)
        
        
    def _delete_confirmation(self):
        index = self._listbox_checked.curselection()
        if len(index) == 0:
            return
        name = self._listbox_checked.get(index[0])
        if isinstance(name, tuple):
            name = name[0]
        answer = tk.messagebox.askokcancel('Delete', 'Make sure you are deleting\n\n    {}\n'.format(name), parent=self.master)
        if answer:
            self._listbox_checked.delete(index[0])
            self._cl.delete_from_checked_list(index[0])
        
    
    def _update(self):
        frame = self._camera.value
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        if self._detecting == 1:
            name, prob = self._fc.identify(frame, 0.6)
            self._label_infer.configure(text=name)
            percentage = Decimal(str(prob * 100)).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
            self._label_infer_prob.configure(text='( {} % )'.format(percentage))
            if self._identified_pause_fl == False:
                if self._cl.has_name(name) and not self._cl.already_checked(name):
                    self._queue.append(name)
                    self._label_id.configure(text='')
                    self._label_id_name.configure(text='')
                    if len(self._queue) == 10:
                        counter = Counter(self._queue)
                        mc = counter.most_common()[0]
                        if mc[1] >= 9 and mc[0] != '':
                            # identified
                            self._label_id.configure(text='Confirmed', style='Inference.TLabel')
                            self._label_id_name.configure(text=mc[0], style='Inference.TLabel')
                            self._cl.add_to_checked(mc[0])
                            self._listbox_checked.insert(tk.END, mc[0])
                            self._identified_pause_fl = True
                            if self._sound_thread != None:
                                self._sound_thread.start()
                            self.master.after(5000, self._reset_queue)
                elif not self._cl.has_name(name):
                    if name == '':
                        self._queue.clear()
                        self._label_id.configure(text='')
                        self._label_id_name.configure(text='')
                    else:
                        self._label_id.configure(text='Not on', style='Failed.TLabel')
                        self._label_id_name.configure(text='the list', style='Failed.TLabel')
                else:
                    self._label_id.configure(text='Already', style='Already.TLabel')
                    self._label_id_name.configure(text='confirmed', style='Already.TLabel')
        self._photo = PIL.ImageTk.PhotoImage(image=image)
        self._canvas1.create_image(self._canvas1.winfo_width() / 2, self._canvas1.winfo_height() / 2, image = self._photo, anchor=tk.CENTER)
        self.master.after(self.settings.canvas.update_interval, self._update)
        
        
    def _play_sound(self):
        playsound(self.settings.recognition.confirmation_sound)
        
        
    def _reset_queue(self):
        if self._sound_thread != None:
            self._sound_thread.join()
            self._sound_thread = threading.Thread(target=self._play_sound)
        self._identified_pause_fl = False
        self._queue.clear()
        self._label_id.configure(text='')
        self._label_id_name.configure(text='')


if __name__ == "__main__":
    window = tk.Tk()
    app = RecogWindow(master=window)
    app.mainloop()
