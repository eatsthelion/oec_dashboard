from tkinter import NSEW
from datetime import datetime

from Backend.database import USERTIME, REGTIME
from GUI.widgets.basics import *

class DateEntry(MyFrame):
    def __init__(self, master, font = FONT, **kw) -> None:
        super().__init__(master, **kw)

        self.date_entry = MyEntry(self, font=font, width=10, value='mm/dd/yy')
        self.time_entry = MyEntry(self, font=font, width=10, value='00:00')
        self.ampm_entry = MyOptionMenu(self, ['AM', 'PM'])

        self.date_entry.grid(row=0, column=0, sticky=NSEW)
        self.time_entry.grid(row=0, column=1, padx=5, sticky=NSEW)
        self.ampm_entry.grid(row=0, column=2, sticky=NSEW)

    def get(self):
        date_text = self.date_entry.get()
        time_text = self.time_entry.get()
        ampm_text = self.ampm_entry.get()

        try: 
            et_time = f"{date_text} {time_text} {ampm_text}"
            et_time = datetime.strptime(et_time, USERTIME)
        except: 
            try:
                et_time = datetime.strptime(date_text, REGTIME)
            except:
                return ''
        return et_time

    def insert(self, date_obj:datetime):
        self.date_entry.set(date_obj.strftime("%m/%d/%y"))
        self.time_entry.set(date_obj.strftime("%I:%M"))
        self.ampm_entry.set(date_obj.strftime("%p"))

    def delete(self):
        self.date_entry.set('mm/dd/yy')
        self.time_entry.set('00:00')
        self.ampm_entry.set('AM')

    def compare_dates(self, date_obj):
        entry = self.get()
        if (date_obj != None) and entry != '':
            return 'updated'
        elif date_obj != None and entry == '':
            return 'removed'
        elif date_obj == None and entry != '':
            return 'set'
        else:
            return None