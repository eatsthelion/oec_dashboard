###############################################################################
# project_options.py
# 
# Created: 8/25/22
# Creator: Ethan de Leon
# Purposes: 
#   - Creates the Pop-up Window for Project Options
#   - Sets up for buttons for navigation
#   - Links to the following windows:
#       - Project Schedule Window
#       - Project Status Log Window
#       - Project Documents Window
#       - Project Packages/Deliverables Window
#       - Project Budget Window
#       - Project People Assignements Window
#   - Creates an option to delete a project from the catalog
# Required Installs: None
###############################################################################
PROGRAMTITLE = 'Project Options'

from Backend.database_get import *
from Backend.database_delete import delete_project

from GUI.window_option import *

from Programs.project_budgets import ProjectBudgetsGUI
from Programs.project_engineers import ProjectEngineers
from Programs.project_schedule import ProjectScheduleGUI
from Programs.project_packages import ProjectPackagesGUI
from Programs.project_documents import ProjectDocumentsGUI
from Programs.project_status_log  import ProjectStatusGUI
from Programs.project_assignments import ProjectAssignmentsGUI

class ProjectOptionsWindow(OptionWindow):
    """A window that displays the different options of a project"""
    def __init__(self, master, **kw) -> None:
        """Internal Function. Sets up initial window settings"""
        super().__init__(master, bg='mediumorchid2', width=400, height=300,
        project_title = PROGRAMTITLE, **kw)

    def configure(self):
        """Initializes window's widgets and navigation buttons"""
        self.project_data = None
        button_width = 15
        self.button_frame = MyFrame(self.frame)
        
        
        # region Initializes navigation buttons
        self.budget_button = MyButton(self.button_frame, width=button_width, 
            text='BUDGET', command=lambda: self.show_next_window('budget'))

        self.documents_button = MyButton(self.button_frame, width=button_width, 
            text='DOC SEARCH', command=lambda: self.show_next_window('documents'))

        self.dates_button = MyButton(self.button_frame, width=button_width, 
            text='SCHEDULE', command=lambda: self.show_next_window("schedule"))

        self.status_log_button = MyButton(self.button_frame, width=button_width, 
            text='STATUS LOG', command=lambda: self.show_next_window("status"))

        self.packages_button = MyButton(self.button_frame, width=button_width,
            text='PACKAGES', 
            command=lambda: self.show_next_window("packages"))

        self.contacts_button = MyButton(self.button_frame, width=button_width,
            text='CONTACTS', command=lambda: self.show_next_window("people"))

        self.pe_button = MyButton(self.button_frame, width=button_width,
            text='PEs', command=lambda: self.show_next_window("pe"))

        self.delete_button  = MyButton(self.button_frame, bg='red', 
            font=FONT, text='DELETE PROJECT',fg='white', 
            command=self.delete_project_command)

        self.terminal = Terminal(self.frame, bg='gold2')
        # endregion 

        self.button_frame.pack(expand=1)
        self.dates_button       .grid(row=0, column=0, sticky=EW, padx=5,pady=5)
        self.status_log_button  .grid(row=0, column=1, sticky=EW, padx=5,pady=5)
        self.documents_button   .grid(row=1, column=0, sticky=EW, padx=5,pady=5)
        self.packages_button    .grid(row=1, column=1, sticky=EW, padx=5,pady=5)
        self.pe_button          .grid(row=2, column=0, sticky=EW, padx=5,pady=5)
        self.contacts_button    .grid(row=2, column=1, sticky=EW, padx=5,pady=5)
        return super().configure()

    def show_next_window(self, windowname):
        self.terminal.show_terminal()
        self.terminal.print_terminal('Loading Information...')
        if windowname == 'budget':
            next_window = self.budget_window = ProjectBudgetsGUI(
                self.parent.frame_master, parent = self)
            dataget = lambda: get_budget_info(self.data[0])
            title = 'BUDGET FOR'
        elif windowname == 'status':
            next_window = self.status_window = ProjectStatusGUI(
                self.parent.frame_master, parent = self)
            dataget = lambda: get_status_log(self.data[0])
            title = "STATUS OF"
        elif windowname == 'people':
            next_window = self.contact_window = ProjectAssignmentsGUI(
                self.parent.frame_master,parent=self)
            dataget = lambda: get_people_info(self.data[0])
            title = "CONTACTS OF"
        elif windowname == 'schedule':
            next_window = self.schedule_window = ProjectScheduleGUI(
                self.parent.frame_master, parent = self)
            dataget = lambda: get_schedule(self.data[0])
            title = "SCHEDULE OF"
        elif windowname == 'pe':
            next_window = self.schedule_window = ProjectEngineers(
                self.parent.frame_master, parent = self)
            dataget = lambda: get_project_engineers(self.data[0])
            title = "PROJECT ENGINEERS OF"
        
        elif windowname in ['documents','packages']:
            self.document_window = ProjectDocumentsGUI(
                self.parent.frame_master, parent = self)
            self.package_window = ProjectPackagesGUI(
                self.parent.frame_master, parent = self)
            if windowname == 'documents':
                next_window = self.document_window
                dataget = lambda: get_project_documents(self.data[0])
                title = "DOCUMENTS OF"
            elif windowname == 'packages':
                next_window = self.package_window
                dataget = lambda: get_packages(self.data[0])
                title = "PACKAGES OF"
        else:
            return False
        self.terminal.print_terminal('Configuring Window...')
        titletext = f'PROJECT {self.data[1]}, {self.data[6]}, {self.data[5]}'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."

        next_window.project_data = self.data
        next_window.project_data_dict = self.data_dict
        next_window.titlelabel.configure(text = f'{title} {titletext.upper()}')
        next_window.context = 'display'
        
        self.terminal.print_terminal('Populating Data table...')
        next_window.display_data(self.data, dataget)
        next_window.show_full_window()
        
        next_window.back_direction=self.show_window
        self.terminal.hide_terminal()
        self.cancel_window()
        pass

    def display_data(self, data):
        """Displays project OEC number on pop-up header"""
        self.data = data
        self.titlelabel.configure(text='PROJECT {}'.format(self.data[1]))
        if self.clearance_check(7, self.get_data('project_engineers_ids')):
            self.budget_button.grid(row=3, column=0, sticky=EW,
            padx=5,pady=5)

            self.delete_button.grid(row=3, column=1, sticky=EW, 
            padx=5,pady=5)
        else:
            self.delete_button.grid_forget()
        self.show_window()

    

    def delete_project_command(self):
        if not delete_project(self.data,self.user.user_id):
            return False
        # Refreshes display
        self.destroy_window()
        self.parent.searchwindow.refresh_page()
    
