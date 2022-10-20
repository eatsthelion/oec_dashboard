import tkinter as tk
from tkinter import *

class TestGUI():
    def __init__(self, testmodule):
        self.root = tk.Tk()
        self.width = 1280
        self.height = 720
        self.bg = "#7f007f"
        self.children = []
        self.font = ('helvetica', 20, 'bold')
        self.root.title('Test GUI')
        self.root.resizable(1,1)
        self.root.minsize(self.width, self.height)
        self.root.geometry('+{}+{}'.format(
            int((self.root.winfo_screenwidth()-self.width)/2),
            int((self.root.winfo_screenheight()-self.height)/2)))

        # Fullscreen button binding  
        self.fullscreen = False
        self.root.bind("<F11>", self.fullscreen_command)

        testing = testmodule(self.root, parent=self)
        testing.frame.pack()
        tk.mainloop()

    def fullscreen_command(self, event):
        if self.fullscreen == False:
            self.root.attributes('-fullscreen',True)
            self.fullscreen = True
        else: 
            self.root.attributes('-fullscreen',False)
            self.fullscreen = False