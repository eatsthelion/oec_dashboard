###################################################################################################
# catalog_materials.py
# 
# Created: 9/02/22
# Creator: Ethan de Leon
# Purposes:
#   - Organize the database of coded materials
###################################################################################################
PROGRAMTITLE = "Material Database"

from GUI.window_datatable import *

class MaterialDatabase(DataTableWindow):
    def __init__(self, master, **kw) -> None:
        super().__init__(master,
        sort_function=self.sortfunction,
        right_options = self.rightoptions, 
        additional_popups = self.additonalOptions, 
        program_title = PROGRAMTITLE,
        format_dict='material_catalog',
        rowheight = 5, searchbar=True,
        bg='lightsteelblue3', search_col_bg='cadetblue2',
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

    def rightoptions(self, master,dataset,row):
        editbutton = tk.Button(master,cursor='hand2', text='EDIT', 
            font=FONT, bg='gold2', 
            command = lambda m=dataset: self.show_update_window(m))
        deletebutton = tk.Button(master,cursor='hand2', text='DELETE', 
            font=FONT, bg='red')
        editbutton.grid(row=0,column=0)
        deletebutton.grid(row=0,column=1)

    def sortfunction(self, sortby, dataset):
        if sortby == 'SORT BY ITEM (A-Z)': 
            named_entries = []
            nameless_entries = []
            for data in dataset:
                if data[1] in ['', None]: 
                    nameless_entries.append(data)
                    continue
                named_entries.append(data)
            named_entries.sort(key=lambda i:i[1])
            dataset = named_entries + nameless_entries
        elif sortby == 'SORT BY ITEM (Z-A)': 
            dataset.sort(key=lambda i:i[1],reverse=True)
        elif sortby == 'SORT BY CODE': 
            dataset.sort(key=lambda i:i[2])
        return dataset

    def additonalOptions(self, button_master, frame_master):
        pass
    
    def show_update_window(self, data):
        self.update_window.data = data
        self.update_window.display_data()
        self.update_window.show_window()