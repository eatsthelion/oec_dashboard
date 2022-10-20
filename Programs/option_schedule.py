PROGRAMTITLE = 'Schedule Options'

from Backend.database_get import *
from Backend.database_send import project_edit_entry

from GUI.window_option import *

from Programs.project_packages import ProjectPackagesGUI
from Programs.project_task_assign import ProjectTaskAssignments
from Programs.project_task_applicants import ProjectTaskApplicants

class ScheduleOptionsWindow(OptionWindow):
    def __init__(self, master:tk, parent, **kw):
        """Initializes the schedule options window"""
        super().__init__(master, parent=parent, bg='cyan4', width=400,
        program_title = PROGRAMTITLE, height=300, **kw)
        self.data = None
        self.project_data = None

    def configure(self):
        self.button_frame = MyFrame(self.frame)
        self.packages_button = MyButton(self.button_frame,  text='SEE PACKAGES', 
            command = lambda: self.see_packages(self.data))

        self.taskpost_button = MyButton(self.button_frame)

        self.assigned_button = MyButton(self.button_frame, text='VIEW ASSIGNED',
            command = self.show_assigned_window)
        
        self.see_app_button = MyButton(self.button_frame, text='VIEW TASK APPLICANTS',
            command=self.see_task_applicants)

        self.delete_button = MyButton(self.button_frame, bg='red', fg='white',
             text='DELETE EVENT')
        
        self.button_frame.pack(expand=1)

        self.assigned_button.grid(row=0, column=0, pady=(5,0), sticky=EW)
        self.taskpost_button.grid(row=1, column=0, pady=(5,0), sticky=EW)
        self.see_app_button.grid(row=2, column=0, pady=(5,0), sticky=EW)
        self.packages_button.grid(row=3, column=0, pady=(5,0), sticky=EW)
        self.delete_button.grid(row=4, column=0, pady=(5,0), sticky=EW)

        return super().configure()

    def display_data(self, data, project_data):
        self.data = data
        self.project_data = project_data
        self.titlelabel.configure(text=self.data[1])
        if self.data[9] == 0:
            self.taskpost_button.configure(text='POST TO TASKBOARD',
            command=self.post_to_taskboard)
            self.see_app_button.grid_remove()
        else:
            self.taskpost_button.configure(text='REMOVE FROM TASKBOARD',
            command=self.remove_from_taskboard)
            self.see_app_button.configure(text=f'VIEW TASK APPLICANTS ({self.data[4]})')
            self.see_app_button.grid()
        self.show_window()

    def post_to_taskboard(self):
        if not messagebox.askyesno('Post to Taskboard?', 
        'Do you want to post this task to the taskboard?'):
            return False

        datapair = [(self.data[9], 1, 'taskboard posting', 'taskboard')]
        
        project_edit_entry(self.project_data[0], self.data[0], 'project_dates',
        PROJECTDB, self.data[1], "TASKBOARD POST",datapair, user=self.user)
        self.cancel_window()
        self.parent.searchwindow.refresh_page()
        
    def remove_from_taskboard(self):
        if not messagebox.askyesno('Remove from Taskboard?', 
        'Do you want to remove this task from the taskboard?'):
            return False

        datapair = [(self.data[9], 0, 'taskboard posting', 'taskboard')]
        
        project_edit_entry(self.project_data[0], self.data[0], 'project_dates',
        PROJECTDB, self.data[1], "TASKBOARD POST REMOVAL",datapair, user=self.user)
        self.cancel_window()
        self.parent.searchwindow.refresh_page()

    def see_packages(self, dataset):
        searchwindow = ProjectPackagesGUI(self.parent.master, parent = self)
        db_function = get_event_packages
        titletext = f'PACKAGES FOR EVENT: {dataset[1]}'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."
        searchwindow.titlelabel.configure(text = titletext)

        # Sends the new dataset to the pop-up SearchWindow 
        searchwindow.context = 'view event packages'
        searchwindow.display_data(self.project_data,
            lambda: db_function(self.data[0]), event_id = self.data[0])
        
        # Changes windows to display
        searchwindow.show_full_window()
        self.cancel_window()

        # Sets the back button of new window to go to previous window
        searchwindow.back_direction = self.show_window

    def see_task_applicants(self):
        searchwindow = ProjectTaskApplicants(self.parent.master, parent=self)
        db_function = get_task_applicants
        titletext = f'{self.data[1].upper()}'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."
        searchwindow.titlelabel.configure(text = titletext)

        # Sends the new dataset to the pop-up SearchWindow 
        searchwindow.context = 'view task applicants'
        searchwindow.display_data(self.project_data,
            lambda: db_function(self.data[0]))
        
        # Changes windows to display
        searchwindow.show_full_window()
        self.cancel_window()
        searchwindow.back_direction = self.show_window

    def show_assigned_window(self):
        searchwindow = ProjectTaskAssignments(self.parent.master, parent=self)

        db_function = get_assigned_staff
        titletext = f'OEC STAFF FOR {self.data[1].upper()}'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."
        searchwindow.titlelabel.configure(text = titletext)

        # Sends the new dataset to the pop-up SearchWindow
        dataset = db_function(self.data[0])
        searchwindow.context = 'view'
        searchwindow.task_id = self.data[0]
        searchwindow.display_data(self.project_data,
            lambda: db_function(self.data[0]))
        
        # Changes windows to display
        searchwindow.show_full_window()
        self.parent.cancel_window()
        self.cancel_window()

        # Sets the back button of new window to go to previous window
        searchwindow.back_direction = self.show_windows

    def show_windows(self):
        self.parent.show_full_window()
        self.show_window()

    def assign_staff(self, data):
        DB_connect(f"""
        INSERT INTO project_task_assignments VALUES
        ({self.data[0]}, {data[0]}, 0)
        """, database=PACKAGEDB)
        self.cancel_window()
        self.parent.show_full_window()
        self.parent.searchwindow.refresh_page()