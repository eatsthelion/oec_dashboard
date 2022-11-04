###############################################################################
# option_dwglist.py
# 
# Created: 10/19/22
# Creator: Ethan de Leon
# Purposes:
#   - Displays the options for drawing lists
#   - Creates a drawing list based on package contents
#   - Updates package contents to reflect information from a drawing list
###############################################################################

PROGRAMTITLE = 'Document Options'

from Backend.database_get import *
from Backend.database_delete import delete_project_document

from GUI.window_option import *

from Programs.catalog_projects import ProjectCatalog
from Programs.project_packages import ProjectPackagesGUI

class DocOptionsWindow(OptionWindow):
    def __init__(self, master, **kw):
        super().__init__(master, bg='cyan4', width=400, height=200, 
        program_title = PROGRAMTITLE, **kw)
        self.data = None #document data
        self.project_data = None
        self.package_data = None
        self.select_project_data = None
        self.select_package_data = None

        self.copy_to_project_button = MyButton(self.frame, 
        text='COPY TO ANOTHER PROJECT',
        command=lambda: self.move_document_command('project'))
        self.move_to_project_button = MyButton(self.frame, 
        text='MOVE TO ANOTHER PROJECT',
        command=lambda: self.move_document_command('project'))

        self.copy_to_package_button = MyButton(self.frame, 
        text='COPY TO ANOTHER PACKAGE',
        command=lambda: self.copy_document_command('package'))
        self.move_to_package_button = MyButton(self.frame, 
        text='MOVE TO ANOTHER PACKAGE',
        command=lambda: self.move_document_command('package'))

        self.deletebutton = MyButton(self.frame, text='DELETE',
        command=lambda: self.delete_document_command())
        
        self.copy_to_project_button.pack(padx=5, pady=5, expand = 1, sticky=EW)
        self.move_to_project_button.pack(padx=5, pady=5, expand = 1, sticky=EW)
        self.copy_to_package_button.pack(padx=5, pady=5, expand = 1, sticky=EW)
        self.move_to_package_button.pack(padx=5, pady=5, expand = 1, sticky=EW)
        self.deletebutton.pack(padx=5, pady=5, expand = 1, sticky=EW)

    def display_data(self, data):
        self.data = data 
        self.show_window()

    def copy_document_command(self, start='project'):
        if start == 'project':
            self.show_projects_window()
        else:
            self.show_packages_window()
        self.process = 'copy'

    def move_document_command(self, start='project'):
        self.copy_document_command(start=start)
        self.process = 'move'
        pass

    def delete_document_command(self, confirm=True):
        if confirm:
            if messagebox.askyesno('Delete Document?',
            f'Are you sure you want to delete this document?\n\n{self.data[1]}'):
                return False
        delete_project_document(self.data[0], self.data[1])
        pass

    def show_projects_window(self):
        self.select_project_data = None
        catalog = ProjectCatalog(self.parent.master, parent = self)
        catalog.context = 'select'
        catalog.display_data(self.project_data)
        catalog.show_full_window()
        catalog.back_direction = self.show_windows
        self.cancel_windows()
        pass

    def show_packages_window(self, project_id=None):
        catalog = ProjectPackagesGUI(self.parent.master, parent=self)
        catalog.context = 'select'
        if not project_id:
            dataget = lambda: get_packages(self.project_data[0])
        else:
            dataget = lambda: get_packages(project_id)
        catalog.display_data(self.project_data, dataget)

        catalog.show_full_window()
        catalog.back_direction = self.show_windows
        self.cancel_windows()

    def select_project(self, dataset):
        self.select_package_data = None
        self.select_project_data = dataset
        self.show_packages_window(dataset[0])

    def select_package(self, dataset):
        self.select_package_data = dataset
        if self.process == 'copy':
            self.copy_doc()
        elif self.process == 'move':
            self.move_doc()

        self.parent.searchwindow.refresh_page()
        self.go_back()
    

    def copy_doc(self):
        if (self.select_project_data == None) or (self.project_data==None):
            if self.select_package_data[0] == self.package_data[0]:
                messagebox.showerror('Same Document', 
                "Document already exists")
                return False
        elif (self.select_project_data[0] == self.select_project_data[0]) and (
            self.select_package_data[0] == self.package_data[0]):
                messagebox.showerror('Same Document', 
                "Document already exists")
                return False

    def move_doc(self):
        self.copy_doc()
        self.delete_document_command(confirm=False)

    def show_windows(self):
        self.show_window()
        self.parent.show_full_window()

    def cancel_windows(self):
        self.cancel_window()
        self.parent.cancel_window()

    
