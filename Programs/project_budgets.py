
from Backend.exports import see_all_budgets
from Backend.database_get import get_change_orders

from GUI.window_datatable import *

from Programs.project_change_orders import ProjectChangeOrders
from Programs.edit_budget import EditBudgetGUI

class ProjectBudgetsGUI(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master, program_title = 'Project Budgets',
        bg='#118C4F', col_color='palegreen3', 
        leftoptions = self.leftoptions, 
        additional_windows = self.additonalOptions,
        format_dict="project_budget",
        **kw)

    def configure(self,**kw):
        self.current_budget_frame = MyLabelFrame(self.frame, 
            font=(FONT[0], 16), text="CURRENT TOTAL BALANCE")
        self.current_budget_label = MyLabel(self.current_budget_frame, 
            font=(FONT[0], 16), text="$0.00")
        self.current_budget_frame.pack()
        self.current_budget_label.pack()
        super().configure(**kw)
        self.terminal = Terminal(self.frame)

    def display_data(self, data, datasetget):
        super().display_data(data, datasetget)
        if len(self.searchwindow.dataset)!=0:
            total_balance = 0
            for po in self.searchwindow.dataset:
                if str(po[3]).upper() in ['CLOSED','CANCELLED']:
                    continue
                try: total_balance += po[9]
                except: pass
            self.current_budget_label.configure(text=f'${total_balance}')
        else:
            self.current_budget_label.configure(text='$0')
        
    def leftoptions(self, master,dataset,row):
        see_co_info=MyButton(master, text='ORDERS', 
            command = lambda m=dataset: self.show_co_window(m))
        update_budget = MyButton(master, text='EDIT', command=lambda m=dataset: 
            self.show_edit_window(m))
        details  = MyButton(master, text='  +  ')

        see_co_info    .grid(row=0,column=0,padx=(5,0))
        update_budget      .grid(row=0,column=1,padx=(5,0))
        details             .grid(row=0,column=3,padx=5)
        pass

    def additonalOptions(self, button_master, frame_master):
        insert_button = MyButton(button_master, text='NEW PURCHASE ORDER', 
            command=self.show_edit_window)
        multi_update_button = MyButton(button_master, text='UPDATE MANY ORDERS')   
        all_budgets_button = MyButton(button_master, text='EXPORT TO EXCEL', 
            command=lambda:
                see_all_budgets(self.data[0],self.data[1], self.terminal))

        all_budgets_button  .pack(side='left', pady=(10,2),padx=5)
        insert_button       .pack(side='left', pady=(10,2),padx=5)
        multi_update_button .pack(side='left', pady=(10,2),padx=5)

    def show_edit_window(self, data=None):
        edit_budget_window = EditBudgetGUI(self.frame, parent=self)
        edit_budget_window.display_data(self.data[0], data=data)

    def show_co_window(self, data):
        change_order_window = ProjectChangeOrders(self.frame, parent=self)
        # Changes the title of the new window
        titletext = f'CHANGE ORDERS FOR {data[1]}'
        if len(titletext)>40:
            titletext = titletext[:40]+"..."
        change_order_window.titlelabel.configure(text = f'{titletext}')

        # Sends the new dataset to the pop-up SearchWindow
        dataset_get = lambda: get_change_orders(data[0])
        change_order_window.context = 'display'
        change_order_window.project_id = self.data[0]
        change_order_window.po_id = data[0]
        change_order_window.display_data(data, dataset_get)
        
        # Changes windows to display
        change_order_window.show_full_window()

        # Sets the back button of new window to go to previous window
        change_order_window.back_direction = self.show_full_window
    