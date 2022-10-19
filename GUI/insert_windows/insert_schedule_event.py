import os
import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Backend.database import  DB_connect

import GUI.fonts
from GUI.GUI_Mains import FONT
from GUI.main_window import PopupWindow

from Backend.database import PROJECTDB, DB_connect, DB_clean_str

EVENTTYPES = ['TASK', 'MILESTONE', 'MEETING', 'SUBMITTAL', 'APROVAL']

class InsertScheduleEventGUI(PopupWindow):
    def __init__(self, master,parent=None, configure=...) -> None:
        self.master = master
        super().__init__(master, bg='cyan4', configure=self.initial)
        self.parent = parent
        self.width = 500
        self.height=450
        self.data = None

    def initial(self):
        self.titlelabel.configure(text='NEW EVENT')
        #self.canvas_show()
        #self.v_scroll_pack()
        self.entryframe = tk.Frame(self.frame, 
            bg=self.frame.cget('background'))
        self.entryframe.pack(expand=1, pady=(5,0), padx=5)
        
        event_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Event*:')
        type_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Event Type*:')
        desc_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Description:')
        assigned_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Assigned:')
        fore_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Forecast Date:')
        actl_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Actual Date:')

        ew = 30
        self.event = tk.Text(self.entryframe, font=FONT, width=ew, height=2,
            wrap='word')
        
        self.typevar = tk.StringVar(value=EVENTTYPES[0])
        self.typeOptions = tk.OptionMenu(self.entryframe, 
            self.typevar, *EVENTTYPES)
        self.typeOptions.config(font=FONT,
            relief = 'flat',indicatoron=0, cursor='hand2')
        self.typemenu = self.frame.nametowidget(self.typeOptions.menuname)
        self.typemenu.config(font=FONT)

        self.desc_text = tk.Text(self.entryframe, font=FONT, width=ew, height=3,
            wrap='word')
        self.assigned_entry = tk.Text(self.entryframe, font=FONT, width=ew,
            height=2, wrap='word')

        self.time_dict = {}
        self.ampm = ['AM', 'PM']
        for et in ['forecast', 'actual']:
            self.time_dict[et] = {'date':{}, 'time':{}, 'ampm':{}}
            self.time_dict[et]['date']['strvar'] = tk.StringVar(value='mm/dd/yy')
            self.time_dict[et]['date']['widget'] = tk.Entry(self.entryframe,  
                textvariable=self.time_dict[et]['date']['strvar'],font=FONT, 
                width=10)
            self.time_dict[et]['time']['strvar'] = tk.StringVar(value='hh:mm')
            self.time_dict[et]['time']['widget'] = tk.Entry(self.entryframe, 
                textvariable = self.time_dict[et]['time']['strvar'], font=FONT,
                width=10)
            self.time_dict[et]['ampm']['strvar'] = tk.StringVar(value='PM')
            self.time_dict[et]['ampm']['widget'] = tk.OptionMenu(
                self.entryframe,self.time_dict[et]['ampm']['strvar'],*self.ampm)
            self.time_dict[et]['ampm']['widget'].config(font=FONT,
                relief = 'flat', indicatoron=0, cursor='hand2')
            self.time_dict[et]['ampm']['menu'] = self.frame.nametowidget(
                self.time_dict[et]['ampm']['widget'].menuname)
            self.time_dict[et]['ampm']['menu'].config(font=FONT)

        enterbutton = tk.Button(self.frame, font=FONT, text='ADD EVENT',
            command=self.enter_event)

        for row, label in enumerate([event_label,type_label,desc_label,
            assigned_label, fore_label,actl_label]):
            label.grid(row=row, column = 0, padx=5, pady=5, sticky=W)

        for row, entry in enumerate([self.event,self.typeOptions,
            self.desc_text, self.assigned_entry]):
            entry.grid(row=row, column = 1, padx=(0,5), pady=5, sticky=EW,
                columnspan = 3)

        for row2, et in enumerate(self.time_dict, start=1):
            for col, ts in enumerate(self.time_dict[et], start=1):
                self.time_dict[et][ts]['widget'].grid(
                    row=row+row2,column=col,
                    padx=(0,5),pady=5,sticky=NSEW)

        enterbutton.pack(pady=5, fill='x', padx=5)

    def enter_event(self):
        new_event = DB_clean_str(self.event.get("1.0", END))
        desc = DB_clean_str(self.desc_text.get('1.0',END))
        event_type = DB_clean_str(self.typevar.get())
        assigned = DB_clean_str(self.assigned_entry.get('1.0',END))
        date_dict = {'forecast':'', 'actual':''}
        for et in self.time_dict:
            date_text = self.time_dict[et]['date']['strvar'].get()
            time_text = self.time_dict[et]['time']['strvar'].get()
            ampm_text = self.time_dict[et]['ampm']['strvar'].get()
            
            try:
                et_time = f"{date_text} {time_text} {ampm_text}"
                date_dict[et] = datetime.strptime(et_time, '%m/%d/%y %I:%M %p')
                continue
            except: pass
            try:
                date_dict[et] = datetime.strptime(date_text, '%m/%d/%y')
            except: pass

        # Checks for required data
        required = [new_event, event_type]
        for attribute in required:
            if attribute == '':
                messagebox.showerror('Missing Info', 
                'All required* fields must be filled before entry.')

        tt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        # Creates Status Log Change
        status_change=f"""{new_event} ({event_type}) was created."""
        if assigned:
            status_change += f"\n{new_event} was assigned to {assigned}"
        if date_dict['forecast'] != "":
            status_change += f"\n{new_event} was scheduled for " + \
                f"{date_dict['forecast'].strftime('%m/%d/%y')}"
            if date_dict['forecast'].strftime('%H:%M')!='00:00':
                status_change += " at " + \
                    f"{date_dict['forecast'].strftime('%I:%M %p')}"
        if date_dict['actual'] != "":
            status_change += f"\n{new_event} occured on " + \
                f"{date_dict['actual'].strftime('%m/%d/%y')}"
            if date_dict['actual'].strftime('%H:%M')!='00:00':
                status_change += " at " + \
                    f"{ date_dict['actual'].strftime('%I:%M %p')}"

        # Reformats dates into YY-mm-dd HH:MM:SS
        for dd in date_dict:
            try: 
                date_dict[dd] = date_dict[dd].strftime('%Y-%m-%d %H:%M:%S')
            except: pass
        
        DB_connect([f"""INSERT INTO project_dates VALUES 
            ('{self.data[0]}', '{new_event}', '{desc}', '{event_type}', 
            '{assigned}', '', '{date_dict['forecast']}', '{date_dict['actual']}',  
            '{tt}', '{tt}', '{os.getlogin().upper()}')""",

            f"""INSERT INTO project_status_log VALUES
            ('{self.data[0]}', '{status_change}', '{'SCHEDULE'}', '{tt}', 
            '{tt}', '{os.getlogin().upper()}') """,
            ], database = PROJECTDB)
        self.cancel_window()
        self.parent.searchwindow.refresh_page()

    def show_window(self):
        self.event.delete('1.0', END)
        self.desc_text.delete('1.0', END)
        self.assigned_entry.delete('1.0', END)
        self.typevar.set('TASK')
        for et in ['forecast', 'actual']:
            self.time_dict[et]['date']['strvar'].set('mm/dd/yy')
            self.time_dict[et]['time']['strvar'].set('HH:MM')
            self.time_dict[et]['ampm']['strvar'].set('AM')

        return super().show_window()

    def display_data(self, data):
        self.data = data
        self.show_window()