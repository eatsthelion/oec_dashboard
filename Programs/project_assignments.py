###############################################################################
# project_assignments.py
# 
# Created: 10/19/22
# Creator: Ethan de Leon
# Purposes:
#   - Organizes and displays the contacts of a project
#   - Connects to 
#       - edit_project_people.py for contact inserting and editing
###############################################################################
from GUI.window_datatable import *
from Programs.edit_project_people import EditPeopleGUI

class ProjectAssignmentsGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Contacts',
        bg='purple2',col_color='magenta2',
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions, 
        format_dict='project_people',
        **kw)

    def configure(self, **kw):
        return super().configure(**kw)
    
    def leftoptions(self, master,dataset,row):
        see_project_info=MyButton(master,text='INFO')
        update_person = MyButton(master, text='UPDATE', 
            command=lambda m=dataset: 
                self.edit_people_window.display_data(self.data[0], data=m))
        details  = MyButton(master, text='  +  ',
            command=lambda m=dataset: self.show_option_window(m))

        see_project_info    .grid(row=0,column=0,padx=(5,0))
        update_person      .grid(row=0,column=1,padx=(5,0))
        details             .grid(row=0,column=3,padx=5)
        pass

    def additionalOptions(self, button_master, frame_master):
        self.edit_people_window = EditPeopleGUI(frame_master, parent=self)
        insert_button = MyButton(button_master, text='NEW ROLE',
            command = lambda: self.edit_people_window.display_data(self.data[0]))
        multi_update_button = MyButton(button_master, 
            text='UPDATE ALL ASSIGNMENTS')   
        all_schedule_button = MyButton(button_master, 
            text='EXPORT TO EXCEL')

        all_schedule_button .pack(side='left', pady=(10,2),padx=5)
        insert_button       .pack(side='left', pady=(10,2),padx=5)
        multi_update_button .pack(side='left', pady=(10,2),padx=5)