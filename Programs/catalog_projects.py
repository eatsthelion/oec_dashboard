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

from datetime import datetime
from Backend.database_get import get_my_project_info, get_project_info

from Backend.exports import see_all_projects

from GUI.window_datatable import *
from Programs.edit_project import EditProjectGUI
from Programs.info_project import BasicProjectInfo
from Programs.option_projects import ProjectOptionsWindow

PROGRAMTITLE = 'Project Catalog'

class ProjectCatalog(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, entrylimit = 15,
        sortfunction=self.sortfunction,
        leftoptions = self.leftoptions, 
        additional_windows = self.additonalOptions, 
        format_dict='project_catalog', program_title = PROGRAMTITLE,
        destroy_stop = True,
        **kw)       
    
    def configure(self):
        self.titlelabel.configure(font = ("montserrat extrabold",24,'bold'), 
            text="★ "+PROGRAMTITLE.upper()+" ★", bg='white',
            height=2)
        self.titlelabel.place_forget()
        self.titlelabel.pack(fill='x')
        
        super().configure()
        
        self.terminal = Terminal(self.frame)
        self.hide_back_button()
        self.hide_cancel_button()
    
    def leftoptions(self, master, dataset, row):
        select_button = MyButton(master, text='SELECT')
        see_project_info=MyButton(master, text='INFO', 
            command = lambda m=dataset: self.show_info_window(m))
        update_project = MyButton(master, text='UPDATE',
            command=lambda m=dataset: self.show_edit_window(m))
        details  = MyButton(master, text='  +  ', 
            command=lambda m=dataset: self.show_options_window(m))

        see_project_info.grid(row=0,column=0,padx=(5,0),sticky=NS)
        if self.context == 'select':
            select_button.grid(row=0,column=1,padx=(5,0),sticky=NS)
        if self.clearance_check(7, self.get_data('project_engineers_ids', dataset)):
            update_project.grid(row=0,column=1,padx=(5,0),sticky=NS)
        details.grid(row=0,column=2,padx=5,sticky=NS)

    def sortfunction(self, sortby, dataset):
        if sortby == 'SORT BY FILE NAME (A-Z)': 
            named_entries = []
            nameless_entries = []
            for data in dataset:
                if data[2] in ['', None]: 
                    nameless_entries.append(data)
                    continue
                named_entries.append(data)
            named_entries.sort(key=lambda i:i[2])
            dataset = named_entries + nameless_entries
        elif sortby == 'SORT BY OEC NUMBER': 
            dataset.sort(key=lambda i:i[1],reverse=True)
        elif sortby == 'SORT BY NEWEST': 
            dataset.sort(key=lambda i: datetime.strptime(
                i[15], "%Y-%m-%d %H:%M:%S"), reverse=True)
        elif sortby == 'SORT BY OLDEST': 
            dataset.sort(key=lambda i: datetime.strptime(
                i[15], "%Y-%m-%d %H:%M:%S"))
        elif sortby == 'SORT BY LAST MODIFIED': 
            dataset.sort(key=lambda i: datetime.strptime(
                i[16], "%Y-%m-%d %H:%M:%S"))
        return dataset 

    def additonalOptions(self, button_master, frame_master):
        self.frame_master = frame_master
        insert_button = MyButton(button_master, text='NEW PROJECT', 
            command=self.show_edit_window)
        self.see_project_button = MyButton(button_master, text='MY PROJECTS', 
            command= self.see_my_projects)
        
        look_ahead_button = MyButton(button_master, text='4-Week Look Ahead')

        all_projects_button = MyButton(button_master, text='EXPORT ALL PROJECTS',
            command=lambda:see_all_projects(self.terminal))

        if self.clearance_check(6):
            all_projects_button .pack(side='left', pady=(10,2),padx=5)
            insert_button       .pack(side='left', pady=(10,2),padx=5)
        self.see_project_button.pack(side='left', pady=(10,2),padx=5)

    def show_info_window(self, data):
        info_window = BasicProjectInfo(self.frame, parent=self)
        info_window.display_data(data[0])

    def show_edit_window(self, data=None):
        edit_window = EditProjectGUI(self.frame, parent=self)
        edit_window.display_data(data)

    def show_options_window(self,data):
        option_window = ProjectOptionsWindow(self.frame, parent=self)
        option_window.display_data(data)

    def see_my_projects(self):
        self.see_project_button.configure(text='ALL PROJECTS',
            command = self.see_projects)
        self.titlelabel.configure(text=f"★ MY PROJECTS ({self.user.full_name.upper()}) ★")
        self.display_data(None, lambda:get_my_project_info(self.user))
        
    def see_projects(self):
        self.see_project_button.configure(text='MY PROJECTS',
            command = self.see_my_projects)
        self.titlelabel.configure(text="★ "+PROGRAMTITLE.upper()+" ★")
        self.display_data(None, get_project_info)

    def display_data(self, data, dataset_get):
        if self.context == 'select':
            self.destroy_stop = False
        else: 
            self.destroy_stop = True
        return super().display_data(data, dataset_get)

if __name__ == '__main__':
    print(__name__)