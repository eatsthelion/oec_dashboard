from Backend.database import PROJECTDB, DB_connect
from Backend.database_get import get_my_applied_tasks, get_my_taskboard, get_taskboard
from GUI.GUI_Mains import FONTBOLD
from GUI.project_catalog.info_windows.schedule_info_window import ScheduleInfoWindow
from GUI.project_catalog.info_windows.project_info_window import BasicProjectInfo
from GUI.widgets.terminal import Terminal
from GUI.data_table import DataTableWindow
from GUI.widgets.basics import *

PROGRAMTITLE = "OEC Taskboard"

SKIPFIELDS = [0, 6, 9, 11, 13]
FORMATDICT = {
    1:{'title':'Task', 'width':20},
    2:{'title':'Details', 'width':30},
    3:{'title':'Task Type', 'width':10},
    4:{'title':'Priority', 'width':15, 'format':'hml'},
    5:{'title':'Difficulty', 'width':15, 'format':'hml'},
    6:{'project_id'},
    7:{'title':'OEC No', 'width':20},
    8:{'title':'Project Title', 'width':25},
    9:{'pe_ids'},
    10:{'title':'Project Engineer(s)', 'width':20},
    11:{'assigned_ids'},
    12:{'title':'Assigned Staff', 'width':25},
    13:{'applied_ids'},
}
class Taskboard(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, entrylimit = 15, rowheight=4,
        sortfunction=self.sortfunction,
        leftoptions = self.leftoptions, 
        additional_windows = self.additonalOptions, 
        skipfields=SKIPFIELDS, format_dict=FORMATDICT,
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

    def leftoptions(self, master,dataset,row):
        apply_button = MyButton(master, text='APPLY', 
            command=lambda m=dataset: self.apply_for_task(m))
        task_info_button = MyButton(master, text='TASK INFO',
            command=lambda m=dataset: self.show_schedule_info(dataset))
        project_info_button = MyButton(master, text='PROJECT INFO',
            command=lambda m=dataset: self.show_project_info(dataset))
        engineerlist = []
        assignedlist = []
        appliedlist = []
        if type(dataset[6])==str:
            dset = dataset[6].split(',')
            for d in dset:
                try: 
                    engineerlist.append(int(d))
                except:
                    pass
        if type(dataset[8])==str:
            dset = dataset[8].split(',')
            for d in dset:
                try: 
                    assignedlist.append(int(d))
                except:
                    pass
        if type(dataset[10])==str:
            dset = dataset[10].split(',')
            for d in dset:
                try: 
                    appliedlist.append(int(d))
                except:
                    pass

        if self.user.user_id in assignedlist:
            apply_button.configure(state=DISABLED, text='ASSIGNED', command=None)
        elif self.user.user_id in appliedlist:
            apply_button.configure(text='RESCIND APP', 
            command=lambda m=dataset: self.delete_application(m))
        elif self.user.user_id in engineerlist:
            apply_button.configure(state=DISABLED, text='ASSIGNED AS PE', command=None)
        apply_button.grid(row=0, column=0, padx=5, columnspan=2, sticky=EW)
        task_info_button.grid(row=1, column=0, padx=(5,0), pady=5)
        project_info_button.grid(row=1, column=1, padx=5, pady=5)

    def sortfunction(self, sortby, dataset):
        if sortby == 'SORT BY ITEM (A-Z)': 
            named_entries = []
            nameless_entries = []
            for data in dataset:
                if data[1] in ['', None]: 
                    nameless_entries.append(data)
                    continue
                named_entries.append(data)
            named_entries.sort(key=lambda i:i[1])
            dataset = named_entries + nameless_entries
        elif sortby == 'SORT BY ITEM (Z-A)': 
            dataset.sort(key=lambda i:i[1],reverse=True)
        elif sortby == 'SORT BY CODE': 
            dataset.sort(key=lambda i:i[2])
        return dataset

    def additonalOptions(self, button_master, frame_master):
        self.my_tasks_button = MyButton(button_master, text='MY TASKS',
            command=self.see_my_tasks)
        self.all_tasks_button = MyButton(button_master, text='POSTED TASKS',
            command=self.see_all_tasks)
        self.applied_button = MyButton(button_master, text='APPLIED TASKS',
            command=self.see_my_applied_tasks)
        
        self.all_tasks_button.pack(side=LEFT, padx=5, pady=5)
        self.my_tasks_button.pack(side=LEFT, padx=(0,5), pady=5)
        self.applied_button.pack(side=LEFT, padx=(0,5), pady=5)

    def apply_for_task(self, dataset):
        if not messagebox.askyesno('Apply for Task', 
        "Do you want to apply for this task?"):
            return False 
            
        DB_connect(f"""
        INSERT INTO project_task_assignments VALUES
        ({dataset[0]}, {self.user.user_id}, 0)
        """, database=PROJECTDB)

        self.searchwindow.refresh_page()

    def delete_application(self, dataset):
        if not messagebox.askyesno('Remove Application', 
        "Do you want to remove your application for this task?"):
            return False 
            
        DB_connect(f"""
        DELETE FROM project_task_assignments 
        WHERE project_task_id =  {dataset[0]}
        AND project_person_id = {self.user.user_id}
        """, database=PROJECTDB)

        self.searchwindow.refresh_page()

    def see_my_applied_tasks(self):
        datafunction = lambda: get_my_applied_tasks(self.user.user_id)
        self.titlelabel.configure(
            text="★ "+f'MY TASK APPLICATIONS ({self.user.full_name})'+" ★")
        self.display_data(None, datafunction)

    def see_my_tasks(self):
        datafunction = lambda: get_my_taskboard(self.user.user_id)
        self.titlelabel.configure(
            text="★ "+f'MY ASSIGNED TASKS ({self.user.full_name})'+" ★")
        self.display_data(None,datafunction)

    def see_all_tasks(self):
        datafunction = lambda: get_taskboard(self.user.user_id)
        self.titlelabel.configure(text="★ "+PROGRAMTITLE.upper()+" ★")
        self.display_data(None, datafunction)

    def show_schedule_info(self, dataset):
        infowindow = ScheduleInfoWindow(self.frame)
        infowindow.display_data(dataset[0])

    def show_project_info(self, dataset):
        infowindow = BasicProjectInfo(self.frame)
        infowindow.display_data(dataset[6])