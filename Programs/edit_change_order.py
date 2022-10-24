PROGRAMTITLE = 'Change Order Edits'

from tkinter import messagebox
from datetime import datetime

from Backend.database import  DBTIME, USERTIME, DB_connect, PROJECTDB
from Backend.database_send import project_input_entry, project_edit_entry

from GUI.window_edit import *

class EditChangeOrderGUI(EditWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='seagreen3',width=600, height=400, 
        program_title = PROGRAMTITLE, **kw)
        self.dataset_len = 0
        self.project_id = None
        self.po_id = None

    def configure(self):
        ew=25 
        self.entryframe  = MyFrame(self.frame, bg=self.bg)
        self.description_entry = MyEntry(self.entryframe, width=ew)
        self.proposed_entry = MyEntry(self.entryframe, width=ew)
        self.contracted_entry = MyEntry(self.entryframe, width=ew)        
        
        self.proposed_date_entry = DateEntry(self.entryframe)
        self.contract_date_entry = DateEntry(self.entryframe)

        self.datapairs = [
            ("Description:", self.description_entry),
            ("Proposed Amount:", self.proposed_entry),
            ("Contracted Amount:", self.contracted_entry),
            ("Proposed Date:", self.proposed_date_entry),
            ("Contract Date:", self.contract_date_entry),
        ]

        for row, pair in enumerate(self.datapairs):
            label = MyLabel(self.entryframe, text=pair[0])
            label.grid(row=row, column = 0, padx=5, pady=(5,0), sticky=W)
            pair[1].grid(row=row, column = 1, padx=5, pady=(5,0), sticky=EW)

        self.enterbutton = MyButton(self.frame, command=self.enter_command)
        self.entryframe.pack(expand=1, padx=5)
        self.enterbutton.pack(fill='x', padx=5, pady=5)
        
        return super().configure()

    def enter_command(self):
        description = self.description_entry.get()
        proposed = self.proposed_entry.get()
        contracted = self.contracted_entry.get()
        proposed_date = self.proposed_date_entry.get()
        contracted_date = self.contract_date_entry.get()

        try:
            proposed = float(proposed)
        except:
            proposed = ''
        try:
            contracted = float(contracted)
        except:
            contracted = ''

        # Input Validation
        required = []
        for attribute in required:
            if attribute == '':
                messagebox.showerror('Missing Info', 
                'All required* fields must be filled before entry.')
                return

        if self.context == 'insert':
            new_co = DB_connect(f"""SELECT MAX(change_order_number) 
                FROM change_order_log WHERE purchase_order = {self.po_id}""",
                database=PROJECTDB)[0][0]
            if  not new_co: 
                new_co = 1
            else:
                new_co = int(new_co) + 1

            insert_str = f"""'{self.po_id}', '{new_co}', '{description}', 
                '{proposed}', '{contracted}', '{proposed_date}', 
                '{contracted_date}'"""

            status_updates = f"New Change Order No. {new_co} for PO.ID {self.po_id} was created.\n"
            if proposed_date!='':
                fd = proposed_date.strftime(USERTIME)
                status_updates+=f"Change Order {new_co}'s proposal was submitted on {fd}\n"
            if contracted_date!='':
                ad = contracted_date.strftime(USERTIME)   
                status_updates+=f"Change Order {new_co}'s contract was recieved on {ad}\n"

            project_input_entry(self.project_id, 'change_order_log', PROJECTDB,
                insert_str, status_updates, 'NEW CHANGE ORDER', user=self.user)
            self.parent.searchwindow.refresh_results()
            
        elif self.context == 'modify':
            datapairs = [
                (description, 'description', 'description'), 
                (proposed, 'proposed amount', 'change_order_submitted'),
                (contracted, 'contracted amount', 'change_order_acceptance'),
            ]

            datepairs = [
                (self.proposed_date_entry, 'proposal submittal', 
                    'submitted_date'),
                (self.contract_date_entry, 'contract submittal', 
                    'accepted_date')
            ]
            po_name = DB_connect("SELECT purchase_order FROM project_budget " + \
                f"WHERE rowid={self.po_id}", database=PROJECTDB)[0][0]
            name = f'PO.ID {po_name} CO {self.data[1]}'

            project_edit_entry(self.project_id, self.data[0], 'change_order_log',
                PROJECTDB, name, 'CHANGE ORDER EDIT', self.data, self.data_dict, 
                datapairs, user=self.user, datelist=datepairs)
            self.parent.searchwindow.refresh_page()
        self.cancel_window()
        

    def display_data(self, project_id, po_id, data=None):
        self.description_entry.delete()
        self.contracted_entry.delete()
        self.proposed_entry.delete()
        self.proposed_date_entry.delete()
        self.contract_date_entry.delete()

        self.project_id = project_id
        self.po_id = po_id

        if data == None:
            self.context= 'insert'
            self.titlelabel.configure(text='NEW CHANGE ORDER')
            self.enterbutton.configure(text='ADD CHANGE ORDER')
            self.show_window()
            return

        self.data = data
        self.context = 'modify'
        
        self.description_entry.insert(self.data[self.data_dict['description']])
        self.proposed_entry.insert(self.data[self.data_dict['change_order_submitted']])
        self.contracted_entry.insert(self.data[self.data_dict['change_order_acceptance']])
        try:            
            self.proposed_date_entry.insert(datetime.strptime(self.data[self.data_dict['submitted_date']], DBTIME))
        except:
            pass
        try:
            self.contract_date_entry.insert(datetime.strptime(self.data[self.data_dict['accepted_date']], DBTIME))
        except:
            pass
        
        self.titlelabel.configure(text=f'EDIT CHANGE ORDER {self.data[1]}')
        self.enterbutton.configure(text='APPLY CHANGES')
        
        self.show_window()

