###############################################################################
# project_schedule.py
# 
# Created: 10/19/22
# Creator: Ethan de Leon
# Purposes:
#   - Displays and organizes the schedule of a project
#   - Connects to
#       - option_packages.py to see package options
#       - edit_packages.py for package insertion or package editing
#       - project_package_documents.py to view a package's contents
###############################################################################

from GUI.window_datatable import *
from Programs.edit_schedule_event import EditScheduleEventGUI
from Programs.option_schedule import ScheduleOptionsWindow

class ProjectScheduleGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Schedules',
        bg='coral1', col_color='orangered',
        leftoptions=self.leftoptions,  
        additional_windows = self.additionalOptions, 
        format_dict='project_schedule',
        **kw)

    def configure(self, **kw):
        self.upcoming_frame = MyLabelFrame(self.frame, font=(FONT[0], 16), 
            text="UPCOMING SCHEDULE")
        self.upcoming_label = MyLabel(self.upcoming_frame, font=(FONT[0], 16), 
            text="NO UPCOMING DATES")
        
        self.upcoming_frame.pack()
        self.upcoming_label.pack()
        super().configure(**kw)

    def leftoptions(self, master, dataset, row):
        if self.context == 'display':
            update_event = MyButton(master, text='UPDATE',
                command=lambda m=dataset:self.show_edit_window(data=m))
            details  = MyButton(master, text='  +  ', 
                command=lambda m=dataset: self.show_options_window(m))

            if self.clearance_check(7, 
                self.get_data('project_engineers_ids', data_dict = self.project_data_dict)):
                update_event.grid(row=0,column=1,padx=(5,0))
                
            details.grid(row=0,column=3,padx=5)

        elif self.context == 'select':
            select_button = MyButton(master, text='SELECT',
                command=lambda m=dataset: self.select_data(m))
            select_button.grid(row=0,column=3,padx=5)

    def additionalOptions(self, button_master, frame_master):
        self.insert_button = MyButton(button_master, text='NEW EVENT', 
            command=self.show_edit_window)
        self.multi_update_button = MyButton(button_master, 
            text='UPDATE WHOLE SCHEDULE')   
        self.all_schedule_button = MyButton(button_master, 
            text='EXPORT TO EXCEL')

        self.all_schedule_button .pack(side='left', pady=(10,2),padx=5)
        self.insert_button       .pack(side='left', pady=(10,2),padx=5)
        self.multi_update_button .pack(side='left', pady=(10,2),padx=5)

    def show_options_window(self, data):
        option_window = ScheduleOptionsWindow(self.frame, parent=self)
        option_window.display_data(data, self.data)
    def show_edit_window(self, data=None):
        edit_window = EditScheduleEventGUI(self.frame, parent=self)
        edit_window.display_data(self.data[0], data=data)

    def display_data(self, data,  datasetget):
        self.all_schedule_button .pack_forget()
        self.insert_button       .pack_forget()
        self.multi_update_button .pack_forget()

        if self.context == 'select':
            self.insert_button       .pack(side='left', pady=(10,2),padx=5)
        else:
            self.all_schedule_button .pack(side='left', pady=(10,2),padx=5)
            self.insert_button       .pack(side='left', pady=(10,2),padx=5)
            self.multi_update_button .pack(side='left', pady=(10,2),padx=5)
            
        return super().display_data(data, datasetget)

    def select_data(self, dataset):
        self.sender(dataset)
        self.cancel_window()