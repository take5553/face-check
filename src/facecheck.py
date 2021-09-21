import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import json_util as ju


nn_device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(min_face_size=120, device=nn_device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(nn_device)


class FaceCheck():
    def __init__(self):
        self._registered = []
        self._settings = ju.load()
        self._registered_dir = self._settings['save_settings']['main_dir']
        if self._registered_dir[-1] != '/':
            self._registered_dir += '/'
        self._registered_dir += self._settings['save_settings']['onepic_dir']
        if self._registered_dir[-1] != '/':
            self._registered_dir += '/'


    def setup_network(self, dummy_im=None, dataset_setup=True):
        print('FaceCheck initializing...')
        if not (dummy_im is None):
            global mtcnn
            print('Start pre-detection')
            mtcnn.detect(dummy_im)
            print('End pre-detection')
        if dataset_setup:
            print('Start making registered dataset')
            self._registered = self._make_dataset(self._registered_dir)
            print('End making registered dataset')
            print('Dataset shape is ' + str(self._registered.shape))
            
            
    def detect(self, img):
        global mtcnn
        return mtcnn.detect(img)
        
        
    def identify(self, img):
        vec = self._get_vec(img)
        if vec is None:
            return '', 0
        result = self._cos_sim_vs2d(self._registered, vec)
        result_idx = result.argmax()
        return self._file_list[result_idx][:-8], result[result_idx]
    
    
    def _cos_sim_vs2d(self, arr, vec):
        den = np.sqrt(np.einsum('ij,ij->i',arr,arr)*np.einsum('j,j',vec,vec))
        out = arr.dot(vec) / den
        return out


    def _get_vec(self, img):
        global mtcnn
        global resnet
        global nn_device
        img_cropped = mtcnn(img)
        if img_cropped == None:
            return None
        elif type(img_cropped) is torch.Tensor:
            img_embedding = resnet(img_cropped.unsqueeze(0).to(nn_device))
            return img_embedding.squeeze().to('cpu').detach().numpy().copy()
        else:
            img_cropped = torch.stack(img_cropped)
            img_embedding = resnet(img_cropped.to(nn_device))
            return img_embedding.to('cpu').detach().numpy().copy()
    

    def _make_dataset(self, dir_path):
        self._file_list = sorted(os.listdir(dir_path))
        ps = []
        for i in range(len(self._file_list)):
            print(dir_path + self._file_list[i])
            img = cv2.imread(dir_path + self._file_list[i])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ps += [img]
        q = np.stack(ps)
        return self._get_vec(q)
        