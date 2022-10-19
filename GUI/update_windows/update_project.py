import tkinter as tk

from tkinter import *
from Backend.database import  DB_connect

import GUI.fonts
from GUI.widgets.highlight import enter_leave_stylechange
from GUI.GUI_Mains import FONT, FONTBOLD, OECCOLOR
from GUI.main_window import PopupWindow

COLUMNTITLES = ['Project Title', 'Client', 'Client Job #','Location', 'Project Engineer', 
    'Outdoor Designers', 'Indoor Designers', 'Project Type', 'CWA Type']
class UpdateProjectGUI(PopupWindow):
    def __init__(self, master, parent=None, configure=...) -> None:
        self.master = master
        super().__init__(master, bg='cyan4', configure=self.initial)
        self.parent = parent

    def initial(self):
        titlelabel = tk.Label(self.canvas_window.canvasframe, bg=self.canvas_window.canvasframe.cget('background'), font=FONTBOLD, text='UPDATE PROJECT')
        titlelabel.pack(pady=10)
        self.widgetdict = {}
        self.entryframe = tk.Frame(self.canvas_window.canvasframe, bg=self.canvas_window.canvasframe.cget('background'))
        self.entryframe.pack(anchor=CENTER)
        self.data=None

        self.folder_frame = tk.Frame(self.entryframe,bg=self.canvas_window.canvasframe.cget('background'))
        self.folder_entry = tk.Entry(self.folder_frame,  font=FONT,state=DISABLED, disabledbackground='white')
        self.folder_label = tk.Label(self.folder_frame,  font=FONT,bg=self.canvas_window.canvasframe.cget('background'), text='Upload File:')
        self.folder_btton = tk.Button(self.folder_frame, font=FONT,text='SELECT')

        self.folder_frame.grid(row=0,column=0,columnspan=2)

        self.folder_label.grid(row=0,column=0, sticky=NW, padx=(5,0))
        self.folder_entry.grid(row=0,column=1, padx=(5,0))
        self.folder_btton.grid(row=0,column=2, padx=5)

        self.active_statuses = ['ACTIVE', 'COMPLETE', 'ON HOLD', 'CANCELLED']
        self.active_status_label = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Active Status:')

        self.active_status_strvar = tk.StringVar(value=self.active_statuses[0])
        self.active_status_options = tk.OptionMenu(self.entryframe, self.active_status_strvar, *self.active_statuses)
        self.active_status_options.config(font=FONT, relief = 'flat',indicatoron=0, cursor='hand2')
        self.statusmenu = self.entryframe.nametowidget(self.active_status_options.menuname)
        self.statusmenu.config(font=(FONT[0],FONT[1]))

        title_entry_label       = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Project Title:')
        client_label            = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Client:')
        client_job_label        = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Client Job #:')
        location_label          = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Location:')
        project_engineer_label  = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Project Engineer:')
        outdoor_designers_label = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Outdoor Designers:')
        indoor_designers_label  = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Indoor Designers:')
        project_type_label      = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='Project Type:')
        cwa_type_label          = tk.Label(self.entryframe, font=FONT, bg=self.frame.cget('background'), text='CWA Type:')

        title_entry_label       .grid(row=self.row_counter(reset=True), column=0, padx=10, sticky=NW)

        self.active_status_label.grid(row=self.row_counter(),column=0, ipadx=10,sticky=NW)

        client_label            .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        client_job_label        .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        location_label          .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        project_engineer_label  .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        outdoor_designers_label .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        indoor_designers_label  .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        project_type_label      .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)
        cwa_type_label          .grid(row=self.row_counter(), column=0, padx=10, sticky=NW)

        self.title_strvar             = tk.StringVar()
        self.client_strvar            = tk.StringVar()
        self.client_job_strvar        = tk.StringVar()
        self.location_strvar          = tk.StringVar()
        self.project_engineer_strvar  = tk.StringVar()
        self.outdoor_designers_strvar = tk.StringVar()
        self.indoor_designers_strvar  = tk.StringVar()
        self.project_type_strvar      = tk.StringVar()
        self.cwa_type_strvar          = tk.StringVar()

        self.title_entry             = tk.Entry(self.entryframe, textvariable = self.title_strvar            , font=FONT, text='Project Title*:')
        self.client_entry            = tk.Entry(self.entryframe, textvariable = self.client_strvar           , font=FONT, text='Client*:')
        self.client_job_entry        = tk.Entry(self.entryframe, textvariable = self.client_job_strvar       , font=FONT, text='Client Job #:')
        self.location_entry          = tk.Entry(self.entryframe, textvariable = self.location_strvar         , font=FONT, text='Location*:')
        self.project_engineer_entry  = tk.Entry(self.entryframe, textvariable = self.project_engineer_strvar , font=FONT, text='Project Engineer*:')
        self.outdoor_designers_entry = tk.Entry(self.entryframe, textvariable = self.outdoor_designers_strvar, font=FONT, text='Outdoor Designers:')
        self.indoor_designers_entry  = tk.Entry(self.entryframe, textvariable = self.indoor_designers_strvar , font=FONT, text='Indoor Designers:')
        self.project_type_entry      = tk.Entry(self.entryframe, textvariable = self.project_type_strvar     , font=FONT, text='Project Type:')
        self.cwa_type_entry          = tk.Entry(self.entryframe, textvariable = self.cwa_type_strvar         , font=FONT, text='CWA Type:')

        self.title_entry            .grid(row=self.row_counter(reset=True), column=1, padx=10,sticky=NW)
        self.active_status_options  .grid(row=self.row_counter(),column=1, sticky=NW, pady=5)
        self.client_entry           .grid(row=self.row_counter(), column=1, padx=10, sticky=NW)
        self.client_job_entry       .grid(row=self.row_counter(), column=1, padx=10, sticky=NW)
        self.location_entry         .grid(row=self.row_counter(), column=1, padx=10, sticky=NW)
        self.project_engineer_entry .grid(row=self.row_counter(), column=1, padx=10, sticky=NW)
        self.outdoor_designers_entry.grid(row=self.row_counter(), column=1, padx=10, sticky=NW)
        self.indoor_designers_entry .grid(row=self.row_counter(), column=1, padx=10, sticky=NW)
        self.project_type_entry     .grid(row=self.row_counter(), column=1, padx=10, sticky=NW)
        self.cwa_type_entry         .grid(row=self.row_counter(), column=1, padx=10, sticky=NW)

        self.uploadbutton = tk.Button(self.canvas_window.canvasframe, font=FONT, text="★ UPDATE PROJECT ★", relief='flat', cursor='hand2')
        self.uploadbutton.pack(pady=10)

    def update_project(self):
        pass

    def display_data(self):
        self.title_entry             .delete(0,END)
        self.client_entry            .delete(0,END)
        self.client_job_entry        .delete(0,END)
        self.location_entry          .delete(0,END)
        self.project_engineer_entry  .delete(0,END)
        self.outdoor_designers_entry .delete(0,END)
        self.indoor_designers_entry  .delete(0,END)
        self.project_type_entry      .delete(0,END)
        self.cwa_type_entry          .delete(0,END)

        self.title_entry             .insert(0,self.data[5])# text='Project Title*:')
        self.client_entry            .insert(0,self.data[3])# text='Client*:')
        self.client_job_entry        .insert(0,self.data[2])# text='Client Job #:')
        self.location_entry          .insert(0,self.data[6])# text='Location*:')
        self.project_engineer_entry  .insert(0,self.data[7])# text='Project Engineer*:')
        self.outdoor_designers_entry .insert(0,self.data[8])# text='Outdoor Designers:')
        self.indoor_designers_entry  .insert(0,self.data[9])# text='Indoor Designers:')
        self.project_type_entry      .insert(0,self.data[10])# text='Project Type:')
        self.cwa_type_entry          .insert(0,self.data[11])# text='CWA Type:')

    def row_counter(self, reset=False):
        if reset == True: self.row_count = 0
        try: self.row_count +=1
        except: self.row_count = 0
        return self.row_count