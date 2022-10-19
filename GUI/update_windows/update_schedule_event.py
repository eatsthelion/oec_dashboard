###############################################################################
# catalog_projects.py
# 
# Created: 8/02/22
# Creator: Ethan de Leon
# Purposes: 
#   - Organize and store all of our project data in one place
#   - Export Project Data into a single Excel File
#   - Easily make real time edits and changes to a project
#   - Keep track of project schedules
#   - Access the different attributes of a project including:
#       - Project Schedule
#       - Project Budget
#       - Project Employee Assignments
#       - Project Packages/Deliverables
#       - Project Documents
# Required Installs: pandas, openpyxl
###############################################################################

import os
import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Backend.database import  DBTIME, REGTIME, TIME12HR, USERTIME, DB_connect

import GUI.fonts
from GUI.GUI_Mains import FONT
from GUI.main_window import PopupWindow

from Backend.database import PROJECTDB, DB_connect, DB_clean_str

EVENTTYPES = ['TASK', 'MILESTONE', 'MEETING', 'SUBMITTAL', 'APROVAL']

class UpdateScheduleEventGUI(PopupWindow):
    def __init__(self, master,parent=None, configure=...) -> None:
        self.master = master
        super().__init__(master, bg='cyan4', configure=self.initial)
        self.parent = parent
        self.width = 500
        self.height=470
        self.data = None
        self.project_id = None

    def initial(self):
        self.titlelabel.configure(text='UPDATE EVENT')
        #self.canvas_show()
        #self.v_scroll_pack()
        self.entryframe = tk.Frame(self.frame, 
            bg=self.frame.cget('background'))
        self.entryframe.pack(expand=1, pady=(5,0), padx=5)
        
        event_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Event:')
        type_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Event Type:')
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
        prog_label = tk.Label(
            self.entryframe,bg=self.frame.cget('background'),
            font = FONT, text='Progress Percent:')

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

        self.progress_entry = tk.Entry(self.entryframe, font=FONT, width=ew)

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

        enterbutton = tk.Button(self.frame, font=FONT, text='UPDATE EVENT',
            command=self.update_event)

        for row, label in enumerate([event_label,type_label,desc_label,
            assigned_label, prog_label, fore_label,actl_label]):
            label.grid(row=row, column = 0, padx=5, pady=5, sticky=W)

        for row, entry in enumerate([self.event,self.typeOptions,
            self.desc_text, self.assigned_entry, self.progress_entry]):
            entry.grid(row=row, column = 1, padx=(0,5), pady=5, sticky=EW,
                columnspan = 3)

        for row2, et in enumerate(self.time_dict, start=1):
            for col, ts in enumerate(self.time_dict[et], start=1):
                self.time_dict[et][ts]['widget'].grid(
                    row=row+row2,column=col,
                    padx=(0,5),pady=5,sticky=NSEW)

        enterbutton.pack(pady=5, fill='x', padx=5)

    def update_event(self):
        new_event = DB_clean_str(self.event.get("1.0", END))
        desc = DB_clean_str(self.desc_text.get('1.0',END))
        event_type = DB_clean_str(self.typevar.get())
        assigned = DB_clean_str(self.assigned_entry.get('1.0',END))
        progress = DB_clean_str(self.progress_entry.get())
        
        # formats dates and filters out invalid dates
        date_dict = {'forecast':'', 'actual':''}
        for et in self.time_dict:
            date_text = self.time_dict[et]['date']['strvar'].get()
            time_text = self.time_dict[et]['time']['strvar'].get()
            ampm_text = self.time_dict[et]['ampm']['strvar'].get()
            
            try:
                et_time = f"{date_text} {time_text} {ampm_text}"
                date_dict[et] = datetime.strptime(et_time, USERTIME)
                continue
            except: pass
            try:
                date_dict[et] = datetime.strptime(date_text, REGTIME)
            except: pass

        # Checks for required data
        required = [new_event, event_type]
        for attribute in required:
            if attribute == '':
                messagebox.showerror('Missing Info', 
                'All required* fields must be filled before entry.')
                return

        tt = datetime.today().strftime(DBTIME)

        # Finds which data was changed
        updates = ''
        status_change= ''
        if new_event != self.data[1]:
            updates += f"event = '{new_event}', "
            status_change += f"\n\n{new_event} updated its title from " + \
                f"'{self.data[1]}' to '{new_event}'"
        if desc != self.data[2]:
            updates += f"description = '{desc}', "
            status_change += f"\n\n{new_event} updated its description from " + \
                f"'{self.data[2]}' to '{desc}'"
        if event_type != self.data[3]:
            updates += f"event_type = '{event_type}', "
            status_change += f"\n\n{new_event} updated its type from " + \
                f"'{self.data[3]}' to '{event_type}'" 
        if assigned != self.data[4]:
            updates += f"assigned = '{assigned}', "
            status_change += f"\n\n{new_event} updated its assignment from " + \
                f"'{self.data[4]}' to '{assigned}'" 

        if progress != "":
            try: 
                float(progress)
                if self.data[5]!='':
                    if str(self.data[5]) != progress:
                        updates += f"progress_percent = '{progress}', "
                        status_change += f"\n\n{new_event} " + \
                            f"updated its progress to {progress}%" 
                else:
                    updates += f"progress_percent = '{progress}', "
                    status_change += f"\n\n{new_event} " + \
                        f"updated its progress to {progress}%" 
            except:
                messagebox.showerror('Invalid Input',
                'The input of Progress Percentage can only be a numerical value.')
            
        # Checks if dates were changed
        date_updates = ''
        date_status = ''
        for dd in [
            ('forecast', self.data[6], 'forecast_date', 'was scheduled to ',
                'was rescheduled from '), 
            ('actual', self.data[7], 'actual_date', 'occured on ', 
                'was changed from ')
            ]:

            if date_dict[dd[0]] != '':
                dt = date_dict[dd[0]].strftime(DBTIME)
                if dt == dd[1]:
                    continue
                
                date_updates += f"{dd[2]} = '{dt}', "
                if dd[1] == '':
                    date_status += f"\n{new_event} ({event_type}) " + \
                        dd[3] + \
                        f"{date_dict[dd[0]].strftime(REGTIME)} at " + \
                        f"{date_dict[dd[0]].strftime(TIME12HR)}"
                else:
                    old_time = datetime.strptime(dd[1],DBTIME)
                    date_status += f"\n{new_event} ({event_type}) " + \
                        dd[4] + \
                        f"{old_time.strftime(REGTIME)} at " + \
                        f"{date_dict[dd[0]].strftime(TIME12HR)} to " +\
                        f"{date_dict[dd[0]].strftime(REGTIME)} at " + \
                        f"{date_dict[dd[0]].strftime(TIME12HR)}"

            elif (date_dict[dd[0]] == '') and (dd[1] != ''):
                date_updates += f"{dd[2]} = '{dt}', "
                date_status += f"\nThe {dd[0]} date for {new_event} " + \
                f"{event_type} was removed" 
                pass


        if (updates == "") and (date_updates == ''):
            return
        

        sql_array = []
        updates += date_updates
        if updates != '':
            updates += f"modify_date = '{tt}', "
            updates += f"last_modified_by = '{os.getlogin().upper()}' "
            status_change = DB_clean_str(status_change)
            sql_array += [
            f"UPDATE project_dates SET {updates.strip(', ')} " + \
            f"WHERE rowid = {self.data[0]}"
            ]              
        if status_change != '':
            status_change = DB_clean_str(status_change)
            sql_array += [
            f"""INSERT INTO project_status_log VALUES
            ('{self.project_id}', '{status_change}', '{'SCHEDULE INFO'}', 
            '{tt}', '{tt}', '{os.getlogin().upper()}')"""]
            
        if date_updates != '':
            date_status = DB_clean_str(date_status)
            sql_array += [
            f"""INSERT INTO project_status_log VALUES
            ('{self.project_id}', '{date_status}', 
            '{'SCHEDULE DATE CHANGE'}', '{tt}', '{tt}', 
            '{os.getlogin().upper()}')"""]      

        # Reformats dates into YY-mm-dd HH:MM:SS
        for dd in date_dict:
            try: 
                date_dict[dd] = date_dict[dd].strftime('%Y-%m-%d %H:%M:%S')
            except: pass
        
        # Updates databases 
        DB_connect(sql_array, database = PROJECTDB)
        self.cancel_window()
        self.parent.searchwindow.resultwindow.refresh_results()

    def show_window(self):
        self.event.delete('1.0', END)
        self.desc_text.delete('1.0', END)
        self.assigned_entry.delete('1.0', END)
        self.progress_entry.delete(0,END)

        self.event.insert('1.0', self.data[1])
        self.desc_text.insert('1.0', self.data[2])
        self.assigned_entry.insert('1.0', self.data[4])

        self.typevar.set(self.data[3])
        self.progress_entry.insert(0,DB_clean_str(str(self.data[5])))
        try: 
            fore_obj = datetime.strptime(self.data[6],'%Y-%m-%d %H:%M:%S')
            self.time_dict['forecast']['date']['strvar'].set(
                fore_obj.strftime('%m/%d/%y'))
            if fore_obj.strftime("%H:%M")!='00:00':
                self.time_dict['forecast']['time']['strvar'].set(
                    fore_obj.strftime('%I:%M'))
                self.time_dict['forecast']['ampm']['strvar'].set(
                    fore_obj.strftime('%p'))
            else:
                self.time_dict['forecast']['time']['strvar'].set('HH:MM')
                self.time_dict['forecast']['ampm']['strvar'].set('AM')
        except: 
            self.time_dict['forecast']['date']['strvar'].set('mm/dd/yy')
            self.time_dict['forecast']['time']['strvar'].set('HH:MM')
            self.time_dict['forecast']['ampm']['strvar'].set('AM')

        try: 
            actl_obj = datetime.strptime(self.data[7],'%Y-%m-%d %H:%M:%S')
            self.time_dict['actual']['date']['strvar'].set(
                actl_obj.strftime('%m/%d/%y'))
            if actl_obj.strftime("%H:%M")!='00:00':
                self.time_dict['actual']['time']['strvar'].set(
                    actl_obj.strftime('%I:%M'))
                self.time_dict['actual']['ampm']['strvar'].set(
                    actl_obj.strftime('%p'))
            else:
                self.time_dict['actual']['time']['strvar'].set('HH:MM')
                self.time_dict['actual']['ampm']['strvar'].set('AM')
        except:
            self.time_dict['actual']['date']['strvar'].set('mm/dd/yy')
            self.time_dict['actual']['time']['strvar'].set('HH:MM')
            self.time_dict['actual']['ampm']['strvar'].set('AM')
        return super().show_window()

    def display_data(self, data, project_id):
        self.data = data
        self.project_id = project_id
        if len(self.data[1])>22:
            headertext = self.data[1][:22] + "..."
        else:
            headertext = self.data[1]
        self.titlelabel.configure(text=headertext)
        self.show_window()