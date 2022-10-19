from Backend.filesystem import FileSystem

from GUI.widgets.basics import MyButton
from GUI.data_table import DataTableWindow
from GUI.project_catalog.edit_windows.edit_document import EditDocumentGUI
from GUI.project_catalog.option_windows.dwglist_options import DWGListWindow

from Backend.database_get import get_packages

FORMATDICT = {
    1:{'title':'Item No', 'width':10},
    2:{'title':'Filename', 'width':10},
    3:{'title':'EXT', 'width':8},
    4:{'title':'Title', 'width':8},
    5:{'title':'Drawing No', 'width':10},
    6:{'title':'REV', 'width':10},
    7:{'title':'SH', 'width':10},
    8:{'title':'Description', 'width':30},
    9:{'title':'Purpose', 'width':20},
    10:{'title':'Progress', 'width':15},
    11:{'title':'Author', 'width':20},
    12:{'title':'Checked Out By', 'width':20},
    13:{'title':'Input Date', 'width':15},
    14:{'title':'Modified Date', 'width':15},
    15:{'title':'Last Modified By', 'width':20},
}
SKIPFIELDS = [0]
class ProjectDocumentsGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Documents',
        bg='royalblue1', col_color='deepskyblue2', 
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions, 
        skipfields=SKIPFIELDS,
        format_dict=FORMATDICT,
        **kw)
        self.package_id = None

    def configure(self,**kw):
        super().configure(**kw)

    def leftoptions(self, master,dataset,row):
        download_document = MyButton(master, text='  ⇩  ',
            command = lambda m=dataset[0]:
                FileSystem.deliver_project_to_desktop(
                    FileSystem.get_project_document(m)))

        update_document = MyButton(master, text='UPDATE',
            command=lambda m=dataset: 
                self.show_edit_doc_window(data=m))
        details  = MyButton(master, text='  +  ',
            command=lambda m=dataset: self.show_option_window(m))

        update_document  .grid(row=0,column=1,padx=(5,0))
        download_document.grid(row=0,column=2,padx=(5,0))
        details          .grid(row=0,column=3,padx=5) 

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
        
        self.parent.package_window.display_data(self.data, dataget)
        self.parent.package_window.show_full_window()
        self.parent.package_window.back_direction = self.parent.show_window
        self.cancel_window()

    def show_option_window(self, dataset):
        pass

    def show_dwglist_options(self):
        dwglist_window = DWGListWindow(self.frame, parent=self)
        dwglist_window.display_data(self.package_id)

    