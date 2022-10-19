from GUI.widgets.basics import MyButton
from GUI.data_table import DataTableWindow
from GUI.project_catalog.edit_windows.edit_project_people import EditPeopleGUI

SKIPFIELDS = [0]
FORMATDICT = {
    1:{'title':'Name', 'width':20},
    2:{'title':'Role', 'width':20},
    3:{'title':'Clearance', 'width':15},
    4:{'title':'Orginization', 'width':15},
    5:{'title':'Email', 'width':15},
    6:{'title':'Phone', 'width':15},
    7:{'title':'Input Date', 'width':15 , 'format':'date'},
    8:{'title':'Modify Date', 'width':15, 'format':'date'},
}

class ProjectAssignmentsGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Contacts',
        bg='purple2',col_color='magenta2',
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions, 
        skipfields=SKIPFIELDS,
        format_dict=FORMATDICT,
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