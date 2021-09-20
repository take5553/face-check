import cv2
import numpy as np
import os
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import tkinter as tk
from tkinter import ttk
import json_util as ju
from mycamera import MyCamera

# from facenet_pytorch import MTCNN, InceptionResnetV1
# import torch

# nn_device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# mtcnn = MTCNN(device=nn_device)
# resnet = InceptionResnetV1(pretrained='vggface2').eval().to(nn_device)

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
        # self._setup_nn_engine()
        
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
        self._label_infer = ttk.Label(self._frame_infer, text='', style='Inference.TLabel')
        self._label_infer.grid(column=1, row=0)
        
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
    
    # def _setup_nn_engine(self):
    #     print('Initializing start')
    #     global nn_device
    #     #self._nn_device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    #     print('Running on device: {}'.format(nn_device))
    #     print('MTCNN initializing')
    #     #self._mtcnn = MTCNN(device=self._nn_device)
    #     global mtcnn
    #     print('MTCNN initialized')
    #     dummy = self._camera.read()
    #     dummy = cv2.cvtColor(dummy, cv2.COLOR_BGR2RGB)
    #     mtcnn.detect(dummy)
    #     print('MTCNN Pre-detection complete')
    #     print('InceptionResnet V1 initializing')
    #     #self._resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self._nn_device)
    #     print('InceptionResnet V1 initialized')
    #     print('Make Dataset')
    #     self._registered = self._make_dataset(os.path.dirname(os.path.abspath(__file__)) + '/data/register/')
    #     print('Made Dataset')
        
        
    # def _get_vec(self, img):
    #     global mtcnn
    #     global resnet
    #     global nn_device
    #     img_cropped = mtcnn(img)
    #     if img_cropped == None:
    #         return None
    #     img_embedding = resnet(img_cropped.unsqueeze(0).to(nn_device))
    #     return img_embedding.squeeze().to('cpu').detach().numpy().copy()
        
    
    # def _make_data(self, file_path):
    #     img = cv2.imread(file_path)
    #     return self._get_vec(img)
    
    
    # def _make_dataset(self, dir_path):
    #     self._file_list = sorted(os.listdir(dir_path))
    #     ps = []
    #     for i in range(len(self._file_list)):
    #         print(dir_path + self._file_list[i])
    #         ps += [self._make_data(dir_path + self._file_list[i])]
    #     q = np.stack(ps)
    #     return q
    
    
    # def _cos_sim_vs2d(self, arr, vec):
    #     den = np.sqrt(np.einsum('ij,ij->i',arr,arr)*np.einsum('j,j',vec,vec))
    #     out = arr.dot(vec) / den
    #     return out
    
        
    def _on_closing(self):
        self._camera.running = False
        self._camera.cap.release()
        self.master.destroy()
        
        
    def _close(self):
        self._on_closing()
        
        
    def _start_detection(self):
        self._detecting = not self._detecting
        
    
    def _update(self):
        frame = self._camera.value
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(frame)
        # if self._detecting == True:
        #     vec = self._get_vec(frame)
        #     if not (vec is None):
        #         result_idx = self._cos_sim_vs2d(self._registered, vec).argmax()
        #         draw = PIL.ImageDraw.Draw(image)
        #         draw.text((0, 0), self._file_list[result_idx])
        self._photo = PIL.ImageTk.PhotoImage(image=image)
        self._canvas1.create_image(self._canvas1.winfo_width() / 2, self._canvas1.winfo_height() / 2, image = self._photo, anchor=tk.CENTER)
        self.master.after(self._delay, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = RecogWindow(master=window)
    app.mainloop()