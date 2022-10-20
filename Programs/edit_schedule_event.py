###############################################################################
# edit_schedule.py
# 
# Created: 8/02/22
# Creator: Ethan de Leon
# Purposes: 
#   - GUI for both inserting and modifying project schedule data in the 
#     database
###############################################################################
PROGRAMTITLE = 'Schedule Edits'

from datetime import datetime

from Backend.database import PROJECTDB
from Backend.database import  DBTIME, USERTIME
from Backend.database_send import project_edit_entry, project_input_entry

from GUI.window_edit import *

EVENTTYPES = ['TASK', 'MILESTONE', 'MEETING', 'SUBMITTAL', 'APROVAL']

class EditScheduleEventGUI(EditWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='coral2', width = 500,
        height=470, program_title = PROGRAMTITLE, **kw)
        
    def configure(self):
        self.titlelabel.configure(text='UPDATE EVENT')
        
        self.entryframe = MyFrame(self.frame)
        self.entryframe.pack(expand=1, pady=(5,0), padx=5)

        ew = 30
        lmh = ['LOW', 'MEDIUM', 'HIGH']
        status_opts = [
            'NOT STARTED', 'ACTIVE', 'CANCELED', 'ON HOLD', 'COMPLETED'
            ]

        self.event              = MyText(self.entryframe, width=ew, height=2)
        self.typeOptions        = MyOptionMenu(self.entryframe, EVENTTYPES)
        self.status_options     = MyOptionMenu(self.entryframe, status_opts)
        self.priority_options   = MyOptionMenu(self.entryframe, lmh)
        self.difficulty_options = MyOptionMenu(self.entryframe, lmh)
        self.desc_text          = MyText(self.entryframe, width=ew, height=3)
        self.progress_entry     = MyEntry(self.entryframe, font=FONT, width=ew)
        self.forecast_entry     = DateEntry(self.entryframe)
        self.actual_entry       = DateEntry(self.entryframe)

        self.datapairs = [
            ('Event*:',self.event                   ),  
            ('Event Type*:',self.typeOptions        ),
            ('Status:',self.status_options          ),
            ('Progress (%):',self.progress_entry    ),          
            ('Priority:',self.priority_options      ),      
            ('Difficulty:',self.difficulty_options  ),       
            ('Description:',self.desc_text          ),        
            ('Forecast Date:',self.forecast_entry   ),          
            ('Actual Date:',self.actual_entry       ),
        ]

        self.enterbutton = MyButton(self.frame, command=self.enter_command)
        self.enterbutton.pack(pady=5, fill='x', padx=5)
        return super().configure()

    def widget_placement(self):
        for child in self.entryframe.winfo_children():
            child.grid_forget()
        for row, datapair in enumerate(self.datapairs):
            if self.context == 'insert' and self.progress_entry in datapair:
                continue
            label = MyLabel(self.entryframe, text=datapair[0])
            label.grid(row=row, column = 0, padx=5, pady=(5,0), sticky=W)
            datapair[1].grid(row=row, column = 1, padx=5, pady=(5,0), sticky=EW)

    def enter_command(self):
        lmh_dict = {'LOW':1, 'MEDIUM':2, 'HIGH':3}
        new_event = self.event.get()
        desc = self.desc_text.get()
        event_type = self.typeOptions.get()
        priority = lmh_dict[self.priority_options.get()]
        difficulty = lmh_dict[self.difficulty_options.get()]
        progress = self.progress_entry.get()
        forecast = self.forecast_entry.get()
        actual = self.actual_entry.get()
        status = self.status_options.get()

        required = [new_event, event_type]
        for attribute in required:
            if attribute == '':
                messagebox.showerror('Missing Info', 
                'All required* fields must be filled before entry.')
                return
        if self.context == 'insert':
            status_updates = f"Event {new_event} ({event_type}) was created.\n"

            if forecast!='':
                fd = forecast.strftime(USERTIME)
                forecast = forecast.strftime(DBTIME)
                status_updates+=f"{new_event} has a forecast date on {fd}\n"
            if actual!='':
                ad = actual.strftime(USERTIME)
                actual = actual.strftime(DBTIME)
                status_updates+=f"{new_event} has an actual date on {ad}\n"
            sql_query = f"""'{self.project_id}', '{new_event}', '{desc}', '{event_type}', 
            '', '{forecast}', '{actual}', 0, {difficulty}, {priority}, '{status}'"""

            project_input_entry(self.project_id, 'project_dates', PROJECTDB,
            sql_query, status_updates, 'NEW EVENT', user=self.user)

        elif self.context == 'modify':
            datapairs = [
                (self.data[1], new_event, 'event', 'event'),
                (self.data[2], desc, 'description', 'description'),
                (self.data[3], event_type, 'event type', 'event_type'),
                (self.data[6], priority, 'priority', 'priority'),
                (self.data[7], difficulty, 'difficulty', 'difficulty'),
                (self.data[5], progress, 'progress', 'progress_percent'),
                (self.data[4], status, 'status', 'status'),
            ]
            datelist=[
                (self.data[10], self.forecast_entry, 'forecast', 'forecast_date'),
                (self.data[11], self.actual_entry, 'actual', 'actual_date')
            ]

            project_edit_entry(self.project_id, self.data[0], 'project_dates',
            PROJECTDB, new_event, 'EVENT INFO EDIT', datapairs, datelist,
            user=self.user, date_status_type='SCHEDULE CHANGE')

        self.cancel_window()
        self.parent.searchwindow.refresh_page()
        

    def display_data(self, project_id, data=None):
        self.data = data
        self.project_id = project_id
        if self.data == None:
            self.context = 'insert'
            self.titlelabel.configure(text="NEW SCHEDULE EVENT")
        else:
            self.context = 'modify'
            if len(self.data[1])>22:
                headertext = self.data[1][:22] + "..."
            else:
                headertext = self.data[1]
            self.titlelabel.configure(text=headertext)
        self.show_window()

    def show_window(self):
        self.event.delete()
        self.desc_text.delete()
        self.progress_entry.delete()
        self.forecast_entry.delete()
        self.actual_entry.delete()
        self.priority_options.delete()
        self.difficulty_options.delete()
        self.widget_placement()
        if self.context == 'insert':
            self.enterbutton.configure(text = 'ADD EVENT')
            return super().show_window()

        self.enterbutton.configure(text='UPDATE EVENT')
        self.event.insert(self.data[1])
        self.desc_text.insert(self.data[2])
        self.typeOptions.set(self.data[3])
        self.status_options.set(self.data[4])
        self.progress_entry.insert(f"{(self.data[5]*100):.2f}")
        self.priority_options.set(self.data[6])
        self.difficulty_options.set(self.data[7])
        
        try:
            date_obj = datetime.strptime(self.data[9], DBTIME)
            self.forecast_entry.insert(date_obj)
        except:
            pass
        try:
            date_obj = datetime.strptime(self.data[10], DBTIME) 
            self.actual_entry.insert(date_obj)
        except:
            pass

        return super().show_window()