from Backend.database_get import get_docs_in_package, get_project_documents
from Backend.filesystem import FileSystem

from GUI.window_datatable import *

from Programs.option_packages import PackageOptionsWindow
from Programs.edit_packages import EditPackagesGUI

SKIPFIELDS = [0, 4, 5]
FORMATDICT = {
    1:{'title':'Package',               'width':30},
    2:{'title':'Description',           'width':15},
    3:{'title':'Package Type',          'width':15},
    4:{'deletable'},
    5:{'event_id'},
    6:{'Access':'Event',                'width':25},
    7:{'title':'Access',                'width':25},
    8:{'title':'Forecast Date',         'width':15, 'format':'date'},
    9:{'title':'Submittal Date',        'width':15, 'format':'date'},
    10:{'title':'Creation Date',        'width':15, 'format':'date'},
    11:{'title':'Modify Date',          'width':15, 'format':'date'},
    12:{'title':'Last Modified By',     'width':15, 'format':'date'},
}

class ProjectPackagesGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Packages',
        bg='cyan3', col_color='cyan2', 
        leftoptions = self.leftoptions, 
        additional_windows = self.additionalOptions, 
        skipfields=SKIPFIELDS,
        format_dict=FORMATDICT,
        **kw)
        self.event_id = ''

    def configure(self,**kw):
        super().configure(**kw)

    def leftoptions(self, master,dataset,row):
        see_contents=MyButton(master, text='CONTENTS',
            command=lambda m=dataset: 
                self.show_package_documents_window_full(m))

        update_package = MyButton(master, text='UPDATE', 
            command=lambda m=dataset:self.show_edit_window(m))

        download_package = MyButton(master, text='  ⇩  ',
            command = lambda m=dataset[0]:
                FileSystem.deliver_project_to_desktop(
                    FileSystem.get_package_folder(m)))

        details  = MyButton(master, text='  +  ', 
            command = lambda m=dataset: self.show_option_window(m))

        see_contents        .grid(row=0,column=0,padx=(5,0))
        update_package      .grid(row=0,column=1,padx=(5,0))
        download_package    .grid(row=0,column=3,padx=(5,0))
        details             .grid(row=0,column=4,padx=5)
        pass

    def additionalOptions(self, button_master, frame_master):
        insert_button = MyButton(button_master, text='NEW PACKAGE/DELIVERABLE', 
            command=self.show_edit_window)
        multi_update_button = MyButton(button_master, text='SEE DOCUMENTS',
            command=self.show_document_window_full)   
        all_packages_button = MyButton(button_master, 
            text='ALL PACKAGES/DELIVERABLES')

        all_packages_button .pack(side='left', pady=(10,2),padx=5)
        insert_button       .pack(side='left', pady=(10,2),padx=5)
        multi_update_button .pack(side='left', pady=(10,2),padx=5)

    def show_document_window_full(self):
        dataget = lambda: get_project_documents(self.data[0])
        
        self.parent.document_window.display_data(self.data, dataget)
        self.parent.document_window.show_full_window()
        self.parent.document_window.back_direction = self.parent.show_window
        self.cancel_window()

    def show_package_documents_window_full(self, dataset):      
        from Programs.project_documents import ProjectDocumentsGUI  
        searchwindow = ProjectDocumentsGUI(self.master, parent=self)
        db_function = get_docs_in_package

        # Changes the title of the new window
        titletext = f'DOCUMENTS OF {dataset[1].upper()} FOR PROJECT {self.data[1]}'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."
        searchwindow.titlelabel.configure(text = titletext)

        # Sends the new dataset to the pop-up SearchWindow
        searchwindow.package_id = dataset[0]
        searchwindow.context = 'package docs'
        searchwindow.display_data(self.data, lambda: db_function(dataset[0]))
        
        # Changes windows to display
        searchwindow.show_full_window()
        self.cancel_window()

        # Sets the back button of new window to go to previous window
        searchwindow.back_direction = self.show_full_window

    def display_data(self, data, datasetget, event_id = ''):
        self.event_id = event_id
        return super().display_data(data, datasetget)

    def go_back(self):
        self.parent.document_window.destroy_window()
        return super().go_back()

    def show_edit_window(self, dataset=None):
        edit_window = EditPackagesGUI(self.frame, parent=self)
        edit_window.display_data(self.data[0], dataset, event_id=self.event_id)
    def show_option_window(self,dataset): 
        options_window = PackageOptionsWindow(self.frame, parent=self)
        options_window.display_data(dataset, self.data)