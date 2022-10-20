
PROGRAMTITLE = 'Package Options'

import tkinter as tk
from tkinter import *
from tkinter import messagebox

from Backend.database import  EMPTYLIST, DB_connect
from Backend.database_get import *

from GUI.window_option import *

class PackageOptionsWindow(OptionWindow):
    def __init__(self, master, **kw):
        super().__init__(master, bg='cyan4', width=400, height=200, 
        program_title = PROGRAMTITLE, **kw)
        self.data = None
        self.project_data = None

    def configure(self):
        button_width = 15
        self.button_frame = tk.Frame(self.frame, bg=self.frame.cget('background'))
        
        self.event_button = tk.Button(self.button_frame, 
            width=button_width, font=FONT, text='EVENT INFO',
            command=self.show_schedule_info)

        self.add_event_button = tk.Button(self.button_frame, 
            width=button_width, font=FONT, text='ADD EVENT',
            command=self.show_event_schedule)

        self.remove_event_button = tk.Button(self.button_frame, 
            width=button_width, font=FONT, text='REMOVE EVENT',
            command=self.remove_event)

        self.replace_event_button = tk.Button(self.button_frame, 
            width=button_width, font=FONT, text='REPLACE EVENT',
            command=self.show_event_schedule)

        self.delete_button = tk.Button(self.button_frame, bg='red', fg='white',
            width=button_width, font=FONT, text='DELETE PACKAGE')
        
        self.button_frame.pack(expand=1)
        return super().configure()

    def display_data(self, data, project_data):
        self.data = data
        self.project_data = project_data
        self.titlelabel.configure(text=self.data[1])

        self.event_button.grid_forget()
        self.add_event_button.grid_forget()
        self.remove_event_button.grid_forget()
        self.replace_event_button.grid_forget()
        self.delete_button.grid_forget()
        
        if self.data[5] not in EMPTYLIST:
            
            self.event_button.grid(row=0, column=0, columnspan=2, padx=5, 
                pady=5, sticky=EW)
                        
            self.remove_event_button.grid(row=1, column=0, 
                padx=5, pady=(0,5), sticky=EW)
            
            if self.parent.context != 'view event packages':
                self.replace_event_button.grid(row=1, column=1, 
                    padx=(0,5), pady=(0,5), sticky=EW)
        
        else:
            self.add_event_button.grid(row=0, column=0, padx=5, 
                pady=5, sticky=EW)

        if int(self.data[4]) == 1:
            self.delete_button.grid(row=2, column=0, columnspan=2,
                padx=5, pady=5, sticky=EW)

        self.show_window()

    def remove_event(self):
        if not messagebox.askyesno("Remove Event?", 
            "Are you sure you want to remove the event from this package?"):
            return
        DB_connect(f"""
        UPDATE packages SET event_id = '' WHERE rowid = {self.data[0]}
        """, database=PACKAGEDB)
        self.cancel_window()
        self.parent.searchwindow.refresh_page()

    def show_event_schedule(self):
        from Programs.project_schedule import ProjectScheduleGUI
        searchwindow = self.schedule_window = ProjectScheduleGUI(
            self.parent.frame_master, parent = self)
        db_function = lambda: get_schedule(self.project_data[0])
        titletext = f'SELECT A SCHEDULED EVENT'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."
        searchwindow.titlelabel.configure(text = titletext)

        # Sends the new dataset to the pop-up SearchWindow
        searchwindow.context = 'select'
        searchwindow.sender = self.add_event
        searchwindow.display_data(self.project_data, db_function)
        
        # Changes windows to display
        searchwindow.show_full_window()
        self.parent.cancel_window()
        self.cancel_window()

        # Sets the back button of new window to go to previous window
        searchwindow.back_direction = self.show_windows

    def show_windows(self):
        self.parent.show_full_window()
        self.show_window()

    def add_event(self, data):
        DB_connect(f"""
        UPDATE packages SET event_id = '{data[0]}' WHERE rowid = {self.data[0]}
        """, database=PACKAGEDB)
        self.cancel_window()
        self.parent.show_full_window()
        self.parent.refresh_page()

    def show_schedule_info(self):
        from Programs.info_schedule import ScheduleInfoWindow
        infowindow = ScheduleInfoWindow(self.master)
        infowindow.show_back_button()
        infowindow.back_direction=self.show_window
        infowindow.display_data(self.data[5])
        self.cancel_window()
