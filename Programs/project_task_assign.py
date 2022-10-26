PROGRAMTITLE = "Task Applicants"

from Backend.database import PROJECTDB, DB_connect
from Backend.database_get import get_active_employees

from GUI.window_datatable import *

from Programs.catalog_users import EmployeeDatabase

class ProjectTaskAssignments(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Task Assignments',
        bg='royalblue1', col_color='deepskyblue2', 
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions,
        format_dict="project_task_assignments",
        **kw)
        self.task_id = None

    def configure(self):
        super().configure()
        self.hide_cancel_button()

    def leftoptions(self, master,dataset,row):
        remove_button = MyButton(master, text= 'REMOVE',
            command = lambda m=dataset: self.remove_staff(m))
        remove_button.grid(padx=5)

    def additionalOptions(self, button_master, frame_master):
        select_staff_button = MyButton(frame_master, text="SELECT STAFF", 
        command=self.show_assign_staff_window)
        select_staff_button.pack(padx=5)

    def remove_staff(self, dataset):
        if not messagebox.askyesno('Remove Staff Assignment', 
        f"Are you sure you want to remove {dataset[1]} from this task assignment?"):
            return False

        DB_connect(
            f"""DELETE FROM project_task_assignments 
            WHERE project_task_id = {self.task_id}
            AND project_person_id = {dataset[0]}""", database = PROJECTDB)

        self.searchwindow.refresh_page()

    def show_assign_staff_window(self):
        searchwindow = EmployeeDatabase(
            self.master, parent=self)

        db_function = get_active_employees
        titletext = f'OEC STAFF FOR {self.data[1].upper()}'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."
        searchwindow.titlelabel.configure(text = titletext)

        # Sends the new dataset to the pop-up SearchWindow
        searchwindow.sender = self.assign_staff
        dataset = db_function()
        searchwindow.context = 'select'
        searchwindow.display_data(dataset,  lambda: db_function())
        
        # Changes windows to display
        searchwindow.show_full_window()
        self.cancel_window()

        # Sets the back button of new window to go to previous window
        searchwindow.back_direction = self.show_full_window

    def assign_staff(self, dataset):
        duplicate = DB_connect(f"""\
            SELECT * FROM project_task_assignments 
            WHERE project_task_id = {self.task_id} 
            AND project_person_id = {dataset[0]}""", database=PROJECTDB)
        if len(duplicate)>0:
            if duplicate[0][2] == 1:
                messagebox.showerror('Already Assigned', 
                'This person is already assigned to the task')
                return False
            else: 
                DB_connect(f"""
                UPDATE project_task_assignments 
                SET assigned = 1 
                WHERE project_person_id = {dataset[0]}
                AND project_task_id = {self.task_id}""", database=PROJECTDB)
        else:
            DB_connect(f"""
            INSERT INTO project_task_assignments VALUES
            ({self.task_id}, {dataset[0]}, 1)
            """, database=PROJECTDB)
            self.show_full_window()
        self.searchwindow.refresh_page()