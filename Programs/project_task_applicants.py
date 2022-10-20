from Backend.database import PROJECTDB, DB_connect

from GUI.window_datatable import *

FORMATDICT = {
    1:{'title':'Applicant', 'width':20},
    2:{'title':'Total Active Tasks', 'width':20},
    3:{'title':'Total Active Projects', 'width':20},
}
SORTOPTIONS = ['SORT BY NEWEST', 'SORT BY OLDEST']
SKIPFIELDS = [0]

class ProjectTaskApplicants(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Task Applicants',
        bg='royalblue1', search_col_bg='deepskyblue2', 
        left_options = self.leftoptions, 
        additional_windows = self.additionalOptions, 
        skipfields=SKIPFIELDS,
        format_dict=FORMATDICT,
        **kw)
        self.task_id = None

    def configure(self):
        super().configure()
        self.hide_cancel_button()

    def leftoptions(self, master,dataset,row):
        accept_button = MyButton(master, text= 'ASSIGN',
            command = lambda m=dataset: self.assign_staff(m))
        accept_button.grid(padx=5)

    def additionalOptions(self, button_master, frame_master):
        tasklabel = MyLabel(frame_master, font=FONTBOLD, text="SELECT AN APPLICANT")
        tasklabel.pack()

    def assign_staff(self, dataset):
        DB_connect(f"""
        UPDATE project_task_assignments 
        SET assigned = 1 
        WHERE rowid = {dataset[0]}""", database=PROJECTDB)

        self.searchwindow.refresh_results()

    