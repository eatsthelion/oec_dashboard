
from GUI.window_edit import *

from Backend.database import PROJECTDB
from Backend.database_send import project_edit_entry, project_input_entry

class EditBudgetGUI(EditWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, bg='seagreen3',width=600, height=400, 
        program_title = 'BUDGET EDITS', **kw)
        self.change_order_id = None

    def configure(self):
        ew=25 
        self.entryframe  = MyFrame(self.frame, bg=self.bg)
        self.purchase_order_entry = MyEntry(self.entryframe, width=ew)
        self.client_job_entry = MyEntry(self.entryframe,  width=ew)
        self.description_entry = MyEntry(self.entryframe, width=ew)
        self.cwa_num_entry = MyEntry(self.entryframe, width=ew)
        self.cwa_type_entry = MyEntry(self.entryframe, width=ew)
        self.items_entry = MyEntry(self.entryframe, width=ew)
        self.contingency_entry = MyEntry(self.entryframe, width=ew)
        self.billed_to_date_entry = MyEntry(self.entryframe, width=ew)
        self.status_entry = MyEntry(self.entryframe, width=ew)

        entrypairs = [
            ("Purchase Order*:", self.purchase_order_entry),
            ("Client Job No:", self.client_job_entry),
            ("Description:", self.description_entry),
            ("Invoiced:", self.billed_to_date_entry),
            ("Status:", self.status_entry),
            ("CWA No:", self.cwa_num_entry),
            ("CWA Type:", self.cwa_type_entry),
            ("Number of Items:", self.items_entry),
            ("Contingency:", self.contingency_entry),
        ]

        for row, pair in enumerate(entrypairs):
            label = MyLabel(self.entryframe, text=pair[0])
            label.grid(row=row, column = 0, padx=5, pady=(5,0), sticky=W)
            pair[1].grid(row=row, column = 1, padx=5, pady=(5,0), sticky=EW)

        self.enterbutton = MyButton(self.frame, command=self.entry_command)
        self.entryframe.pack(expand=1, padx=5)
        self.enterbutton.pack(fill='x', padx=5, pady=5)
        
        return super().configure()

    def entry_command(self):
        purchase_order = self.purchase_order_entry.get()
        client_job = self.client_job_entry.get()
        description = self.description_entry.get()
        CWA_No = self.cwa_num_entry.get()
        CWA_Type = self.cwa_type_entry.get()
        items = self.items_entry.get()
        contingency = self.contingency_entry.get()
        invoiced = self.billed_to_date_entry.get()
        status = self.status_entry.get()

        try:
            items = int(items)
        except:
            items = ''
        try:
            contingency = float(contingency)
        except:
            contingency = ''
        try: 
            invoiced = float(invoiced)
        except:
            invoiced = ''

        required = [purchase_order]
        for attribute in required:
            if attribute == '':
                messagebox.showerror('Missing Info', 
                'All required* fields must be filled before entry.')
                return

        if self.context == 'insert':
            insert_str = f"""
                '{purchase_order}', '{self.project_id}', '{client_job}', 
                '{description}', '{CWA_No}', '{CWA_Type}', '{items}', 
                '', '','', '', 
                '{contingency}', '{invoiced}', '', '', '{status}', ''"""

            project_input_entry(self.project_id, 'project_budget', PROJECTDB,
                insert_str, f"New Purchase Order {purchase_order} was created.", 
                'NEW PURCHASE ORDER', user=self.user)
            
            self.parent.searchwindow.refresh_results()
            
        elif self.context == 'modify':
            datapairs = [
                (self.data[1], purchase_order, 'purchase order', 'purchase_order'),
                (self.data[2], client_job, 'client job #', 'client_job'),
                (self.data[3], status, 'status', 'status'),
                (self.data[4], description, 'description', 'description'), 
                (self.data[5], CWA_No, 'CWA No', 'cwa_num'),
                (self.data[6], CWA_Type, 'CWA Type', 'cwa_type'),
                (self.data[7], items, 'items', 'items'),
                (self.data[10], invoiced, 'invoiced', 'billed_to_date'),
                (self.data[12], contingency, 'contingency', 'contingency'),
            ]
            name = f'PO {purchase_order}'

            project_edit_entry(self.project_id, self.data[0], 'project_budget',
                PROJECTDB, name, 'PURCHASE ORDER EDIT', datapairs, user=self.user)
            
            self.parent.searchwindow.refresh_page()
        self.cancel_window()
        return

    def display_data(self, project_id, data=None):
        self.purchase_order_entry.delete()
        self.client_job_entry.delete()
        self.description_entry.delete()
        self.cwa_num_entry.delete()
        self.cwa_type_entry.delete()
        self.items_entry.delete()
        self.contingency_entry.delete()
        self.billed_to_date_entry.delete()
        self.status_entry.delete()

        self.data = data
        self.project_id = project_id

        if data == None:
            self.context= 'insert'
            self.titlelabel.configure(text='NEW PURCHASE ORDER')
            self.enterbutton.configure(text='ADD PURCHASE ORDER')
            self.show_window()
            return
        
        self.context = 'modify'
        self.purchase_order_entry.insert(self.get_data('purchase_order'))
        self.client_job_entry.insert(self.get_data('client_job'))
        self.status_entry.insert(self.get_data('status'))
        self.description_entry.insert(self.get_data('description'))
        self.cwa_num_entry.insert(self.get_data('cwa_num'))
        self.cwa_type_entry.insert(self.get_data('cwa_type'))
        self.items_entry.insert(self.get_data('items'))
        self.billed_to_date_entry.insert(self.get_data('billed_to_date'))
        self.contingency_entry.insert(self.get_data('contingency'))

        headertext = f"EDIT {self.data[1].upper()}"
        if len(headertext)>40:
            headertext = headertext[:40]+'...'
        self.titlelabel.configure(text=headertext)
        self.enterbutton.configure(text='APPLY CHANGES')
        
        self.show_window()
        return