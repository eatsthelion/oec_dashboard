import tkinter as tk

from tkinter import *
from Backend.database import  DB_connect

import GUI.fonts
from GUI.widgets.highlight import enter_leave_stylechange
from GUI.GUI_Mains import FONT, FONTBOLD, OECCOLOR
from GUI.main_window import PopupWindow


class UpdateMultiProjectsGUI(PopupWindow):
    def __init__(self, master, configure=...) -> None:
        self.master = master
        super().__init__(master, bg='cyan4', configure=self.initial)

    def initial(self):
        self.titlelabel.configure(text='UPDATE MULTIPLE PROJECTS')
        self.widgetdict = {}
        self.entryframe = tk.Frame(self.frame, bg=self.frame.cget('background'))
        self.entryframe.pack(anchor=N, fill=BOTH, expand=1)
        self.data=None

        self.folder_frame = tk.Frame(self.entryframe, 
            bg=self.canvas_window.canvasframe.cget('background'))
        self.folder_entry = tk.Entry(self.folder_frame,  
            font=FONT,state=DISABLED, disabledbackground='white')
        self.folder_label = tk.Label(self.folder_frame,  
            font=FONT,bg=self.canvas_window.canvasframe.cget('background'), 
            text='Upload File:')
        self.folder_btton = tk.Button(self.folder_frame, 
            font=FONT,text='SELECT')

        self.folder_frame.grid(row=0,column=0,columnspan=2)

        self.folder_label.grid(row=0,column=0, sticky=W, padx=(5,0))
        self.folder_entry.grid(row=0,column=1, padx=(5,0), sticky=NSEW)
        self.folder_btton.grid(row=0,column=2, padx=5)

        self.uploadbutton = tk.Button(self.canvas_window.canvasframe, 
            font=FONT, text="★ UPDATE PROJECT ★", relief='flat', cursor='hand2')
        self.uploadbutton.pack(pady=10, fill=BOTH)

    def update_projects(self):
        pass