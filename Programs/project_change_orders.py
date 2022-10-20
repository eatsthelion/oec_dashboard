###################################################################################################
# catalog_budgets.py
# 
# Created: 9/09/22
# Creator: Ethan de Leon
# Purposes:
#   - Organize the database project budgets
###################################################################################################

from Backend.database_delete import delete_change_order
from GUI.window_datatable import *
from Programs.edit_change_order import EditChangeOrderGUI

PROGRAMTITLE = "Change Order Catalog"
COLUMNTITLES = [
    'rowid', 'Change Order No', 'Description', 
    'Proposed Amount', 'Contract Amount', 'Proposed Date', 'Contracted Date'
    ]
COLUMNWIDTHS = [
    1 , 8 , 20, 
    10, 10, 15, 15    
    ]
SORTOPTIONS = ['SORT BY NEWEST', 'SORT BY OLDEST']
SKIPFIELDS = [0]
FORMATDICT = {
    1:{'title':'Change Order No',       'width':8},
    2:{'title':'Description',           'width':20},
    3:{'title':'Proposed Amount',       'width':10, 'format':'dollar'},
    4:{'title':'Contract Amount',       'width':10, 'format':'dollar'},
    5:{'title':'Proposed Date',         'width':15, 'format':'date'},
    6:{'title':'Contracted Date',       'width':15, 'format':'date'},
}

class ProjectChangeOrders(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Change Orders',
        bg='royalblue1', col_color='deepskyblue2', 
        left_options = self.leftoptions, 
        additional_popups = self.additonalOptions, 
        columntitles=COLUMNTITLES, columnwidths=COLUMNWIDTHS, 
        skipfields=SKIPFIELDS,
        **kw)
        self.project_id = None
        self.po_id = None

    def configure(self):
        super().configure()
        self.hide_cancel_button()

    def additionalOptions(self, button_master, frame_master):
        insert_button = MyButton(button_master, text='NEW CHANGE ORDER',
            command = self.show_edit_window)
        insert_button .pack(side='left', pady=(10,2),padx=5)

    def leftoptions(self, master,dataset,row):
        editbutton = MyButton(master, text='EDIT', 
            command = lambda m=dataset: self.show_edit_window(m))
        delete_button = MyButton(master, text ='DELETE', bg='red',
            command=lambda m=dataset: self.delete_co(m))

        delete_button.grid(row=0, column = 1, padx=5, pady=5)
        editbutton.grid(row=0,column=0, padx=5, pady=5)

    def sortfunction(self, sortby, dataset):
        if sortby == 'SORT BY FILE NAME (A-Z)': 
            named_entries = []
            nameless_entries = []
            for data in dataset:
                if data[2] in ['', None]: 
                    nameless_entries.append(data)
                    continue
                named_entries.append(data)
            named_entries.sort(key=lambda i:i[2])
            dataset = named_entries + nameless_entries
        elif sortby == 'SORT BY OEC NUMBER': dataset.sort(key=lambda i:i[2],reverse=True)
        
        return dataset 

    

    def show_edit_window(self, data=None):
        self.edit_co_window = EditChangeOrderGUI(self.frame, parent=self)
        self.edit_co_window.display_data(self.project_id, self.po_id, data)

    def delete_co(self, dataset):
        """Deletes a change order from showing up in the Catalog. The data
        still exists within our systems, but it will not appear within
        the application."""
        delete_change_order(dataset, self.project_id)

        # Refreshes display
        self.searchwindow.refresh_page()