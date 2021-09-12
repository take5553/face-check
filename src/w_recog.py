import cv2
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import ttk
import json_util as ju
from mycamera import MyCamera

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
        
        self._camera.running = True
        self.master.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._update()


    def _create_widgets(self):

        # Canvas
        self._canvas1 = tk.Canvas(self, width = self._canvas_width, height = self._canvas_height)
        self._canvas1.grid(column=0, row=0, sticky=(tk.W, tk.E))
        
        
    def _on_closing(self):
        self._camera.running = False
        self._camera.cap.release()
        self.master.destroy()
        
    
    def _update(self):
        frame = self._camera.value
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self._photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self._canvas1.create_image(0, 0, image = self._photo, anchor = tk.NW)
        self.master.after(self._delay, self._update)


if __name__ == "__main__":
    window = tk.Tk()
    app = RecogWindow(master=window)
    app.mainloop()