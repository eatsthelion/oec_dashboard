###################################################################################################
# catalog_budgets.py
# 
# Created: 9/09/22
# Creator: Ethan de Leon
# Purposes:
#   - Organize the database project budgets
###################################################################################################

from GUI.window_datatable import *

PROGRAMTITLE = "OEC Budget Catalog"

class BudgetCatalog(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master,
        sort_function=self.sortfunction,
        left_options = self.leftoptions, 
        additional_popups = self.additonalOptions, 
        program_title = PROGRAMTITLE,
        format_dict = 'budget_catalog',
        rowheight = 3, searchbar=True,
        bg='#19D719', search_col_bg='#F02D7D',
        **kw)

    def configure(self):
        self.titlelabel.configure(font = ("montserrat extrabold",24,'bold'), 
            text="★ "+PROGRAMTITLE.upper()+" ★", bg='white',
            height=2)
        self.titlelabel.place_forget()
        self.titlelabel.pack(fill='x')
        
        super().configure()
        self.terminal = Terminal(self.frame)
        self.hide_back_button()
        self.hide_cancel_button()

    def leftoptions(self, master,dataset,row):
        editbutton = tk.Button(master,cursor='hand2', text='EDIT', 
            font=FONT, bg='gold2', 
            command = lambda m=dataset: self.show_update_window(m))
        editbutton.grid(row=0,column=0)

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

    def additonalOptions(self, button_master, frame_master):
        #insert_window = InsertMaterialGUI(frame_master, parent=self)
        #self.update_window = UpdateMaterialGUI(frame_master, parent=self)
        #insert_button = tk.Button(button_master, text='NEW ITEM',
        #    relief='flat', font=FONT, command=insert_window.show_window)
        #insert_button.pack(side='left', pady=(10,2),padx=5)
        pass

    def show_update_window(self, data):
        self.update_window.data = data
        self.update_window.display_data()
        self.update_window.show_window()