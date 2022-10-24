from Backend.database import PROJECTDB, DB_connect

from GUI.window_datatable import *

class ProjectTaskApplicants(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Task Applicants',
        bg='royalblue1', search_col_bg='deepskyblue2', 
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions, 
        format_dict="project_task_applicants",
        **kw)
        self.task_id = None

    def configure(self):
        super().configure()
        self.hide_cancel_button()

    def leftoptions(self, master,dataset,row):
        accept_button = MyButton(master, text= 'ASSIGN',
            command = lambda m=dataset: self.assign_staff(m))
        accept_button.grid(row=0, column=0, padx=5)

    def additionalOptions(self, button_master, frame_master):
        tasklabel = MyLabel(frame_master, font=FONTBOLD, text="SELECT AN APPLICANT")
        tasklabel.pack()

    def assign_staff(self, dataset):
        DB_connect(f"""
        UPDATE project_task_assignments 
        SET assigned = 1 
        WHERE rowid = {dataset[0]}""", database=PROJECTDB)

        self.searchwindow.refresh_results()

    