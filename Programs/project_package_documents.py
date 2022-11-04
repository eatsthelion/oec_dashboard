###############################################################################
# project_package_documents.py
# 
# Created: 10/19/22
# Creator: Ethan de Leon
# Purposes:
#   - Organizes and displays the change orders of a purchase order
#   - Allows users to check in and out documents
#   - Connects to 
#       - option_dwglist.py
#       - edit_document.py
###############################################################################

from Backend.database import DOCDB
from Backend.filesystem import FileSystem

from GUI.window_datatable import *

from Programs.edit_document import EditDocumentGUI
from Programs.option_dwglist import DWGListWindow

from Backend.database_get import get_packages
from Backend.database_send import project_edit_entry

class PackageDocumentsGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Documents',
        bg='royalblue1', col_color='deepskyblue2', 
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions, 
        format_dict='package_documents',
        **kw)
        self.package_id = None
        self.project_data = None

    def configure(self,**kw):
        super().configure(**kw)

    def leftoptions(self, master,dataset,row):
        download_document = MyButton(master, text='  ⇩  ',
            command = lambda m=dataset[0]:
                FileSystem.deliver_project_to_desktop(
                    FileSystem.get_project_document(m)))

        check_out = MyButton(master, text='CHECKOUT', 
            command = lambda m=dataset: self.toggle_checkout(m))

        update_document = MyButton(master, text='UPDATE',
            command=lambda m=dataset: 
                self.show_edit_doc_window(data=m))
        details  = MyButton(master, text='  +  ',
            command=lambda m=dataset: self.show_option_window(m))

        check_out        .grid(row=0,column=0,padx=(5,0))
        update_document  .grid(row=0,column=1,padx=(5,0))
        download_document.grid(row=0,column=2,padx=(5,0))
        details          .grid(row=0,column=3,padx=5) 

        if self.get_data("checked_out_by", dataset):
            if self.clearance_check(100, self.get_data("checked_out_by", dataset)):
                check_out.configure(text = 'CHECK IN')
            elif self.clearance_check(7, 
                self.get_data('project_engineers_ids', self.data, self.project_data_dict)):
                check_out.configure(text = 'CHECKED OUT',
                    command = lambda m=dataset: self.toggle_checkout(m))
            else:
                update_document.grid_remove()
                check_out.configure(text = 'CHECKED OUT', bg='gold2',
                    command = lambda:
                    messagebox.showerror('Document is Checked Out', 
                    f'The document is currently checked out by {dataset[self.data_dict["checked_out_name"]]}'))
        return   

    def toggle_checkout(self, dataset):
        if dataset[self.data_dict['checked_out_by']] == 0:
            if not messagebox.askyesno('Check out?', 
            f'Would you like to check in this document? \n\n{dataset[self.data_dict["filename"]]}'):
                return False
            checkout = self.user.user_id

        else:
            if not messagebox.askyesno('Check in?', 
            f'Would you like to check in this document? \n\n{dataset[self.data_dict["filename"]]}'):
                return False
            checkout = 0

        datapair = [(checkout, 'checked out', 'checked_out_by')]

        project_edit_entry(self.data[0], dataset[0], 
        "documents", DOCDB, 'check out','CHECKOUT', 
        dataset, self.data_dict, datapair)

        self.searchwindow.refresh_page()

    def additionalOptions(self, button_master, frame_master):
        insert_button = MyButton(button_master, text='UPLOAD',
            command = self.show_edit_doc_window)
        #packages_button = MyButton(button_master, text='SEE PACKAGES',
        #    command=self.show_package_window_full)   
        drawinglist_button = MyButton(button_master, text='DWG LIST',
            command = self.show_dwglist_options)

        #all_documents_button .pack(side='left', pady=(10,2),padx=5)
        insert_button.pack(side='left', pady=(10,2),padx=5)
        drawinglist_button.pack(side='left', pady=(10,2),padx=5)
        #packages_button .pack(side='left', pady=(10,2),padx=5)

    def show_edit_doc_window(self, data = None):
        edit_doc_window = EditDocumentGUI(self.frame, parent=self)
        edit_doc_window.display_data(self.package_id, data)

    def show_package_window_full(self):
        dataget = lambda: get_packages(self.data[0])
        self.parent.package_window.project_data = self.data
        self.parent.package_window.project_data_dict = self.data_dict
        self.parent.package_window.display_data(self.data, dataget)
        self.parent.package_window.show_full_window()
        self.parent.package_window.back_direction = self.parent.show_window
        self.cancel_window()

    def show_option_window(self, dataset):
        pass

    def show_dwglist_options(self):
        dwglist_window = DWGListWindow(self.frame, parent=self)
        dwglist_window.display_data(self.package_id)

    