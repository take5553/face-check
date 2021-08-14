import tkinter as tk
from tkinter import ttk

class CaptureWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

if __name__ == "__main__":
    window = tk.Tk()
    app = CaptureWindow(master=window)
    app.mainloop()
    